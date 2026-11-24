# Tallyfoot site design

The landing page at `index.html` with its stylesheet `assets/landing.css`. The Privacy and Support pages keep the minima theme, because the App Store listing links to them and their output must not change.

## Direction

Two hero directions were rendered at 1440x900: a navy page taken from the app icon background (#0F1520) and a cool light page. The light page won. The app's black screens read as devices against it, and the icon keeps its edge. On the navy page the screens and icon sank into the background.

Source of truth for every claim: the App Store listing (`docs/store/listing.md` in the app repo). The page says nothing the listing does not.

## Palette (60-30-10)

| Token | Hex | Role | Contrast on page |
| --- | --- | --- | --- |
| `--page` | #F6F8FB | Page background (60) | |
| `--ink` | #111827 | Headings, body text, footer text (30, with the black app screens) | 16.7:1 |
| `--muted` | #4B5563 | Lede, figure captions | 7.1:1 |
| `--accent` | #0A6FA8 | Links and the focus ring only (10). It is the app ring blue (#40C8FF) deepened within its hue to pass AA | 5.1:1 |
| `--rule` | #D5DBE3 | The one divider above the footer | decorative |

The app screenshots bring their own black. Nothing else on the page is black.

## Type

- Family: the system UI stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`). On Apple devices that is SF Pro, the typeface the app uses. No web fonts.
- h1: 56/1.08, weight 700, tracking -0.02em; 38 px below 720 px wide.
- h2: 36/1.15, weight 700, tracking -0.01em; 28 px below 720 px wide.
- Body: 18/1.55, weight 400. Captions and footer: 16/1.45. Nothing smaller than 16 px.
- Paragraphs stop at 34em (about 65 characters). Headings use `text-wrap: balance`, paragraphs `text-wrap: pretty`.

## Spacing and radius

- Spacing scale: 8, 16, 24, 32, 48, 80, 120 px. Tight inside a group, wider between groups, more space above a heading than below it.
- Content width: 1120 px with 24 px side padding at every width.
- Radius follows the hardware, not a UI token: watch captures 19% of width, iPhone captures 12.5% of width, the Home Screen widget 13%, the circular Lock Screen widget a full circle. The App Store badge keeps Apple's own shape.

## States

- Links: accent colour and always underlined (1 px, offset 3 px), so colour is never the only cue. Hover thickens the underline to 2 px.
- Focus: `:focus-visible` draws a 3 px accent outline, offset 3 px.
- No pending, disabled or loading states: the page is static and uses no JavaScript.

## Bans and their replacements

- No gradients, glows, shadows or decorative backgrounds. Depth comes from the app's black screens on the light page.
- No cards or boxed sections. Sections are separated by space alone, 120 px on desktop and 80 px on phones.
- No identical section layouts. The hero and watch-face sections are split columns facing opposite ways, history is a centred stack, widgets are a split with a cluster of three images, privacy and the closing call are single text columns.
- No icons, emoji, eyebrow labels, pill chips or numbered sections. Headings stand alone; the only images are real captures, the app icon and Apple's badge.
- No Inter, serif display or monospace. Everything is the system UI stack.
- No mock-ups or recoloured captures. Captures are resized, compressed and corner-clipped only. No invented device frames, Home Screens or Lock Screens.
- No hype words, invented figures or testimonials. Copy restates the listing in plain sentences.
- No duplicate navigation. The header carries only the name; Privacy and Support live in the footer and in the privacy section's text.
- No motion. Nothing animates.
- No dark mode. The captures are black; on a dark page they lose their edges.

## Copy

Written here first, then built.

**Title:** Tallyfoot: Step goal ring for Apple Watch

**Description:** Your daily step goal, right on your Apple Watch face. Build streaks with room for rest. No accounts, ads, tracking, or in-app purchases. Works on iPhone too.

**h1:** Your daily step goal, right on your Apple Watch face.

**Lede:** Tallyfoot's ring fills as you walk, with your step count in the center. It's free, with no accounts, ads, tracking or in-app purchases, and it works on iPhone alone too.

**A complication for your watch face.** Add Tallyfoot as a complication to a compatible face, such as Modular Duo or X-Large. Tinted faces draw the ring in the system tint. Open the app on your watch for a larger ring with your goal and streak. Turn on notifications to get one tap on your wrist when you reach your goal.

**Streaks with room for rest.** Six goal days in a row earn you a rest day. You can hold one at a time, and it protects your streak from a missed day. Mark a sick day on any of the last 7 days in your history, or set weekly days off in Settings. Neither breaks your streak.

**History against each day's goal.** See the last 7 days on Apple Watch, and 7 or 30 days on iPhone. Each day is measured against that day's goal.

**Home Screen and Lock Screen widgets.** Put your ring on your iPhone Home Screen or Lock Screen. Set your daily goal and ring color in the iPhone app. Lock Screen widgets use the system tint.

**Your steps stay on your devices.** Tallyfoot reads steps from Apple Health and your devices' motion sensors. It syncs between your own iPhone and Apple Watch and sends no data to the developer. Details are in the Privacy Policy. For help, see Support.

**Closing:** Tallyfoot is free on the App Store. (Heading and badge only.)

**Footer:** © 2026 Jeremy Daughhetee. Privacy Policy. Support.
