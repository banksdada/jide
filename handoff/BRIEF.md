# Jide Arowolo: design and build brief

For the developer agent building the production web application. Stack: **Laravel + Filament**. The static prototype in the parent folder is the design reference. Open `index.html` in a browser to see it. Copy its look and behaviour exactly, then replace the hard-coded content and the stubbed forms with real, admin-managed data.

## 1. Who and what

- **Client:** Jide Arowolo, a self-taught Nigerian-born afro pop, gospel and worship musician, songwriter and producer based in London. The old site (jidearowolo.com) is offline and is being reactivated at the same address.
- **Goal:** a premium, luxurious artist site that lets visitors listen, learn his story, watch, and book him for events.
- **Audience:** church and event organisers, fans, promoters, collaborators. Many visitors will be on phones.
- **Tone:** warm, confident, plain English. No hype.
- **Build for mobile first.** Every layout starts at 360px wide.

## 2. Pages and routes

| Route | Page | Purpose |
|---|---|---|
| `/` | Home | Welcome screen (first visit only), hero, "The sound" photo panels, albums row, booking call to action |
| `/music` | Music | Sticky album tabs; one panel per album with cover, description, YouTube link, track list, sample player |
| `/story` | Story | Portrait and biography, timeline, "Beyond the stage" cards, call to action |
| `/watch` | Watch | YouTube embed, link to channel, gallery |
| `/book` | Book Jide | Qualifying booking form, plus guest book form and approved messages |
| `POST /book`, `POST /guestbook` | Form handlers | Validate, store, notify |
| `/sitemap.xml`, `/robots.txt` | SEO | Generated from the database |

Navigation: the JA monogram logo (links home), Home, Music, Story, Watch, and a pill button "Book Jide". The current page is marked with `aria-current="page"`. On phones the links collapse into a menu button.

## 3. Design system

Copy the tokens from `styles.css` (`:root`). Summary:

**Colour (dark theme only):** ink `#0e0a07` (page), umber `#1a120c` and `#241910` (panels), gold `#c9a24b` (accent), brass `#e6c987` (light accent, headings accents), ivory `#f3e9d6` (text), muted `#b9a98f` (secondary text), line `rgba(201,162,75,.28)` (borders). Error text `#f0a08c`.

**Type:** Bodoni Moda 500 for display and headings (Google Fonts), Figtree 400/500/600 for body and controls. Scale: h1 `clamp(2.8rem, 13vw, 5.8rem)`, h2 `clamp(1.9rem, 6vw, 3.1rem)`, h3 1.3 to 1.5rem serif, body 1rem at line-height 1.65. Keep lines under about 62 characters.

**Layout:** content max width 1120px; side gutter 20px, 32px from 700px up; breakpoints at 700px and 960px. Radius: covers 6px, cards 8 to 12px, buttons fully round. Minimum touch target 44px.

**Logos** (in `logo/`, SVG with the lettering already converted to outlines, so no font is needed): `ja-monogram-nav.svg` is the nav logo, a JA monogram inside a ring of sound-level ticks. `jide-arowolo-wordmark.svg` is the footer logo, "JIDE AROWOLO" with a sound-wave line under it. `favicon.svg` is the browser tab icon. `ja-monogram.svg` (on dark) and `ja-monogram-transparent.svg` are for other uses. `images/share.jpg` (1200x630) is the default share image. The client has not yet chosen between the monogram and the wordmark for the main logo, so keep both as swappable components.

**Components to build as Blade components** (names are suggestions): `nav`, `footer`, `button` (variants gold, ghost, small), `cover` (image with a styled fallback showing the title if the image is missing), `page-head` (title, lede, background image, sound-wave strip), `album-panel`, `track-list`, `player`, `sound-card`, `welcome`, `timeline`, `info-card`, `cta-band`, `form-field`, `form-status`, `equaliser`, `logo-mark` (inline SVG).

## 4. Motion (keep it restrained)

1. **Welcome screen** on the home page, first visit per browser session only. A full-screen split: Jide's portrait (`images/jide-portrait.webp` on the gold glow) on one half, and on the other the JA monogram, the greeting "E kaabo · Welcome", his name, his own welcome line and an "Enter the site" button. The piano photo (`images/bg-piano.jpg`) sits behind everything under a dark overlay as a very quiet background. On desktop and landscape phones the portrait is the left half and fades into the text side; on portrait phones it is the top 40% (46% on short screens) and the monogram is hidden on short screens. It lifts away on click or Escape. Focus moves to the button; page scroll is locked while it is open.
2. **No line-art anywhere.** The client found small icon-style graphics childish and asked for the guitar and bass drawings to be removed from the welcome screen too. Do not add line-art instruments.
3. **Revolving logo.** On the nav monogram and the larger monogram on the welcome screen, the ring of sound ticks rotates slowly around a steady JA (24s a turn in the nav, 30s on the welcome screen). The prototype inlines the SVG and animates the `.logo-ring` group with CSS. With `prefers-reduced-motion` it does not turn.
4. **Sound-wave bars** are decorative. They sit along the bottom of the home hero and music page header, and a small one in the player. They animate continuously and speed up while a sample is playing.
5. **Phone Book Jide bar.** Below 820px wide, every page has one wide gold pill button fixed to the bottom of the screen, always visible: a slow light shimmer sweeps across it every few seconds, five small sound-wave bars move beside the label, and it presses in slightly when tapped. It respects the phone safe area, adds bottom padding to the page so the footer is never hidden, sits under the welcome screen, and on the Music page the player floats just above it. It links to the booking page; on the booking page itself it scrolls to the form. Hidden on tablets and desktop. (`.bookbar` in styles.css, markup at the end of each page.)
6. **Reveal on scroll:** cards and text blocks fade up once.
7. **Reduced motion:** with `prefers-reduced-motion`, no animation; drawings show complete, bars are static.

## 5. Page details

**Home.** Hero: kicker, headline "Music with roots, made to lift.", lede, buttons Listen now (to /music) and Book Jide. Right side: Dreams cover large, Roots cover small overlapping at bottom-left. Sound-wave strip along the bottom. Section "The sound": four large cinematic photo panels (piano, drum, saxophone, violin) in a 2 by 2 grid on wide screens, each with a heading and one sourced line. Panels are titled by sound, not instrument, so they do not imply what Jide plays. Section "Five albums, 2001 to 2011": five linked covers, each with the album name on one line and the year on a line below. Order is newest first for now (see open items). Call to action band.

**Music.** Page head with the drum photo. Sticky tab bar jumps to each album. Each album panel: cover, title and year, description, gold "Listen on YouTube" button, track list in two columns on wide screens. Track buttons play an audio sample if one exists. If none, the player says "Sample not added yet. Listen on YouTube." The player is a fixed bar at the bottom with play/pause, title, album, mini sound-wave and close.

**Story.** Violin photo header. Two-column intro: portrait (a transparent cut-out, `images/jide-portrait.webp`, sitting on a gold-to-umber radial glow; the original with its white background is kept in `images/source/`), biography text and three highlight figures. Then "Stages around the world": nine country cards (Nigeria, The Gambia, Sierra Leone, United Kingdom, Romania, Hungary, Germany, Canada, United States), each with a short place or detail line. Then "The story so far": a dated timeline in three eras (Nigeria: the early years, 1984 to 1998; The Gambia and the wider world, 1995 to 2005; London and abroad, 2006 to 2014), about 21 entries from Jide's music CV. Then eight "Beyond the stage" cards (the first two, Roots Festival and United Nations, carry a CD cover image), (Roots Festival, United Nations, commissioned recordings, producer credits, teaching and training, Universal Recording Studio, hotel stage, concerts and giving back). Then "From the archive": five scans of two CDs in `images/archive/` (Roots theme song front, back and dedication; International Year of Volunteers front and track listing), in two captioned groups, each opening in a dialog lightbox on click (plain links to the image without JavaScript). Then a call to action. All of this content is in `build_prototype.py` (`ERAS`, `PLACES`, `BEYOND`) and should become admin-managed.

**Watch.** Sax photo header. YouTube embed of the channel's uploads or album playlists (see open items), then a button linking to the channel. Gallery of three photos.

**Book Jide.** Piano photo header. Booking form fields: name, email, what you are booking for (select), event date, location, expected audience (select), budget range (select), about your event (min 15 characters). Guest book: name, where writing from, message; approved messages are listed above the form. Both forms validate on the client (messages in `script.js`) and again on the server.

## 6. Data model and admin (Filament)

Admin panel at `/admin`, single admin user to start. Tables:

- `albums`: title, slug, year, description, cover image, YouTube playlist ID (optional), sort order, published.
- `tracks`: album, title, slug, sort order, audio file (optional), YouTube video ID (optional).
- `career_events`: era, date label (free text such as "1989 to 1993"), text, sort order, published. The era is a heading (title and range) that groups entries.
- `places`: country, detail line, sort order.
- `highlights`: title, text, sort order (the "Beyond the stage" cards).
- `events`: title, starts at, venue, city, link, published. Shown on the home or Watch page when any exist (the prototype has the empty state only).
- `videos`: title, YouTube ID, sort order, published.
- `photos`: image, alt text, caption, sort order, published.
- `bookings`: name, email, type, event date, location, audience size, budget range, message, status (new, contacted, confirmed, declined), internal notes, timestamps.
- `guestbook_entries`: name, place, message, status (pending, approved, hidden), timestamps.
- `settings` (single row): site name, YouTube channel URL, booking notification email, social links, welcome message.

Filament resources: Career (events, places and highlights), Album (with a reorderable Tracks relation manager and audio upload), Booking (filter by status, quick status actions, view page, CSV export), Guestbook (approve and hide, including bulk actions), Event, Video, Photo (reorderable), and a Settings page. The dashboard should show counts of new bookings and pending guest messages.

## 7. Behaviour and security

- Booking and guest book submissions: server-side validation matching the prototype rules, a honeypot field, rate limiting, and optional Cloudflare Turnstile.
- On a new booking, email the notification address from Settings. Sending an automatic confirmation to the enquirer is a decision for the client; default to yes with plain text.
- Guest messages are never public until approved.
- Escape all output. Audio uploads limited to MP3, with a size cap.
- Collecting names and emails means UK GDPR applies. Add a privacy notice page and a short consent line under both forms before launch. This is not in the prototype.
- YouTube embeds use `youtube-nocookie.com` and load only on the Watch page.

## 8. SEO, accessibility and performance

- Unique title and meta description per page, canonical URL, Open Graph and Twitter tags. Use `images/share.jpg` (logo on dark) as the default share image.
- JSON-LD: Person and MusicGroup with albums on Home and Music; Person on Story; ContactPage on Book. Generate from the database.
- Sitemap and robots generated; the prototype has static examples.
- One `h1` per page. Visible focus states. Skip link. Labels on every form control. Meaningful `alt` text from the Photos table.
- Convert images to WebP with responsive sizes, lazy-load below the fold, set width and height to avoid layout shift. Preload the two fonts. Target Lighthouse 90+ on mobile for performance, accessibility, best practices and SEO.

## 9. Content rules

- Copy is in the prototype. Sources are the old site text and the owner's notes. Do not add claims.
- The old contact details, 2011 launch event, CD prices and store links are deliberately **left out** as out of date.
- Do not state track counts on albums. The old text and track lists disagree (Dreams 11 vs 10 listed, Love Connection 12 vs 11, Treasures 10 vs 11). Show the track lists as supplied.
- Roots is described as "native African language and English". Do not narrow it to Yoruba.
- The photos of a piano, saxophone, violin and drum (`images/bg-*.jpg`) are mood imagery only. Do not caption them as instruments Jide plays. The piano photo shows a small manufacturer name on the fallboard; crop or darken it if the owner does not want it visible.
- The stage stills carry on-screen text from the source video ("T2GB'08"). Replace them when better photos arrive.

## 10. Open items for the client

1. Booking notification email address and the public contact details to show, if any.
2. Reactivating `jidearowolo.com` and pointing it at the host.
3. YouTube: album playlist links or video IDs. The channel is an auto-generated "Topic" channel, so the uploads playlist may not embed. Test early.
4. MP3 samples, if any, named after each track slug.
5. Better source images: Love Connection and So So Wonder covers, a fresh portrait shot on a dark background, and stage photos. Upscaled covers for Dreams, Roots and Treasures are already in `images/`.
6. Streaming links for a "Where to listen" strip.
7. Decision on whether the guest book is public, and who moderates it.
8. Career details. Jide answered the first round of questions (his reply is in `handoff/source/jide-reply.docx`). Applied: Sabena, Maersk Sealand and GNIC signature tunes dated 2000 to 2001; GNIC confirmed as a different organisation from ITC; the Roots Festival CD dated 2001; the State House meeting is 1999 with President Yahya Jammeh; the "Queen in attendance" statement removed. Still open:
   - Spellings of names, unconfirmed: Margurite Ingram (Marguerite?), Debbie Perolls, Kenny Smith, Mary Tade. "Stuttgatt" was corrected to Stuttgart.
   - GNIC: spell out the full name.
   - The CV sentence on the Abiding Word concerts in The Gambia was cut off after 1996 (\"1995, 1996, and\"). The Sierra Leone concert in 2003 is a separate entry.
   - No dates yet for the Shikra hotel post, the Universal Recording Studio, Toronto or Maryland.
   - Permission to name the artists, clients and the president.
   - Not used: the document title "Jay Dee" and the Wikipedia reference (pt.wikipedia.org, Gospel nigeriano), because it is unchecked whether that page mentions Jide.
   - Scans received and used (originals in `images/source/scans/`). Wording now follows the printed covers: "International Roots Homecoming Festival", "Department of State for Tourism & Culture", and the two United Nations tracks "Join hands together" (CD 1, track 9) and "It's our year. It's our time" (CD 2, track 6). The scans show the songs were "donated by artists around the globe", so "contracted" was removed.
   - The back covers carry other organisations' branding (UN Volunteers emblem, a GPTC ferry advert). Confirm Jide is happy to show them, or swap the Roots back scan for a crop of just the credit line.
   - The Roots front scan is cut off at the bottom in the source ("Celebrated in June every year!"). Ask for a fuller scan if possible.
9. Main logo: the client is deciding between the JA monogram (currently in the nav, with a slowly turning sound ring) and the "JIDE AROWOLO" wordmark (currently in the footer). Both are built; swapping is a one-component change.
10. Album order on the home row: newest first (Dreams, Roots, Love Connection, So So Wonder, Treasures) or oldest first, to match the "2001 to 2011" heading.

## 11. Acceptance checklist

- All five pages match the prototype at 390px and 1280px, with no horizontal scroll at 360px.
- Welcome screen shows once per session and can be skipped with keyboard.
- On a phone, the Book Jide bar is visible on all five pages, does not cover the player, footer or welcome screen, and is hidden at 820px and wider.
- The sound ring on both logo marks turns slowly; reduced motion holds it still.
- Track buttons play a sample when one exists and show the fallback message when not; the sound waves speed up during playback.
- Booking submission is stored, visible in the admin, triggers the notification email, and shows a clear success or error message.
- Guest book messages stay hidden until approved.
- Every album, track list, video, photo, event, career entry, place and highlight card is editable in Filament without code changes.
- Sitemap, robots, canonical and structured data present and valid.
- Lighthouse mobile scores at or above 90 in all four categories.

## 12. Files in this package

- `index.html`, `music.html`, `story.html`, `watch.html`, `book.html`: the prototype pages
- `styles.css`, `script.js`: prototype styling and behaviour (settings at the top of `script.js`)
- `logo/`: monogram, wordmark and favicon as SVG, plus PNG exports
- `handoff/source/jide-music-cv.docx`: the music CV Jide supplied, the source for the Story page career content
- `handoff/source/jide-reply.docx`: Jide's answers to the first round of questions
- `handoff/make_logos.py`: regenerates the logo SVGs (needs Python `fonttools` and the npm package `@fontsource/bodoni-moda`; only needed if the logo changes)
- `images/`: cleaned covers and photos, four background images, and the share image
- `handoff/build_prototype.py`: the generator that wrote the pages, including all content and track lists
- `sitemap.xml`, `robots.txt`, `README.md`

## 13. Suggested build order

1. Laravel app, Filament admin, database migrations and seeders. Seed the five albums and track lists from `ALBUMS` in `handoff/build_prototype.py`, and the timeline from the same file.
2. Blade layout, tokens and base components: nav, footer, buttons, cover, page head, equaliser. Match `styles.css`.
3. Public pages in this order: Music, Home, Story, Watch, Book Jide.
4. Welcome screen and motion (see section 4). Reuse `script.js` for the welcome, nav, reveal and player behaviour.
5. Forms, validation, storage, notification email, honeypot and rate limiting. Then guest book moderation.
6. SEO output from the database: meta tags, JSON-LD, sitemap, robots.
7. Image pipeline (WebP, sizes), Lighthouse pass, privacy notice and consent lines.

## 14. Asset inventory

| File | Status |
|---|---|
| `images/jide-dreams.jpg`, `jide-roots.jpg`, `jide-treasures.jpg` | Client-supplied upscales, cleaned. Final. |
| `images/jide-love-connection.jpg`, `jide-so-so-wonder.jpg` | 3x upscales of small thumbnails from the old site. Soft. Replace when better scans arrive. |
| `images/jide-hero-stool.webp`, `jide-hero-close.webp` | Home header photos supplied by the client (Nov 2026), cut out from white. Stool (full body) shows from 820px up, close-up below. Originals in `images/source/`. |
| `images/jide-portrait.webp` | Sharper client-supplied portrait, cut out from its white background with sloped shoulders and a warmed collar. Original in `images/source/jide-portrait-original.jpg`. A fresh shot on a dark background would still be better. |
| `images/jide-stage.jpg`, `jide-guitar.jpg` | Video stills with burned-in "T2GB'08" text. Replace. |
| `images/jide-studio.jpg` | Acceptable. |
| `images/bg-*.jpg` | Mood photography supplied by the client from another project. Piano shows a small manufacturer name. |
| `images/archive/*.webp` | Cleaned scans of the Roots theme song CD and the International Year of Volunteers 2001 album (cropped, straightened, auto-levelled). Originals in `images/source/scans/`. Roots front is cut off at the bottom in the source. |
| `images/share.jpg` | Generated share image (logo on dark). |
| `logo/*` | Designed for this project. Lettering is Bodoni Moda converted to outlines. |
| `audio/` | Empty. MP3 samples are optional. |

## 15. Not done in the prototype

- Forms do not send anything (`FORM_ENDPOINT` is empty).
- The YouTube embed uses the channel's uploads playlist. It has not been tested on a live host, and a "Topic" channel may not allow embedding.
- No privacy notice or consent lines.
- No events. The empty state is built but there is no events section on the page yet.
- No audio samples.
