# Tallyfoot site design

The landing page at `index.html` with its stylesheet `assets/landing.css`. The Privacy and Support pages keep the minima theme, because the App Store listing links to them and their output must not change.

## Direction

Dark page, by the owner's choice (2026-11-23: the light page was too bright). The page is a dark slate (#12161C), lighter than the app's pure-black screens, and every capture and the app icon carry a 1 px edge line (`--screen-edge`) so they keep their outline instead of sinking into the page.

Source of truth for every claim: the App Store listing (`docs/store/listing.md` in the app repo). The page says nothing the listing does not.

## Palette (60-30-10)

| Token | Hex | Role | Contrast on page |
| --- | --- | --- | --- |
| `--page` | #12161C | Page background (60) | |
| `--ink` | #F2F4F7 | Headings, body text, footer text (30) | 16.5:1 |
| `--muted` | #A7B0BD | Lede, figure captions | 8.3:1 |
| `--accent` | #5CC4F5 | Links and the focus ring only (10). It is the app ring blue (#40C8FF), lightened slightly within its hue | 9.2:1 |
| `--rule` | #2A313B | The one divider above the footer | decorative |
| `--screen` | #000000 | Backdrop behind captures, so image edges stay black like the screens | |
| `--screen-edge` | #2E3640 | 1 px outline around captures and the app icon | 1.5:1, decorative |

The app screenshots bring their own black. Nothing else on the page is black.

## Type

- Family: the system UI stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`). On Apple devices that is SF Pro, the typeface the app uses. No web fonts.
- h1: 56/1.08, weight 700, tracking -0.02em; 38 px below 720 px wide.
- h2: 36/1.15, weight 700, tracking -0.01em; 28 px below 720 px wide.
- Body: 18/1.55, weight 400. Captions and footer: 16/1.45. Nothing smaller than 16 px.
- Tokens: `--t-h1` 56, `--t-h1-sm` 38, `--t-h2` 36, `--t-h2-sm` 28, `--t-lede` 20 (hero lede and the header name), `--t-body` 18, `--t-small` 16.
- Paragraphs stop at 34em (about 65 characters). Headings use `text-wrap: balance`, paragraphs `text-wrap: pretty`.

## Spacing and radius

- Spacing scale: 8, 16, 24, 32, 48, 80, 120 px. Tight inside a group, wider between groups, more space above a heading than below it.
- Content width: 1120 px with 24 px side padding at every width.
- `--r-control` 8 px: the focus outline around links and the badge. It is the only UI radius.
- Image display widths: header icon 44 px, hero watch 340 px (260 px on phones), paired captures 240 px, App Store badge 150x50 px (Apple's 120x40 badge scaled evenly).
- Radius follows the hardware, not a UI token: watch captures 19% of width, iPhone captures 12.5% of width, the app icon 22.5%. The App Store badge keeps Apple's own shape.

## States

- Links: accent colour and always underlined (1 px, offset 3 px), so colour is never the only cue. Hover thickens the underline to 2 px.
- Focus: `:focus-visible` draws a 3 px accent outline, offset 3 px.
- No pending, disabled or loading states: the page is static and uses no JavaScript.

## Bans and their replacements

- No gradients, glows, soft shadows or decorative backgrounds. Depth comes from the app's black screens on the slate page; the only line around them is the 1 px edge.
- No cards or boxed sections. Sections are separated by space alone, 120 px on desktop and 80 px on phones.
- No identical section layouts. The hero and watch-face sections are split columns facing opposite ways, history is a centred stack, widgets, privacy and the closing call are single text columns. Widgets have no images: only renders existed, not device captures.
- No icons, emoji, eyebrow labels, pill chips or numbered sections. Headings stand alone; the only images are real captures, the app icon and Apple's badge.
- No Inter, serif display or monospace. Everything is the system UI stack.
- No mock-ups or recoloured captures. Captures are resized, compressed and corner-clipped only. No invented device frames, Home Screens or Lock Screens.
- No hype words, invented figures or testimonials. Copy restates the listing in plain sentences.
- No duplicate navigation. The header carries only the name; Privacy and Support live in the footer and in the privacy section's text.
- No motion. Nothing animates.
- One theme only, dark. No light/dark switch.

## Copy

Written here first, then built.

**Title:** Tallyfoot: Step goal ring for Apple Watch

**Description:** Your daily step goal, right on your Apple Watch face. Build streaks with room for rest. No accounts, ads, tracking, or in-app purchases. Works on iPhone too.

**h1:** Your daily step goal, right on your Apple Watch face.

**Lede:** Tallyfoot's ring fills as you walk, with your step count in the center. It's free, with no accounts, ads, tracking or in-app purchases, and it works on iPhone alone too.

**A complication for your watch face.** Add Tallyfoot as a complication to a compatible face, such as Modular Duo or X-Large. Tinted faces draw the ring in the system tint. The Tallyfoot watch app shows your ring too. Turn on notifications to get one tap on your wrist when you reach your goal.

**Streaks with room for rest.** Six goal days in a row earn you a rest day. You can hold one at a time, and it protects your streak from a missed day. Mark a sick day on any of the last 7 days in your history, or set weekly days off in Settings. Neither breaks your streak.

**History against each day's goal.** See the last 7 days on Apple Watch, and 7 or 30 days on iPhone. Each day is measured against that day's goal.

**Home Screen and Lock Screen widgets.** Put your ring on your iPhone Home Screen or Lock Screen. Set your daily goal and app ring color in the iPhone app. Lock Screen widgets use the system tint.

**Your steps stay on your devices.** Tallyfoot reads steps from Apple Health and your devices' motion sensors. It syncs between your own iPhone and Apple Watch and sends no data to the developer. Details are in the Privacy Policy. For help, see Support.

**Closing:** Tallyfoot is free on the App Store. (Heading and badge only.)

**Footer:** © 2026 Jeremy Daughhetee. Privacy Policy. Support.
