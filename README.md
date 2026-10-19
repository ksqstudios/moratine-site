# moratine.app

Static HTML and CSS, deployed via Cloudflare Pages with GitHub auto-deploy.

## Structure

```
.
├── index.html         marketing page
├── privacy.html       privacy policy, linked from the app's About screen
├── support.html       support page and FAQ
├── styles.css         shared stylesheet
├── _headers           Cloudflare Pages cache and security headers
├── robots.txt
├── sitemap.xml
└── images/            screenshots
```

## Fonts

Overpass is the only typeface, loaded from Google Fonts in each page head
(weights 400, 600 and 800). It comes from the Highway Gothic signage
lineage, which suits a site built as a waiting room: a take-a-number ticket,
a ledger like a posted fee schedule, and a posted notice.

## Assets to drop in

| File | Size | Notes |
|---|---|---|
| `images/01.png` | ~600x1300 | Home, ledger |
| `images/02.png` | ~600x1300 | A wait running |
| `images/03.png` | ~600x1300 | Attribution sheet |
| `images/04.png` | ~600x1300 | Counterparty detail |
| `images/05.png` | ~600x1300 | History |
| `images/07.png` | ~600x1300 | Control Center |
| `images/w1.png` | ~410x502 | Watch, at rest |
| `images/w2.png` | ~410x502 | Watch face complication |
| `images/w3.png` | ~410x502 | Watch Smart Stack |
| `og-image.png` | 1200x630 | Open Graph preview, from make_og.py |
| `favicon.png` | 32x32 | |
| `apple-touch-icon.png` | 180x180 | Also used as the masthead mark |

Use the frameless captures for `images/`, not the App Store composites: the
site adds its own rounded corners and shadow, and the captions would be
duplicated.

## Deployment

Cloudflare Pages, connected to this repo. Build command: none. Output
directory: `/`. Deploys on push to `main`.

Custom domain `moratine.app` set in Cloudflare Pages, Custom domains.

Cloudflare serves `.html` at the path-stripped URL, so `/privacy` and
`/support` work without the extension. The app's About screen links to both,
and App Store Connect points at them.

## Before launch

The two App Store links in `index.html` are `href="#"` placeholders. Replace
both with the real product URL once the app is approved.

## Analytics

None. The privacy policy says the site collects nothing, so keep it that way.
