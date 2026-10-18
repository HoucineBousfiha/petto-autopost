# PETTO brand guide (for the daily design job)

**What PETTO is:** an AI pet-care app. Meals, walks, meds and vet records in one calm app, remembered by AI. Free on iOS & Android.
**Voice:** warm, calm, a little funny. Short sentences. Pets "talk" with deadpan humour (lower-case texts, dramatic complaints). Never preachy, never fake stats or fake reviews.

## Look
- Canvas: always **1080×1350** (4:5). Root element: `<div class="post">`.
- Fonts: **Bricolage Grotesque 800** for headlines (72–96px, tight leading), **DM Sans** 400/500/700 for body (24–32px).
- Colours (CSS vars in `brand/brand.css`):
  - Light posts: background `--cream #FCF3EC`, text `--navy #1E2A3B`, secondary `--slate #4A5464`, accent `--clay #A65F47`, chips `--blush #F3DED1`.
  - Dark posts: background `--navy`, text white, accent `--peach #F0A98C`, cards `rgba(255,255,255,0.09)`.
  - Optional third accent: `--sage #3E6B44`.
- Accent the last word or phrase of a headline in clay (light) or peach (dark).
- Rounded everything: cards 28–32px radius, pills 999px.
- Logo: `<img class="logo" src="../brand/logo.png" alt="PETTO logo">` next to the `PETTO` wordmark, on every post.
- Icons: simple inline stroke SVG (stroke-width 2, round caps). **No emoji in the designs** (emoji are fine in captions).
- Generous padding: 80–96px sides.
- No gradient washes, no stock-photo look, no lorem ipsum, no invented numbers.

## Post mix per day (4 posts)
1. **Morning – Useful tip** (light): a real, safe, general pet-care tip, plus how PETTO helps.
2. **Lunch – Fun** (dark): pet humour formats like "if your cat could text", "honest dog review", "your day vs theirs", "things your pet is judging you for".
3. **Afternoon – Feature** (light): one PETTO feature (reminders, meal log, walk tracker, med schedule, vet records, AI answers) shown as a simple UI card mockup.
4. **Evening – Fun or engagement** (dark or light): a question, poll-style "this or that", relatable meme-style layout.

## Captions
- 1–3 short lines + a call to action (comment, tag a friend, link in bio).
- 3–6 hashtags, always including `#PETTO`.
- Medical topics: general advice only, and say "ask your vet" when relevant.
