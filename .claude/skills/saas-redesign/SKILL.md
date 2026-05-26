---
name: saas-redesign
description: Redesign a Vue 3 application's UI into a modern SaaS-style interface - vertical navigation sidebar on the left instead of a top nav bar, consistent spacing scale, and polished professional component styling. Use this skill when asked to restyle, modernize, or redesign the app's layout/UI without changing functionality.
---

# SaaS UI Redesign Guidelines

This skill restructures a Vue 3 application's interface into a modern SaaS-style layout: a fixed vertical sidebar on the left for navigation, a clean content area with consistent spacing, and a professional level of visual polish. It is a **visual/layout refactor only** - functionality, routing, data flow, and branding stay exactly as they are.

## Scope and Hard Constraints

**Do:**
- Replace the top navigation bar with a fixed, full-height left sidebar
- Normalize spacing, typography, cards, tables, buttons, badges, and form controls across all views
- Improve hierarchy, alignment, hover/active/focus states, and empty/loading states

**Do NOT:**
- Change business logic, API calls, props/events, composables, routes, or view behavior
- Change the app's color palette or branding - detect the existing colors and keep them
- Add dependencies (no UI kits, no CSS frameworks, no icon packages - icons are inline SVG)
- Use emojis anywhere in the UI
- Rename routes, components, or i18n keys

**Project rules still apply.** Check the repository's CLAUDE.md before editing: in this repository, any creation or significant modification of a `.vue` file MUST be delegated to the **vue-expert** subagent, and significant changes should get a **code-reviewer** pass afterwards.

## Process

Work in phases and keep each phase verifiable in the running app before moving on.

### Phase 0 - Inventory (read-only)

Before touching anything, identify and write down:
1. **The app shell**: which file owns the top nav, global layout, and global styles (in this repo: `client/src/App.vue` - the unscoped `<style>` block at the bottom is the global stylesheet).
2. **Navigation mechanism**: vue-router (`<router-link>`/`<router-view>`) or a custom router (this repo uses `src/composables/useRouter.js` + a routes object in App.vue + `<component :is="currentView">`). The sidebar must reuse whatever already exists - same hrefs, same active-state logic, same click handlers.
3. **The route/view list** and the i18n keys used for nav labels (`nav.*`), so sidebar labels are identical to the current tabs.
4. **The existing palette and fonts** (this repo: slate `#0f172a` / `#64748b` / `#e2e8f0`, background `#f8fafc`, primary blue `#2563eb`/`#3b82f6`, status green/blue/yellow/red, Inter/system font). These are preserved, not replaced.
5. **Global chrome besides the nav**: filter bars, language switchers, profile menus, modals mounted at the shell level - they all need a home in the new layout.
6. **Every view's top-level structure** (`page-header`, `stats-grid`, `card` patterns) so the spacing pass can be applied consistently.

### Phase 1 - App shell: sidebar layout

Restructure the shell into a two-column layout. Keep all existing nav behavior (same links, same active logic, same i18n labels, same router calls).

```
+------------------+--------------------------------------------+
| Sidebar (fixed)  | Top bar: page context + filters + profile  |
|  Brand           +--------------------------------------------+
|  Nav links       |                                            |
|  ...             |  Main content (max-width container,        |
|                  |  consistent gutters)                       |
|  Footer: user /  |                                            |
|  language        |                                            |
+------------------+--------------------------------------------+
```

Layout rules:
- Sidebar: fixed position, full viewport height, **240px** wide, the app's darkest neutral or white surface (pick whichever matches the existing brand treatment), 1px border on the content side.
- Sidebar contents top to bottom: brand block (logo/app name + subtitle), vertical nav list, then a pinned footer area for the user/profile menu and language switcher if the app has them.
- Nav links: full-width rows, 40-44px tall, 8px radius, icon (16-20px inline SVG, `stroke="currentColor"`) + label, 8-12px gap. States: muted text by default, subtle background tint on hover, and a clearly distinct active state (filled background + accent text or a 3px left accent bar) driven by the app's existing active-route logic.
- Main area: `margin-left: 240px` (or a CSS grid with a `240px 1fr` template), content constrained to a `max-width` of 1280-1440px, centered, with 24-32px gutters.
- A slim top bar inside the content column holds anything that used to share the old top nav (global filter bar, search, profile) so no functionality is lost.
- Keep the shell sticky/fixed behavior sensible: sidebar fixed, top bar sticky, content scrolls.
- Responsive (no JS needed): below ~1024px collapse the sidebar to a 64px icon-only rail (hide labels, keep tooltips via `title`); below ~768px let the content gutters shrink. Do not introduce a JS drawer unless the app already has one.

### Phase 2 - Spacing and layout consistency

Introduce a single spacing scale and apply it everywhere instead of ad-hoc values. Add CSS custom properties to the global stylesheet (colors stay hardcoded as they are today unless the app already uses variables):

```css
:root {
  --space-1: 0.25rem;  /* 4px  */
  --space-2: 0.5rem;   /* 8px  */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-5: 1.5rem;   /* 24px */
  --space-6: 2rem;     /* 32px */
  --space-8: 3rem;     /* 48px */
  --radius-sm: 6px;
  --radius-md: 10px;
  --shadow-card: 0 1px 2px rgba(15, 23, 42, 0.05);
  --shadow-raised: 0 4px 12px rgba(15, 23, 42, 0.08);
}
```

Apply consistently:
- Page gutter: `--space-6`; vertical rhythm between page sections: `--space-5`.
- Card padding: `--space-5`; gap between cards in a grid: `--space-4` or `--space-5` (pick one and use it everywhere).
- Page header: title + one-line description, `--space-5` bottom margin, identical across every view.
- Stat-card grids: equal heights, same gap, `repeat(auto-fit, minmax(220px, 1fr))`.
- Tables: consistent cell padding (`--space-3` vertical / `--space-4` horizontal) across all views.

### Phase 3 - Component polish (using the existing palette)

- **Cards**: white surface, 1px border in the app's border color, `--radius-md`, `--shadow-card`; card headers with a consistent title size and bottom border.
- **Tables**: uppercase 11-12px letter-spaced muted column headers, zebra-free rows with a subtle hover tint, right-aligned numeric columns, consistent badge usage for statuses.
- **Buttons**: one primary style (existing accent color), one secondary (bordered neutral), consistent height (36-40px), radius `--radius-sm`, visible disabled and focus-visible states. Replace one-off gradient or inconsistent buttons with these.
- **Form controls** (inputs, selects, sliders): same height and radius as buttons, border in the existing border color, focus ring in the existing accent color.
- **Badges**: keep the existing status color mapping; normalize size, radius, and casing.
- **Typography**: page title ~1.5rem/700, card titles ~1rem/600, body 0.875rem, muted text in the existing muted color; numbers in stat cards ~1.75rem/700.
- **States**: every view keeps loading / error / empty states, styled consistently (muted, centered, padded with `--space-6`).
- Charts and custom SVG visualizations are left functionally untouched; only their containing cards/spacing change.

### Phase 4 - Per-view pass

Go view by view (smallest first) and apply Phases 2-3 classes/patterns, removing per-view one-off margins and stray inline styles. Do not restructure a view's internal logic - only its layout wrappers, classes, and scoped styles. Where several views define duplicate scoped CSS for the same pattern (cards, tables, badges), prefer promoting one definition to the global stylesheet and deleting the duplicates.

### Phase 5 - Verification

1. Run the app (backend + frontend dev servers) and click through **every** route in the sidebar.
2. Confirm: active nav state follows the route, deep links and browser back/forward still work, global filters still apply, modals open/close, language switching still works, and charts/tables render.
3. Check the browser console for new errors or Vue warnings (none should be introduced).
4. Take before/after screenshots of each view for the user.
5. Run any existing test suites; they must stay green (this is a styling-only change).

## Definition of Done

- No top nav bar remains; all navigation lives in the left sidebar with correct active states.
- Every view uses the same page-header, spacing scale, card, table, and button treatments.
- The app's original colors, branding, copy, and functionality are unchanged.
- No new dependencies, no emojis, no console errors, tests still pass.
