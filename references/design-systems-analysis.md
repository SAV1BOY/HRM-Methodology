# Design Systems Analysis Reference

> Knowledge base for analyzing, designing, and evaluating component-based design systems. Used by the HRM when DOMINIO includes DESIGN, WEB, or REACT and the task involves design system work.

---

## Core Principles of Design Systems

### What Makes a Good Design System

1. **Consistency**: Unified visual language across all components
2. **Composability**: Components combine predictably
3. **Scalability**: System grows without breaking existing patterns
4. **Accessibility**: Built-in a11y from the ground up
5. **Documentation**: Every component is documented with usage guidelines
6. **Token-Based**: Design decisions abstracted into tokens (colors, spacing, typography)

### Design Token Hierarchy

```
Global Tokens (brand level)
    |
    v
Alias Tokens (semantic meaning)
    |
    v
Component Tokens (component-specific)
```

**Example**:
- Global: `color-blue-500: #3B82F6`
- Alias: `color-primary: {color-blue-500}`
- Component: `button-bg-primary: {color-primary}`

### Advanced Token Architecture Patterns

> Source: Synthetic content based on advanced design systems analysis (PDF `design_systems_avancados_analise_completa.pdf` was not readable due to system tooling limitations; content synthesized from equivalent domain knowledge).

#### Three-Tier Token Architecture (Detailed)

Design tokens operate across three tiers, each with distinct responsibilities:

**Tier 1 -- Primitive/Global Tokens** (raw values, no semantic meaning):
```json
{
  "color": {
    "blue": {
      "100": { "value": "#DBEAFE" },
      "200": { "value": "#BFDBFE" },
      "500": { "value": "#3B82F6" },
      "700": { "value": "#1D4ED8" },
      "900": { "value": "#1E3A5F" }
    },
    "neutral": {
      "0":   { "value": "#FFFFFF" },
      "50":  { "value": "#F9FAFB" },
      "900": { "value": "#111827" }
    }
  },
  "spacing": {
    "1":  { "value": "4px" },
    "2":  { "value": "8px" },
    "3":  { "value": "12px" },
    "4":  { "value": "16px" },
    "6":  { "value": "24px" },
    "8":  { "value": "32px" }
  },
  "fontFamily": {
    "sans":  { "value": "Inter, system-ui, sans-serif" },
    "mono":  { "value": "JetBrains Mono, monospace" }
  },
  "fontSize": {
    "xs":   { "value": "12px" },
    "sm":   { "value": "14px" },
    "base": { "value": "16px" },
    "lg":   { "value": "18px" },
    "xl":   { "value": "20px" },
    "2xl":  { "value": "24px" },
    "3xl":  { "value": "30px" }
  }
}
```

**Tier 2 -- Semantic/Alias Tokens** (intent-based, theme-switchable):
```json
{
  "color": {
    "bg": {
      "primary":   { "value": "{color.neutral.0}" },
      "secondary": { "value": "{color.neutral.50}" },
      "inverse":   { "value": "{color.neutral.900}" },
      "brand":     { "value": "{color.blue.500}" },
      "danger":    { "value": "{color.red.500}" }
    },
    "text": {
      "primary":   { "value": "{color.neutral.900}" },
      "secondary": { "value": "{color.neutral.600}" },
      "inverse":   { "value": "{color.neutral.0}" },
      "brand":     { "value": "{color.blue.700}" }
    },
    "border": {
      "default":   { "value": "{color.neutral.200}" },
      "focus":     { "value": "{color.blue.500}" },
      "error":     { "value": "{color.red.500}" }
    }
  },
  "spacing": {
    "inset": {
      "sm":  { "value": "{spacing.2}" },
      "md":  { "value": "{spacing.4}" },
      "lg":  { "value": "{spacing.6}" }
    },
    "stack": {
      "sm":  { "value": "{spacing.2}" },
      "md":  { "value": "{spacing.4}" },
      "lg":  { "value": "{spacing.8}" }
    }
  }
}
```

**Tier 3 -- Component Tokens** (component-scoped, referencing semantic tokens):
```json
{
  "button": {
    "bg": {
      "primary":   { "value": "{color.bg.brand}" },
      "secondary": { "value": "{color.bg.secondary}" },
      "danger":    { "value": "{color.bg.danger}" }
    },
    "text": {
      "primary":   { "value": "{color.text.inverse}" },
      "secondary": { "value": "{color.text.primary}" }
    },
    "padding": {
      "sm": { "value": "{spacing.inset.sm} {spacing.3}" },
      "md": { "value": "{spacing.inset.md} {spacing.4}" },
      "lg": { "value": "{spacing.inset.lg} {spacing.6}" }
    },
    "borderRadius": { "value": "{borderRadius.md}" },
    "fontSize": {
      "sm": { "value": "{fontSize.sm}" },
      "md": { "value": "{fontSize.base}" },
      "lg": { "value": "{fontSize.lg}" }
    }
  }
}
```

#### Token Governance Rules

1. **No raw values in components**: Components MUST reference component tokens. Component tokens reference semantic tokens. Semantic tokens reference primitives. Never skip levels.
2. **Theme switching only changes Tier 2**: When switching light/dark mode, ONLY semantic tokens change. Primitive and component tokens remain stable.
3. **Token naming convention**: `{category}.{property}.{variant}.{state}` (e.g., `color.bg.primary.hover`)
4. **Token validation pipeline**: Lint -> Resolve -> Transform -> Distribute (via Style Dictionary, Tokens Studio, or similar)
5. **Multi-platform output**: Same token source generates CSS custom properties, iOS Swift constants, Android XML resources, and React Native style objects.

#### Token Composition Patterns

```
Simple Composition:
  button.bg.primary = color.bg.brand = color.blue.500 = #3B82F6

Conditional Composition (theme-aware):
  [light] color.bg.brand = color.blue.500
  [dark]  color.bg.brand = color.blue.400

Responsive Composition:
  [mobile]  spacing.inset.md = spacing.3  (12px)
  [desktop] spacing.inset.md = spacing.4  (16px)

State Composition:
  button.bg.primary         = color.blue.500
  button.bg.primary.hover   = color.blue.600
  button.bg.primary.active  = color.blue.700
  button.bg.primary.disabled = color.blue.300 + opacity.50
```

---

## Analysis Framework

### When Analyzing an Existing Design System

Use this structured approach:

#### 1. Token Audit
- Catalog all design tokens (colors, spacing, typography, shadows, borders)
- Check for inconsistencies (e.g., 47 different grays)
- Identify missing semantic tokens
- Map tokens to their usage frequency

#### 2. Component Inventory
- List all components with their variants
- Map component dependencies (what uses what)
- Identify primitive vs compound components
- Check for duplicate/overlapping components

#### 3. Pattern Analysis
- Layout patterns (grid, flex, container queries)
- Interaction patterns (hover, focus, active states)
- Responsive patterns (breakpoints, fluid typography)
- Animation patterns (transitions, motion preferences)

#### 4. Accessibility Audit
- Color contrast ratios (WCAG AA minimum)
- Keyboard navigation paths
- Screen reader annotations (ARIA)
- Focus management patterns
- Reduced motion support

#### 5. Technical Architecture
- Component API design (props, slots, composition)
- State management approach
- Theming mechanism (CSS variables, styled-components, Tailwind)
- Build and distribution pipeline

---

## Advanced Component API Design Patterns

> Source: Synthetic content based on advanced design systems analysis (PDF not readable; synthesized from domain expertise).

### Compound Components Pattern

Compound components share implicit state through React context, allowing flexible composition while maintaining internal coordination.

```tsx
// Usage - consumer controls structure, component manages state
<Select onValueChange={handleChange}>
  <Select.Trigger>
    <Select.Value placeholder="Choose option..." />
  </Select.Trigger>
  <Select.Content>
    <Select.Group>
      <Select.Label>Fruits</Select.Label>
      <Select.Item value="apple">Apple</Select.Item>
      <Select.Item value="banana">Banana</Select.Item>
    </Select.Group>
    <Select.Separator />
    <Select.Group>
      <Select.Label>Vegetables</Select.Label>
      <Select.Item value="carrot">Carrot</Select.Item>
    </Select.Group>
  </Select.Content>
</Select>
```

**Implementation skeleton**:
```tsx
const SelectContext = React.createContext<SelectContextValue | null>(null);

function useSelectContext() {
  const ctx = React.useContext(SelectContext);
  if (!ctx) throw new Error("Select.* must be used within <Select>");
  return ctx;
}

function Select({ children, onValueChange, defaultValue }) {
  const [value, setValue] = React.useState(defaultValue ?? "");
  const [open, setOpen] = React.useState(false);

  const contextValue = React.useMemo(() => ({
    value, setValue: (v) => { setValue(v); onValueChange?.(v); },
    open, setOpen,
  }), [value, open, onValueChange]);

  return (
    <SelectContext.Provider value={contextValue}>
      {children}
    </SelectContext.Provider>
  );
}

Select.Trigger = function Trigger({ children }) { /* uses context */ };
Select.Content = function Content({ children }) { /* uses context */ };
Select.Item = function Item({ value, children }) { /* uses context */ };
// ... other sub-components
```

**When to use**: Complex interactive components (Select, Tabs, Accordion, Dialog, Combobox) where consumers need structural control.

### Polymorphic Components Pattern (`as` / `asChild`)

Allow a component to render as a different HTML element or another component while preserving its styling and behavior.

```tsx
// Approach 1: "as" prop (traditional)
<Button as="a" href="/docs">Go to Docs</Button>  // renders <a> with Button styles
<Text as="label" htmlFor="name">Name</Text>       // renders <label> with Text styles

// Approach 2: "asChild" prop (Radix approach - preferred)
<Button asChild>
  <a href="/docs">Go to Docs</a>  // merges Button behavior onto <a>
</Button>
```

**Implementation pattern (asChild with Slot)**:
```tsx
import { Slot } from "@radix-ui/react-slot";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ asChild = false, variant = "primary", size = "md", className, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        ref={ref}
        className={cn(buttonVariants({ variant, size }), className)}
        {...props}
      />
    );
  }
);
```

**When to use**: Any component that might need to render as a different element (Buttons as links, Text as different heading levels, layout primitives).

### Slot Pattern (Named Slots / Render Props)

Provide designated insertion points for custom content within a component.

```tsx
// Named slots via props
<Card
  header={<CardTitle>Dashboard</CardTitle>}
  media={<img src="/chart.png" alt="Chart" />}
  actions={
    <>
      <Button variant="ghost">Cancel</Button>
      <Button>Save</Button>
    </>
  }
>
  <p>Card body content goes here.</p>
</Card>

// Named slots via compound components (preferred for complex cases)
<Card>
  <Card.Header>
    <Card.Title>Dashboard</Card.Title>
    <Card.Description>Overview of metrics</Card.Description>
  </Card.Header>
  <Card.Content>
    <p>Card body content.</p>
  </Card.Content>
  <Card.Footer>
    <Button variant="ghost">Cancel</Button>
    <Button>Save</Button>
  </Card.Footer>
</Card>
```

### Headless Component Pattern

Separate behavior/logic from visual presentation entirely. The component provides state management and accessibility, the consumer provides all rendering.

```tsx
// Headless hook approach
function useToggle(initialState = false) {
  const [on, setOn] = React.useState(initialState);
  const toggle = React.useCallback(() => setOn(prev => !prev), []);
  const buttonProps = {
    "aria-pressed": on,
    onClick: toggle,
    role: "switch",
  };
  return { on, toggle, setOn, buttonProps };
}

// Usage
function CustomSwitch() {
  const { on, buttonProps } = useToggle();
  return (
    <button {...buttonProps} className={on ? "switch-on" : "switch-off"}>
      {on ? "ON" : "OFF"}
    </button>
  );
}
```

**Reference implementations**: Radix UI Primitives, React Aria (Adobe), Headless UI (Tailwind Labs), Downshift, TanStack Table.

### Component Variant Architecture (CVA Pattern)

Use Class Variance Authority or similar for type-safe variant management.

```tsx
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  // Base classes (always applied)
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary:   "bg-blue-600 text-white hover:bg-blue-700",
        secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
        ghost:     "hover:bg-gray-100 text-gray-700",
        danger:    "bg-red-600 text-white hover:bg-red-700",
        link:      "text-blue-600 underline-offset-4 hover:underline",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
        icon: "h-10 w-10",
      },
    },
    compoundVariants: [
      { variant: "link", size: "sm", className: "h-auto px-0" },
      { variant: "link", size: "lg", className: "h-auto px-0 text-base" },
    ],
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

type ButtonVariants = VariantProps<typeof buttonVariants>;
```

**Advantages**: Type-safe variants, compound variant support, tree-shakeable, framework-agnostic variant logic.

---

## Advanced Accessibility Audit Framework

> Source: Synthetic content based on advanced design systems analysis.

### WCAG 2.2 Compliance Matrix for Design Systems

| Level | Criterion | Design System Responsibility | Testing Method |
|-------|-----------|------------------------------|----------------|
| A | 1.1.1 Non-text Content | All `<img>` components require `alt`; icon components require `aria-label` | Static analysis + unit test |
| A | 1.3.1 Info and Relationships | Semantic HTML in all components; ARIA roles where needed | axe-core + manual review |
| A | 2.1.1 Keyboard | All interactive components keyboard-operable | Cypress/Playwright keyboard tests |
| A | 2.4.3 Focus Order | Logical tab order; no focus traps (except modals) | Manual + automated tab sequence |
| A | 4.1.2 Name, Role, Value | All form controls labeled; custom widgets have ARIA | axe-core + screen reader testing |
| AA | 1.4.3 Contrast (Minimum) | Token system enforces 4.5:1 for text, 3:1 for large text | Token-level contrast validation |
| AA | 1.4.11 Non-text Contrast | UI component boundaries meet 3:1 ratio | Automated contrast checker |
| AA | 2.4.7 Focus Visible | All focusable elements have visible focus indicator | Visual regression + `:focus-visible` audit |
| AAA | 2.4.13 Focus Appearance | Focus indicator is >= 2px, contrasts against adjacent colors | Token-level enforcement |

### Accessibility Testing Pipeline

```
Stage 1: Build-Time (Static Analysis)
  - eslint-plugin-jsx-a11y (catches ~30% of issues)
  - TypeScript props enforcing required aria-* attributes
  - Token contrast validation (automated, every token change)

Stage 2: Component-Level (Unit/Integration)
  - @testing-library/jest-dom (toHaveAccessibleName, toBeVisible, etc.)
  - axe-core integration via jest-axe
  - Keyboard navigation unit tests for every interactive component

Stage 3: Page-Level (E2E)
  - Playwright/Cypress with axe-core injection
  - Tab-order verification
  - Screen reader output validation (optional, via specialized tools)

Stage 4: Manual Audit (Periodic)
  - Screen reader testing (NVDA, VoiceOver, JAWS)
  - Cognitive load assessment
  - Motion sensitivity testing (prefers-reduced-motion)
  - High contrast mode verification
```

### Focus Management Patterns

```tsx
// Pattern 1: Focus trap for modals/dialogs
function Dialog({ open, onClose, children }) {
  const dialogRef = React.useRef(null);
  const previousFocusRef = React.useRef(null);

  React.useEffect(() => {
    if (open) {
      previousFocusRef.current = document.activeElement;
      // Move focus into dialog
      dialogRef.current?.querySelector("[data-autofocus]")?.focus()
        || dialogRef.current?.focus();
    }
    return () => {
      // Restore focus on close
      previousFocusRef.current?.focus();
    };
  }, [open]);

  // Trap focus within dialog (Tab and Shift+Tab cycle)
  // ...
}

// Pattern 2: Roving tabindex for composite widgets
function RadioGroup({ options, value, onChange }) {
  return (
    <div role="radiogroup">
      {options.map((opt, i) => (
        <div
          key={opt.value}
          role="radio"
          aria-checked={value === opt.value}
          tabIndex={value === opt.value ? 0 : -1}
          onKeyDown={(e) => {
            if (e.key === "ArrowDown" || e.key === "ArrowRight") {
              // Focus and select next option
            }
            if (e.key === "ArrowUp" || e.key === "ArrowLeft") {
              // Focus and select previous option
            }
          }}
        >
          {opt.label}
        </div>
      ))}
    </div>
  );
}

// Pattern 3: Live regions for dynamic content
function Toast({ message, type }) {
  return (
    <div
      role={type === "error" ? "alert" : "status"}
      aria-live={type === "error" ? "assertive" : "polite"}
      aria-atomic="true"
    >
      {message}
    </div>
  );
}
```

### Required ARIA Patterns per Component Type

| Component | Required ARIA | Keyboard Pattern |
|-----------|--------------|-----------------|
| Button | `role="button"` (implicit), `aria-pressed` (toggle), `aria-expanded` (menu trigger) | Enter/Space to activate |
| Dialog/Modal | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` | Escape to close, focus trap |
| Tabs | `role="tablist/tab/tabpanel"`, `aria-selected`, `aria-controls` | Arrow keys between tabs |
| Accordion | `role="region"`, `aria-expanded`, `aria-controls` | Enter/Space to toggle |
| Combobox | `role="combobox"`, `aria-expanded`, `aria-activedescendant`, `aria-autocomplete` | Arrow keys, Enter to select, Escape to close |
| Menu | `role="menu/menuitem"`, `aria-haspopup`, `aria-expanded` | Arrow keys navigate, Enter selects, Escape closes |
| Tooltip | `role="tooltip"`, triggered by `aria-describedby` | Appears on focus and hover, Escape dismisses |
| Alert | `role="alert"` or `aria-live="assertive"` | No keyboard interaction (informational) |
| Progress | `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax` | No keyboard interaction |

---

## Performance Optimization Patterns for Design Systems

> Source: Synthetic content based on advanced design systems analysis.

### Bundle Size Optimization

#### Tree-Shaking Architecture
```
// BAD: Barrel exports that prevent tree-shaking
// index.ts
export * from "./Button";
export * from "./Dialog";
export * from "./Table";  // 50KB component included even if unused

// GOOD: Package-level exports with sideEffects: false
// package.json
{
  "sideEffects": false,
  "exports": {
    "./Button": "./dist/Button/index.js",
    "./Dialog": "./dist/Dialog/index.js",
    "./Table":  "./dist/Table/index.js"
  }
}

// Consumer imports only what's needed:
import { Button } from "@ds/react/Button";  // only Button's code
```

#### Per-Component CSS Isolation
```
// Each component ships its own CSS (or CSS-in-JS) independently
// No global stylesheet that must be loaded entirely

// Option A: CSS Modules per component
import styles from "./Button.module.css";

// Option B: Tailwind with PurgeCSS (only used classes shipped)

// Option C: CSS-in-JS with zero-runtime (vanilla-extract, Linaria)
import { style } from "@vanilla-extract/css";
export const button = style({ padding: 16, borderRadius: 8 });
```

### Runtime Performance Patterns

#### Component Memoization Strategy
```tsx
// 1. Memoize expensive components
const DataTable = React.memo(function DataTable({ data, columns }) {
  // ...expensive render with many rows
});

// 2. Stabilize callback/object props
function Parent() {
  const handleSort = React.useCallback((col) => { /* ... */ }, []);
  const columns = React.useMemo(() => [
    { key: "name", label: "Name" },
    { key: "email", label: "Email" },
  ], []);

  return <DataTable data={data} columns={columns} onSort={handleSort} />;
}

// 3. Use composition to avoid unnecessary re-renders
// BAD: Context value changes re-render all consumers
<ThemeContext.Provider value={{ theme, setTheme, colors, spacing }}>

// GOOD: Split contexts by update frequency
<ThemeValueContext.Provider value={{ theme, colors, spacing }}>
  <ThemeSetterContext.Provider value={setTheme}>
    {children}
  </ThemeSetterContext.Provider>
</ThemeValueContext.Provider>
```

#### Lazy Loading Components
```tsx
// Lazy load heavy components (Dialogs, Popovers, DatePickers, Rich Text Editors)
const DatePicker = React.lazy(() => import("@ds/react/DatePicker"));
const RichTextEditor = React.lazy(() => import("@ds/react/RichTextEditor"));

// Show lightweight placeholder while loading
<React.Suspense fallback={<InputSkeleton />}>
  <DatePicker value={date} onChange={setDate} />
</React.Suspense>
```

#### CSS Performance Rules
```css
/* 1. Avoid expensive selectors in design system CSS */
/* BAD: deep descendant selectors */
.card .card-body .card-text p { }

/* GOOD: flat, specific selectors */
.card-text { }

/* 2. Use CSS containment for complex components */
.data-table {
  contain: layout style paint;
}

/* 3. Use content-visibility for off-screen content */
.virtual-list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 50px;
}

/* 4. Leverage CSS layers for token/component ordering */
@layer tokens, base, components, utilities;

@layer tokens {
  :root { --color-primary: #3B82F6; }
}
@layer components {
  .button { background: var(--color-primary); }
}
```

### Performance Budgets for Design System Components

| Component Type | Max JS (gzipped) | Max CSS (gzipped) | Max First Paint | Max TTI Impact |
|---------------|-------------------|-------------------|-----------------|----------------|
| Button, Badge, Tag | < 1 KB | < 0.5 KB | < 5ms | Negligible |
| Input, Select, Checkbox | < 2 KB | < 1 KB | < 10ms | < 5ms |
| Dialog, Popover, Tooltip | < 3 KB | < 1 KB | < 15ms (lazy) | < 10ms |
| Table, DataGrid | < 10 KB | < 2 KB | < 30ms (lazy) | < 50ms |
| DatePicker, RichText | < 15 KB | < 3 KB | < 50ms (lazy) | < 100ms |

---

## Design System Migration Strategies

> Source: Synthetic content based on advanced design systems analysis.

### Migration Approaches

#### 1. Strangler Fig Pattern (Recommended for Large Codebases)

Incrementally replace old components with new ones, coexisting during transition.

```
Phase 1: Foundation (Weeks 1-4)
  - Install new design system alongside old one
  - Map old tokens to new tokens (create bridge/compatibility layer)
  - Establish migration tracking dashboard

Phase 2: Primitives First (Weeks 5-12)
  - Migrate tokens: old CSS vars -> new CSS vars (compatibility aliases)
  - Migrate primitive components: Button, Input, Text, Icon
  - Use codemod scripts for automated prop mapping
  - Keep old components with deprecation warnings

Phase 3: Compound Components (Weeks 13-24)
  - Migrate complex components: Dialog, Tabs, Table, Form
  - Each compound migration = mini-project with its own tests
  - Parallel running: old and new components coexist

Phase 4: Cleanup (Weeks 25-30)
  - Remove old design system dependency
  - Remove compatibility/bridge layer
  - Final visual regression sweep
```

#### 2. Big Bang Migration (Small Codebases Only)

Replace everything at once in a single coordinated effort.

```
Preconditions:
  - Codebase < 50 components consuming design system
  - Dedicated team for 1-2 sprint migration
  - Comprehensive visual regression test suite EXISTS

Steps:
  1. Complete token mapping (old -> new)
  2. Write codemods for all component API changes
  3. Run codemods across entire codebase
  4. Fix edge cases manually
  5. Run visual regression tests
  6. Deploy in single release
```

#### 3. Micro-Frontend Boundary Migration

Different parts of the app migrate at different times, isolated by micro-frontend boundaries.

```
App Shell      -> migrated first (navigation, layout)
Feature A MFE  -> migrated in sprint N
Feature B MFE  -> migrated in sprint N+2
Feature C MFE  -> migrated in sprint N+4
Legacy MFE     -> remains on old system (decommissioned later)
```

### Token Migration Tooling

```javascript
// Token bridge: maps old token names to new token values
// Generates CSS custom property aliases

const tokenBridge = {
  // Old system -> New system
  "--old-color-primary":    "var(--new-color-bg-brand)",
  "--old-color-text":       "var(--new-color-text-primary)",
  "--old-spacing-sm":       "var(--new-spacing-2)",
  "--old-spacing-md":       "var(--new-spacing-4)",
  "--old-border-radius":    "var(--new-radius-md)",
};

// Generate bridge CSS
function generateBridgeCSS(bridge) {
  const declarations = Object.entries(bridge)
    .map(([oldToken, newRef]) => `  ${oldToken}: ${newRef};`)
    .join("\n");
  return `:root {\n${declarations}\n}`;
}
```

### Component Migration Codemod Example

```javascript
// jscodeshift codemod: migrate OldButton -> NewButton
module.exports = function transformer(file, api) {
  const j = api.jscodeshift;
  const root = j(file.source);

  // Rename import
  root.find(j.ImportDeclaration, {
    source: { value: "@old-ds/react" }
  }).find(j.ImportSpecifier, {
    imported: { name: "OldButton" }
  }).forEach(path => {
    path.node.imported.name = "Button";
    path.parent.node.source.value = "@new-ds/react/Button";
  });

  // Rename component usage
  root.find(j.JSXIdentifier, { name: "OldButton" })
    .forEach(path => { path.node.name = "Button"; });

  // Map props: kind="primary" -> variant="primary"
  root.find(j.JSXAttribute, { name: { name: "kind" } })
    .filter(path => {
      return path.parent.node.name.name === "Button";
    })
    .forEach(path => {
      path.node.name.name = "variant";
    });

  return root.toSource();
};
```

### Migration Quality Checklist

```
Token Layer:
  [ ] All primitive tokens mapped to new equivalents
  [ ] Semantic tokens preserve same visual intent
  [ ] Dark mode tokens verified after migration
  [ ] Custom/override tokens accounted for

Component Layer:
  [ ] All component API changes documented (old prop -> new prop)
  [ ] Codemod covers >= 90% of transformations
  [ ] Edge cases (custom className, ref forwarding, event handlers) tested
  [ ] Compound components maintain same composition patterns

Visual Regression:
  [ ] Chromatic/Percy/Playwright screenshot comparison
  [ ] < 0.1% pixel diff threshold (excluding intentional changes)
  [ ] All viewport sizes verified (mobile, tablet, desktop)
  [ ] All themes verified (light, dark, high-contrast)

Accessibility:
  [ ] axe-core audit passes with zero violations post-migration
  [ ] Keyboard navigation paths unchanged
  [ ] Screen reader announcements verified for changed components
  [ ] Focus indicator styling maintained

Performance:
  [ ] Bundle size delta documented (should decrease or stay flat)
  [ ] No new runtime CSS-in-JS overhead introduced
  [ ] Lighthouse scores maintained or improved
```

---

## Advanced Theming Patterns

> Source: Synthetic content based on advanced design systems analysis.

### Multi-Theme Architecture

```css
/* Theme implementation via CSS custom properties + data attributes */

/* Base tokens (all themes share these primitives) */
:root {
  --font-sans: Inter, system-ui, sans-serif;
  --font-mono: JetBrains Mono, monospace;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
}

/* Light theme (default) */
[data-theme="light"], :root {
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F9FAFB;
  --color-bg-tertiary: #F3F4F6;
  --color-text-primary: #111827;
  --color-text-secondary: #6B7280;
  --color-border-default: #E5E7EB;
  --color-brand-500: #3B82F6;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
}

/* Dark theme */
[data-theme="dark"] {
  --color-bg-primary: #111827;
  --color-bg-secondary: #1F2937;
  --color-bg-tertiary: #374151;
  --color-text-primary: #F9FAFB;
  --color-text-secondary: #9CA3AF;
  --color-border-default: #374151;
  --color-brand-500: #60A5FA;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
}

/* High contrast theme */
[data-theme="high-contrast"] {
  --color-bg-primary: #000000;
  --color-bg-secondary: #1A1A1A;
  --color-text-primary: #FFFFFF;
  --color-text-secondary: #E0E0E0;
  --color-border-default: #FFFFFF;
  --color-brand-500: #5CB3FF;
}
```

### Theme Switching Implementation

```tsx
function ThemeProvider({ children, defaultTheme = "system" }) {
  const [theme, setTheme] = React.useState(() => {
    if (typeof window === "undefined") return defaultTheme;
    return localStorage.getItem("theme") ?? defaultTheme;
  });

  React.useEffect(() => {
    const root = document.documentElement;
    const resolved = theme === "system"
      ? (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")
      : theme;

    root.setAttribute("data-theme", resolved);
    localStorage.setItem("theme", theme);
  }, [theme]);

  React.useEffect(() => {
    if (theme !== "system") return;
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = (e) => {
      document.documentElement.setAttribute(
        "data-theme", e.matches ? "dark" : "light"
      );
    };
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

---

## Technique Pipeline for Design System Tasks

### For Design System Analysis (REVIEW)

```
1. step-back-prompting     -> Abstract: What design principles apply?
2. chain-of-thought        -> Analyze each layer systematically
3. checklist-prompting     -> Verify against design system checklist
4. multi-agent-debate      -> Compare approaches (if multiple options)
```

### For Design System Creation (BUILD)

```
1. step-back-prompting     -> Establish design principles first
2. analogical-prompting    -> Reference existing design systems
3. plan-and-solve          -> Plan token hierarchy -> components -> documentation
4. self-refine             -> Iterate on component APIs
5. checklist-prompting     -> Verify completeness and consistency
```

### For Design System Migration (FIX/BUILD)

```
1. chain-of-thought        -> Map current system to target
2. least-to-most           -> Migrate tokens first, then primitives, then compounds
3. checklist-prompting     -> Verify each migration step
4. chain-of-verification   -> Verify no regressions
```

---

## Quality Criteria for Design Systems

| Criterion | Threshold | How to Verify |
|-----------|-----------|--------------|
| Token consistency | 100% | No raw values in components |
| Color contrast | WCAG AA (4.5:1 text, 3:1 large) | Automated contrast checker |
| Component documentation | 100% | Every exported component has docs |
| Accessibility | WCAG 2.1 AA | axe-core or similar |
| Responsive | All breakpoints covered | Visual regression testing |
| Type scale | Mathematical ratio | Consistent scale ratio |
| Spacing scale | Mathematical ratio | Consistent base unit |

---

## Reference Design Systems

| System | Strengths | When to Reference |
|--------|-----------|------------------|
| Material Design 3 | Token system, adaptive color | Token architecture |
| Radix UI | Unstyled primitives, composition | Component API design |
| shadcn/ui | Copy-paste, Tailwind native | Developer experience |
| Chakra UI | Accessible defaults, token system | Accessibility patterns |
| Ant Design | Enterprise patterns, dense UIs | Data-heavy interfaces |
| Apple HIG | Platform consistency, motion | Native-feel web apps |

---

## Integration with HRM

### When HRM Encounters Design System Tasks

1. **Step 0.7 (Registry Lookup)**: Check if task involves design system keywords
2. **Step 6 (Decomposition)**: Decompose into token, component, and documentation workstreams
3. **Step 9.5 (Prompt Generation)**: Use technique pipeline from this reference
4. **Step 11 (Verification)**: Apply design system quality criteria

### Keywords That Trigger This Reference

- "design system", "component library", "design tokens"
- "UI architecture", "component API"
- "style guide", "brand system"
- "Storybook", "design documentation"
- "token migration", "component migration", "design system migration"
- "compound components", "polymorphic components", "headless UI"
- "accessibility audit", "WCAG", "a11y"
- "design system performance", "bundle size", "tree-shaking"

---

## Design System Testing Strategy

> Source: Synthetic content based on advanced design systems analysis.

### Testing Pyramid for Design Systems

```
                    /\
                   /  \
                  / E2E \          Visual regression (Chromatic/Percy)
                 /________\        Cross-browser a11y scans
                /          \
               / Integration \     Component composition tests
              /______________\     Context/provider interaction
             /                \
            /     Unit Tests    \  Individual component rendering
           /____________________\  Props/variants, ARIA attributes
          /                      \
         /    Static Analysis      \ ESLint (a11y, hooks), TypeScript
        /__________________________\  Token validation, prop types
```

### Visual Regression Testing Setup

```typescript
// Chromatic / Storybook visual regression
// Each component has stories covering:
// 1. All variants
// 2. All sizes
// 3. All states (hover, focus, active, disabled, loading, error)
// 4. All themes (light, dark, high-contrast)
// 5. Edge cases (long text, empty state, RTL)

export const ButtonMatrix: Story = {
  render: () => (
    <div style={{ display: "grid", gap: 16 }}>
      {(["primary", "secondary", "ghost", "danger"] as const).map(variant =>
        (["sm", "md", "lg"] as const).map(size => (
          <Button key={`${variant}-${size}`} variant={variant} size={size}>
            {variant} {size}
          </Button>
        ))
      )}
      <Button disabled>Disabled</Button>
      <Button loading>Loading</Button>
      <Button>
        Very Long Button Text That Might Overflow Or Wrap To Multiple Lines
      </Button>
    </div>
  ),
};
```

---

## Design System Governance Model

> Source: Synthetic content based on advanced design systems analysis.

### Contribution Workflow

```
1. Proposal Phase
   - RFC document: problem statement, proposed API, alternatives considered
   - Design review with DS team
   - Accessibility review (required for all new components)

2. Implementation Phase
   - Feature branch with component, tests, stories, docs
   - Visual regression baseline captured
   - Performance budget check (bundle size delta)

3. Review Phase
   - Code review (2 approvals minimum)
   - Accessibility audit (automated + manual)
   - Visual regression approval
   - Documentation completeness check

4. Release Phase
   - Semantic versioning (breaking changes = major bump)
   - Changelog auto-generated from conventional commits
   - Migration guide for breaking changes
   - Deprecation warnings added 1 major version before removal
```

### Component Maturity Model

| Stage | Label | Criteria | Support Level |
|-------|-------|----------|--------------|
| 0 | Experimental | Idea/RFC exists, no implementation | None |
| 1 | Alpha | Initial implementation, API unstable | Best-effort |
| 2 | Beta | API stabilizing, basic tests + stories | Bug fixes |
| 3 | Stable | Full tests, docs, a11y audit, performance budget met | Full support |
| 4 | Mature | Widely adopted, battle-tested, optimized | Long-term support |
| 5 | Deprecated | Superseded, migration guide available | Security fixes only |

---

## Source Note

The advanced content in this reference file (sections on Advanced Token Architecture, Component API Design Patterns, Accessibility Audit Framework, Performance Optimization, Migration Strategies, Theming Patterns, Testing Strategy, and Governance Model) was intended to be sourced from the PDF `design_systems_avancados_analise_completa.pdf`. Due to system tooling limitations (PDF rendering tool `pdftoppm` not available on this Windows environment), the content was synthesized from equivalent domain expertise covering the same topics. If the PDF becomes readable in a future session, this file should be cross-referenced and updated with any PDF-specific patterns, case studies, or data not covered here.
