---
name: Farmacia
description: Navy and turquoise pharmacy management workspace
colors:
  ground: "#e3edf5"
  surface: "#f5f9ff"
  surface-raised: "#ffffff"
  ink: "#152c46"
  muted: "#536c83"
  line: "#ccdae7"
  nav: "#102b45"
  accent: "#007e8a"
  cyan: "#15d3d7"
  blue: "#508fe1"
  button-primary: "#087f8a"
  button-hover: "#066975"
  button-active: "#055e68"
typography:
  body:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "0.9rem"
    lineHeight: 1.55
  title:
    fontSize: "1.35rem"
    fontWeight: 650
    letterSpacing: "-0.025em"
  metric:
    fontSize: "1.85rem"
    fontWeight: 650
    letterSpacing: "-0.035em"
  label:
    fontSize: "0.82rem"
rounded:
  badge: "6px"
  button-small: "8px"
  control: "10px"
  card: "18px"
  sidebar: "22px"
  login: "24px"
spacing:
  card: "22px"
  card-mobile: "16px"
  page: "24px"
components:
  button-primary:
    backgroundColor: "{colors.button-primary}"
    textColor: "#ffffff"
    rounded: "{rounded.control}"
    padding: "0.6rem 0.95rem"
  button-primary-hover:
    backgroundColor: "{colors.button-hover}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "{spacing.card}"
---

# Design System: Farmacia

## Overview

**Creative North Star: "Calm pharmacy workspace"**

Navy navigation anchors a cool, spacious workspace. Turquoise marks actions and selected states; blue supports charts. Soft, rounded cards separate operational information with ambient shadows. Light, dim and dark variants preserve the same hierarchy.

**Key Characteristics:**

- Navy navigation and turquoise actions.
- Soft raised cards over cool backgrounds.
- Compact operational typography and aligned numbers.
- Three persistent appearance variants.

## Colors

Primary: the navy `nav` anchors navigation; turquoise `accent` marks links, focus and progress. Bright `cyan` highlights the brand and selected details. Secondary: `blue` supports charts. Neutral `ground`, `surface` and `surface-raised` create three layers; `ink`, `muted` and `line` carry content and separators. Primary button colors are explicit, stable teal values across themes.

**The Semantic Surface Rule.** Use the theme variables for backgrounds, text and borders so every screen follows the selected appearance.

Light uses the frontmatter primitives. Dim changes ground, surfaces, separators and shadow; dark also changes ink, muted text, accent and navy. Exact overrides are recorded in the sidecar and implemented by `:root[data-theme]`.

## Typography

The current body uses Segoe UI with system fallbacks. The title and metric roles inherit this family. Numbers use tabular spacing. Titles are compact; KPI numbers carry stronger visual emphasis. Table body text is (.82rem), table headings (.75rem, weight 600), navigation (.85rem), and small KPI annotations (.77rem). Mobile KPI numbers reduce to (1.6rem). These are application typography roles, not a prescription for a new marketing display face.

## Layout

The application frame is centered, with maximum width (1680px), outer vertical margin (22px), horizontal padding (24px), and gap (18px). The navy sidebar is (218px) wide. Header content wraps rather than truncating tools. Cards use Bootstrap responsive grids; report metrics occupy two columns below the large breakpoint and four above it. Report charts split into 7/5 columns at Bootstrap's xl breakpoint.

At widths up to (991px), sidebar width becomes (190px), frame padding and gap become (14px), and chart contents wrap. Up to (767px), the sidebar becomes a horizontal scrolling navigation strip, the frame uses (16px) padding, card bodies use (16px), and tables have a minimum width of (620px) inside scrolling regions. The net chart has a minimum width of (340px). From (1600px), the top frame margin increases to (32px).

Login centers a card capped at (440px) with (36px) body padding, reduced to (26px) on mobile; its theme picker returns to normal document flow on mobile.

## Elevation & Depth

Cards combine tonal separation with soft ambient shadows. Card borders are absent; header separators remain subtle. The shared shadow changes with appearance: light (`0 7px 18px #18355216`), dim (`0 8px 20px #0a21333b`), dark (`0 8px 22px #00000029`). Shared header, card shadow utilities and login use this vocabulary.

## Shapes

Cards and modals share gently rounded corners; navigation is more enclosing and login more rounded. Controls use the smaller control radius. Status badges and progress tracks use the badge radius. The theme picker is pill shaped (24px), with circular state buttons. Charts use round donut geometry and rounded bar tops (7px).

## Components

- **Buttons:** primary and success actions share teal fill, white text and a semibold label; hover and pressed fills deepen. Secondary actions use the semantic border and text, with navy hover fill. Small buttons reduce radius and padding.
- **Fields:** raised surface, semantic border, control radius and padding (.65rem .8rem). Focus uses the accent border and a soft turquoise halo; all keyboard targets receive a (3px) accent outline with (3px) offset.
- **Navigation:** pale text on navy; hover lightens text over a blue panel; selected items use turquoise text and weight 600. Mobile preserves readable labels through horizontal scrolling.
- **Cards:** semantic surface, no outer stroke, optional shared shadow, padded body and a separated header. Featured KPI cards use a navy panel and bright turquoise metric.
- **Badges:** compact semantic fills distinguish warning, danger, success and neutral statuses, always with visible text. They are labels rather than interactive controls.
- **Theme picker:** three buttons use `aria-pressed` to expose the selected state. `html[data-theme]` selects light, dim or dark. The key `farmacia-theme` persists selection in localStorage; invalid values fall back to light. Storage failure is tolerated. An early head script sets the theme before styles render.
- **Tables and reports:** retain right-aligned monetary values, tabular numerals, explicit legends and accessible chart summaries. The shared script wraps uncontained tables in focusable regions labelled “Tabla desplazable”.

Source of truth: `farmacia_pos/apps/mockups/templates/mockups/_theme.html`, `_layout.html`, `_theme_script.html`, `login.html` and `reportes.html`. Shared templates own the visual system. Use `python manage.py export_mockups <output>` from `farmacia_pos` to regenerate the deployed static HTML; verify relative links, theme selectors and persistence in that export as well as Django rendering.

## Do's and Don'ts

### Do:

- Do reuse semantic CSS variables across all three themes.
- Do keep tables and charts horizontally scrollable when their content needs more room.
- Do regenerate the static export after changing Django templates.

### Don't:

- Don't hard-code light surfaces into new components.
- Don't replace visible data labels with color alone.
- Don't edit generated export pages as the primary source.
