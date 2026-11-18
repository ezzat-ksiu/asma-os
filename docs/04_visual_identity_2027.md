# FOLIAVERE — Visual Identity Specification

ملخص تنفيذي 1: الهوية مبنية على حبر داكن وعاجي دافئ ولمسات معدنية محدودة، لا على الزخرفة المفرطة.
ملخص تنفيذي 2: يجب أن تبدو الدار تحريرية وذات حرفة، مع مرونة كاملة للكتب العربية والإنجليزية والفرنسية.
ملخص تنفيذي 3: الذهبي لون إبراز وزخرفة وليس لون نص صغير على الخلفية العاجية.
ملخص تنفيذي 4: قيم CMYK المعروضة للتوجيه فقط؛ ملف ICC الخاص بالمطبعة وعينة اللون هما المرجع النهائي.
ملخص تنفيذي 5: لا تُوصف الهوية بأنها “الأكثر فوزاً بالجوائز” قبل تصميمها واختبارها وتقييمها خارجياً.

## 1. Identity idea

**Concept:** The Folio Mark — two page-like vertical forms meeting around a narrow central seam, with a small open aperture suggesting a story held rather than a book icon copied literally. The mark should work as a blind emboss, one-colour foil stamp, favicon, book-spine mark and certificate seal.

**Symbolism:** the two pages represent story and reader; the central seam represents editing and craft; the open negative space represents the details that remain the customer's own. Avoid neural-network imagery, robot motifs, magic sparks, crowns, generic quills, wax-seal clichés or AI circuit lines.

### Logo construction
- Start from a square artboard of 1000 × 1000 units.
- Draw two vertical folio panels with identical outer width and a central gap equal to 0.12 of total mark width.
- Top corners: gently squared with a 0.035-unit radius; lower outer corners: 0.06 radius.
- Create a central vertical channel that opens slightly at the top, but do not create an actual letter F or V that could be mistaken for a font glyph.
- Wordmark: `FOLIAVERE` in a restrained high-contrast serif, optically tracked; use Playfair Display Medium for draft artwork and convert to outlines for print delivery after font-licence validation.
- Arabic wordmark: `فولياڤير` set in a licensed Arabic typeface with custom spacing and optical adjustment; do not force a calligraphic imitation of a Latin serif.
- Clear space: at least 0.5× mark width around the symbol; for wordmark lockup, at least cap-height on all sides.
- Minimum sizes: symbol 12 px digital / 5 mm print; full wordmark 110 px digital / 28 mm print. Below that, use the symbol only.
- Monochrome: pure one-colour black, white or foil plate; no gradients in stamp artwork.
- Reverse lockup: ivory mark and wordmark on Ink; use Gold only for premium decorative applications.

## 2. Color system

### Core palette

| Token | HEX | RGB | Role |
|---|---|---|---|
| Ink | `#171713` | 23, 23, 19 | Primary text, dark background |
| Ivory | `#F5EBDD` | 245, 235, 221 | Main paper and light surface |
| Antique Gold | `#C7A76C` | 199, 167, 108 | Foil accent, dividers and decorative marks |
| Forest | `#343D38` | 52, 61, 56 | Secondary deep surfaces |
| Cocoa | `#765D4C` | 118, 93, 76 | Leather / packaging accent |
| Bronze Text | `#75572D` | 117, 87, 45 | Accessible warm accent text |
| Editorial Blue | `#2A5064` | 42, 80, 100 | Links and secondary interactive accent |
| White | `#FFFFFF` | 255, 255, 255 | High-contrast content surface |

### Contrast checks
Ratios below are calculated from the given sRGB hex values using the WCAG relative-luminance method. They apply to the specified foreground/background pairs only, not automatically to every component state.

| Foreground / background | Contrast | Use |
|---|---:|---|
| Ink / Ivory | 15.24:1 | Body text; AAA |
| Forest / Ivory | 9.52:1 | Large headings/body text; AAA |
| Cocoa / Ivory | 5.18:1 | Normal-size text; AA |
| Bronze Text / Ivory | 5.64:1 | Normal-size text; AA |
| Editorial Blue / Ivory | 7.33:1 | Links/body emphasis; AAA |
| White / Ink | 17.97:1 | Dark-mode text; AAA |
| Ivory / Forest | 9.52:1 | Dark-panel text; AAA |
| Antique Gold / Ink | 7.85:1 | Large/small decorative or text use subject to font rendering; AAA threshold nominally met |
| Antique Gold / Ivory | 1.94:1 | Decorative only; never body text or essential icon |

WCAG 2.2 contrast reference: [W3C Understanding SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum). Normal text minimum AA is 4.5:1; large text minimum is 3:1. Interactive non-text contrast should be checked separately under the relevant success criterion. Never rely on gold-on-ivory for critical information.

### Print colour notes

The values below are approximate starting conversions, not colour-managed production values. CMYK differs by press, substrate, coating, ink set and ICC profile. **Do not send these generic numbers to a printer as final colour instructions.** Request the supplier's ICC profile and a physical proof.

| Token | Approximate CMYK starting point |
|---|---|
| Ink `#171713` | C:0 M:0 Y:17 K:91 |
| Ivory `#F5EBDD` | Prefer uncoated warm stock; do not simulate paper colour with heavy ink coverage |
| Antique Gold `#C7A76C` | C:0 M:16 Y:46 K:22; true metallic requires a separate foil/spot process |
| Forest `#343D38` | C:15 M:0 Y:8 K:76 |
| Cocoa `#765D4C` | C:0 M:21 Y:36 K:54 |

## 3. Typography

| Context | Typeface | Notes |
|---|---|---|
| English display | Playfair Display | Use Semibold for titles; avoid tiny sizes and long all-caps paragraphs. |
| English UI / body | Inter | Use Regular/Medium; strong legibility and stable UI hierarchy. |
| Arabic literary body | Amiri | Test ligatures, diacritics and line-height in actual output. |
| Arabic UI | IBM Plex Sans Arabic | Clear interface labels and metadata. |
| Serial / technical metadata | IBM Plex Mono | Only for serials, hashes and code-like values. |
| French body | Inter | Keep accents and apostrophes; do not use uppercase for long phrases. |

All fonts must be packaged with their correct licence text. Playfair Display, Inter, Amiri and IBM Plex families are available under open-font licences according to their respective distribution repositories; verify the exact file and licence before bundling. Use fallback stacks. Never rely on local user fonts for print rendering.

### Type hierarchy
- Display title: 40–56 px web / 28–38 pt print.
- H1: 36–44 px web / 24–32 pt print.
- H2: 28–32 px web / 18–24 pt print.
- H3: 20–24 px web / 14–18 pt print.
- Body: 16–18 px web / 10.5–12 pt print.
- Caption: 13–14 px web / 8.5–10 pt print, never below printer legibility requirements.

### RTL / LTR rules
- Set `dir="rtl"` on Arabic content blocks, not just text alignment.
- Use logical CSS properties (`margin-inline`, `padding-inline`, `inset-inline`) instead of left/right.
- Keep serial numbers, URLs, email addresses, currencies and model identifiers in isolated LTR spans.
- Test mixed Arabic and English words, parentheses, quotation marks, numerals, punctuation, diacritics, and line breaks.
- Do not mirror logos, numbers, QR codes, or product photography in RTL mode.

## 4. Grid and composition

- Digital content width: 1200 px maximum; editorial text column 620–720 px.
- Grid: 12 columns desktop, 8 tablet, 4 mobile; gutter 24 px desktop, 16 px mobile.
- Book text block: 65–72% of trim width with generous outer margins; test each trim SKU.
- Bleed and safe area follow the exact printer template; do not hardcode generic values.
- Keep one primary focal point per illustration; leave a predictable quiet zone for text.

## 5. Illustration style guide

**Style name:** Contemporary Literary Gouache.

Prompt-ready direction:

> Create a contemporary literary children's-book illustration with a tactile gouache-and-coloured-pencil finish. Use a restrained palette of warm ivory, ink, forest green, muted antique gold, soft terracotta and dusty blue. Light should be natural and directional, with gentle atmospheric shadows and clear separation between focal character and background. Compose each scene with one clear action and generous negative space reserved for page typography. Character design should be kind, expressive and believable without photorealism, exaggerated anatomy or uncanny facial detail. Keep clothing, hair silhouette, accessories and palette consistent with the approved character reference sheet. Avoid text, lettering, logos, watermarks, medical symbols, dangerous props, sexualised styling, stereotypes and identifiable real children. The image must remain readable at printed page size and must not place critical details in the trim or gutter area.

### Character philosophy
- Characters are fictional composites unless the commissioned product requires a permitted adult likeness.
- Children's books use symbolic or illustrated fictional protagonists by default; no biometric face matching.
- Avoid stereotypes about gender, disability, culture, religion, nationality or family structure.
- Depict capable children without implying they must be perfect, fearless or responsible for adult emotions.
- Maintain a written character bible with palette, silhouette, wardrobe, proportions and allowed variations.

## 6. Cover direction

- Front cover hierarchy: title, optional subtitle, commissioned-byline or dedication only if approved, Foliovere imprint mark.
- Do not clutter with “Edition 1 of 1” as a large sales badge; place serial on the certificate and discreetly on the colophon.
- Spine width must be computed from the printer's chosen stock and page count, not guessed.
- Back cover: short synopsis, imprint, legally required identifiers if applicable, no invented endorsements or fabricated reviews.
- Foil artwork must be supplied as a separate spot-colour / vector layer only where the printer supports it.

## 7. Packaging and unboxing

- Exterior: recyclable rigid mailer or corrugated shipper sized to the actual book.
- Inner wrap: uncoated ivory tissue or paper band; avoid plastic where practical.
- Closure: one-colour paper seal, not a fake wax seal that can crack in transit.
- Insert: certificate, personal letter, QR card, care note.
- Protection: corner protection and moisture barrier appropriate to destination shipping.
- No perfume or scented insert by default.
- Packaging cost is an estimate until a pack test and supplier quote are recorded.

## 8. Motion and sonic identity

### Motion
- Page-reveal transition: 240–360 ms ease-out; no exaggerated flip-book animation.
- Mark reveal: two folio panels move into alignment with a subtle 4 px easing motion.
- Respect `prefers-reduced-motion`; all content remains available without animation.
- No auto-playing audio. Audio is initiated by a clear play control.

### Sonic
- Use an original two-note restrained tonal signature commissioned or generated with clear commercial rights.
- Audio narration uses a licensed synthetic voice; no voice cloning from a child or third party without documented authority and rights.
- Do not imitate a known publisher's sonic identity or musical composition.

## 9. Photography and mockup direction

- Photograph actual sample books after physical proof, in natural directional light, with paper grain and binding visible.
- Use uncluttered surfaces: warm limestone, dark wood, linen and neutral bookcase contexts.
- 3D mockups must be labelled “digital mockup” until physical sample photography exists.
- Portfolio characters must be synthetic and must not resemble an identifiable child.
- Do not create fake hotel installations, customer testimonials, press logos or awards.

## 10. Decision Log

| Decision | Owner | Why |
|---|---|---|
| Adopt Contemporary Literary Gouache as the illustration direction | Brand + Creative | Distinctive and reproducible without imitating a living illustrator. |
| Use Ink/Ivory as core accessible pair | Brand + Accessibility | Strong verified contrast for editorial text. |
| Restrict Antique Gold on Ivory to non-text decoration | Accessibility + Brand | 1.94:1 contrast fails normal text requirements. |
| Use physical samples to determine final CMYK and finishing | Publishing | Screen colour is not press proof. |
| Avoid “award-winning” claims until independently awarded | CEO + Legal | No award has been established. |

**Sign-off:** Chief Brand Officer — visual system; World Luxury Publishing Expert — print craft; Accessibility reviewer — contrast and interaction verification required.
