# Jide Arowolo website (prototype)

A five-page static prototype: Home, Music, Story, Watch and Book Jide. Open `index.html` in a browser, or upload the folder to any web host. The pages need an internet connection for the Google Fonts and the YouTube embed.

## For the developer
Start with `handoff/BRIEF.md`. It covers the design system, motion, page details, data model, Filament admin, security, SEO, open items, suggested build order and an asset inventory. The stack is Laravel + Filament.

## Folder
- `index.html`, `music.html`, `story.html`, `watch.html`, `book.html`: the pages
- `styles.css`, `script.js`: styling and behaviour (settings at the top of `script.js`)
- `images/`: covers, photos and the share image
- `logo/`: JA monogram, wordmark and favicon (SVG, with PNG exports)
- `audio/`: optional MP3 samples
- `handoff/`: the brief, the page generator and the logo generator

## Settings (top of `script.js`)
- `YOUTUBE_PLAYLIST_ID` or `YOUTUBE_VIDEO_IDS`: what the Watch page embeds
- `FORM_ENDPOINT`: a form service address so booking and guest book messages reach you (empty means preview only)
- Track samples: add MP3s to `audio/`, named after the track, e.g. `audio/ololufe.mp3`

## Editing the prototype
- Page text lives in `handoff/build_prototype.py`. Edit it and run `python3 handoff/build_prototype.py` to regenerate the pages (it writes into the folder above `handoff/`), or edit the HTML directly.
- Replace `https://www.jidearowolo.com/` in the pages if the address differs.
