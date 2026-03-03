# Example Session: Coding Task

> **User Task:** "Build rate-limiting middleware for a FastAPI application that supports per-user and per-endpoint limits with a sliding window algorithm backed by Redis."

## Task Analysis

```yaml
task_type: code-generation
complexity: moderate
constraints:
  latency: normal
  token_budget: large
  quality: production
  tools_available: [code_interpreter]
language: python
framework: fastapi
output_format: code-with-tests
```

## Technique Selection

| Rank | Technique | Score | Rationale |
|------|-----------|-------|-----------|
| 1 | Plan-and-Solve | 0.94 | Coding benefits from upfront decomposition |
| 2 | Program of Thoughts | 0.91 | Code is both solution and reasoning trace |
| 3 | Self-Refine | 0.88 | Code review catches bugs and improves quality |
| 4 | Checklist Prompting | 0.82 | Production-quality verification |

**Playbook match:** `playbooks/code-generation.md` — exact match!

## Pipeline Design

```
Plan-and-Solve → Program of Thoughts → Self-Refine → Checklist Prompting
```

## Execution Trace

### Step 1: Plan-and-Solve

**Prompt:**
```
You are a senior software engineer. Before writing any code, create a detailed
implementation plan for the following task.

TASK: Build rate-limiting middleware for a FastAPI application that supports
per-user and per-endpoint limits with a sliding window algorithm backed by Redis.

CONSTRAINTS:
- Language: Python 3.11+
- Framework: FastAPI
- Storage: Redis (async via redis.asyncio)
- Must be production-ready

Create your plan covering:
1. Requirements Analysis (inputs, outputs, edge cases, performance)
2. Design Decisions (data structures, patterns, API surface)
3. Implementation Steps (ordered)
4. Testing Strategy
5. Error Handling
```

**Output:**
```
## 1. Requirements Analysis
- Input: HTTP request with user identifier (header or IP) and endpoint path
- Output: Either pass request through or return 429 Too Many Requests
- Edge cases:
  - Missing user ID → fall back to client IP
  - Redis unavailable → configurable fail-open or fail-closed
  - Clock skew between Redis and application
  - Concurrent requests from same user (race condition)
- Performance: Must add < 5ms latency per request

## 2. Design Decisions
- Sliding window via Redis sorted sets (ZADD + ZRANGEBYSCORE + ZREMRANGEBYSCORE)
- Use Redis pipeline (MULTI/EXEC) to avoid race conditions
- Configuration via Pydantic model with per-endpoint overrides
- Dependency injection for Redis client (testability)
- Standard rate limit headers: X-RateLimit-Limit, X-RateLimit-Remaining,
  X-RateLimit-Reset, Retry-After

## 3. Implementation Steps
1. Define RateLimitConfig and RateLimitRule Pydantic models
2. Implement SlidingWindowLimiter class with check_and_increment method
3. Create FastAPI middleware that calls the limiter
4. Add response headers for rate limit info
5. Write unit tests with mock Redis
6. Write integration test with TestClient

## 4. Testing Strategy
- Unit: SlidingWindowLimiter with fakeredis
- Integration: Full middleware with FastAPI TestClient
- Cases: under limit, at limit, over limit, Redis failure, missing user ID

## 5. Error Handling
- Redis connection errors → log warning, apply fail_open policy
- Invalid config → raise ValueError at startup
- Malformed user ID → sanitize and hash
```

### Step 2: Program of Thoughts

**Prompt:**
```
Following the implementation plan below, write the complete code.
Use code comments to explain your reasoning at each step.

IMPLEMENTATION PLAN:
{plan_output}

Generate production-quality Python code with type hints, docstrings,
and error handling.
```

**Output:**
```python
# rate_limiter/config.py
from pydantic import BaseModel, Field

class RateLimitRule(BaseModel):
    """Defines a rate limit for an endpoint or default."""
    requests: int = Field(gt=0, description="Max requests in window")
    window_seconds: int = Field(gt=0, description="Sliding window size")

class RateLimitConfig(BaseModel):
    """Global rate limit configuration."""
    default_rule: RateLimitRule = RateLimitRule(requests=100, window_seconds=60)
    endpoint_rules: dict[str, RateLimitRule] = Field(default_factory=dict)
    fail_open: bool = True
    user_id_header: str = "X-User-ID"
```

```python
# rate_limiter/limiter.py
import time
import hashlib
from dataclasses import dataclass
from redis.asyncio import Redis

@dataclass
class RateLimitResult:
    allowed: bool
    limit: int
    remaining: int
    reset_at: float

class SlidingWindowLimiter:
    """Sliding window rate limiter backed by Redis sorted sets."""

    def __init__(self, redis: Redis):
        self._redis = redis

    async def check_and_increment(
        self, key: str, rule_requests: int, rule_window: int
    ) -> RateLimitResult:
        """Check rate limit and record request atomically using Redis pipeline."""
        now = time.time()
        window_start = now - rule_window

        # Use pipeline for atomicity — prevents race condition between
        # check and increment
        async with self._redis.pipeline(transaction=True) as pipe:
            # Remove expired entries outside the sliding window
            pipe.zremrangebyscore(key, 0, window_start)
            # Count current requests in window
            pipe.zcard(key)
            # Add current request with timestamp as score
            pipe.zadd(key, {f"{now}:{id(pipe)}": now})
            # Set TTL to auto-cleanup
            pipe.expire(key, rule_window + 1)
            results = await pipe.execute()

        current_count = results[1]  # zcard result
        allowed = current_count < rule_requests

        if not allowed:
            # Remove the request we just added since it's denied
            await self._redis.zrem(key, f"{now}:{id(pipe)}")

        return RateLimitResult(
            allowed=allowed,
            limit=rule_requests,
            remaining=max(0, rule_requests - current_count - (1 if allowed else 0)),
            reset_at=now + rule_window,
        )

    @staticmethod
    def build_key(user_id: str, endpoint: str) -> str:
        """Build a Redis key from user ID and endpoint."""
        safe_user = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        return f"ratelimit:{safe_user}:{endpoint}"
```

```python
# rate_limiter/middleware.py
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from redis.asyncio import Redis
from .config import RateLimitConfig
from .limiter import SlidingWindowLimiter

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis: Redis, config: RateLimitConfig):
        super().__init__(app)
        self.limiter = SlidingWindowLimiter(redis)
        self.config = config

    async def dispatch(self, request: Request, call_next):
        user_id = self._get_user_id(request)
        endpoint = request.url.path
        rule = self.config.endpoint_rules.get(endpoint, self.config.default_rule)

        try:
            key = SlidingWindowLimiter.build_key(user_id, endpoint)
            result = await self.limiter.check_and_increment(
                key, rule.requests, rule.window_seconds
            )
        except Exception:
            logger.warning("Redis error during rate limit check", exc_info=True)
            if self.config.fail_open:
                return await call_next(request)
            return JSONResponse({"error": "Service unavailable"}, status_code=503)

        if not result.allowed:
            return JSONResponse(
                {"error": "Rate limit exceeded", "retry_after": result.reset_at},
                status_code=429,
                headers=self._build_headers(result),
            )

        response = await call_next(request)
        response.headers.update(self._build_headers(result))
        return response

    def _get_user_id(self, request: Request) -> str:
        """Extract user ID from header or fall back to client IP."""
        user_id = request.headers.get(self.config.user_id_header)
        if not user_id:
            user_id = request.client.host if request.client else "unknown"
        return user_id

    @staticmethod
    def _build_headers(result) -> dict[str, str]:
        return {
            "X-RateLimit-Limit": str(result.limit),
            "X-RateLimit-Remaining": str(result.remaining),
            "X-RateLimit-Reset": str(int(result.reset_at)),
        }
```

### Step 3: Self-Refine

**Critique:**
```
Issues Found:
- [HIGH] Race condition still possible: the ZADD happens before we know if
  allowed, and the cleanup ZREM is not atomic. Use Lua script instead.
- [MEDIUM] The unique key `f"{now}:{id(pipe)}"` could collide in high-
  concurrency scenarios. Use UUID or a counter.
- [LOW] Missing __init__.py files for the package.
- [LOW] _get_user_id should handle X-Forwarded-For for proxied setups.

Fixes applied:
- Replaced pipeline with Lua script for true atomicity
- Used uuid4 for unique request identifiers
- Added X-Forwarded-For fallback
- Added __init__.py with public exports
```

### Step 4: Checklist Verification

```
Production Readiness Checklist:
- [PASS] All requirements implemented (per-user, per-endpoint, sliding window)
- [PASS] Edge cases handled (missing user ID, Redis failure, concurrent requests)
- [PASS] Type annotations on all public functions
- [PASS] Docstrings on all public classes and methods
- [PASS] Error handling with configurable fail-open/fail-closed
- [PASS] No hardcoded secrets or credentials
- [PASS] Rate limit headers follow RFC 6585 conventions
- [PASS] Lua script prevents race conditions
- [PASS] Redis keys have TTL (no memory leaks)
- [FAIL] Missing Retry-After header on 429 responses → FIXED
```

## Pipeline Cost Summary

| Step | API Calls | Tokens Used | Latency |
|------|-----------|------------|---------|
| Plan-and-Solve | 1 | ~800 | ~4s |
| Program of Thoughts | 1 | ~2500 | ~10s |
| Self-Refine | 2 | ~2000 | ~8s |
| Checklist | 1 | ~800 | ~3s |
| **Total** | **5** | **~6100** | **~25s** |
