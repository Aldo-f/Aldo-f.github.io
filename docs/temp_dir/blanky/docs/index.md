# blanky

A tiny, dependency-free library that opens **external** links in a new window —
safely and correctly. Ships as an ESM module, a UMD bundle and an optional
jQuery plugin layer.

## Usage

### ESM / bundlers

```js
import { blanky } from 'blanky';

const rescan = blanky({ blank: true, noopener: true, nofollow: false, debug: false });
// rescan() re-processes the page — call it after dynamically adding content.
```

### Global script (UMD)

```html
<script src="dist/blanky.umd.js"></script>
<script>
  window.blanky.blanky(); // processes the whole document
</script>
```

### jQuery (v1-compatible API)

```js
import 'blanky/jquery'; // or include blanky.js after jQuery

$("body").blanky({
    blank: true,      // add target="_blank" to external links
    noopener: true,   // merge rel="noopener" into external links
    nofollow: false,  // add rel="nofollow" to internal links
    debug: false      // log classification decisions to the console
});
```

### What counts as "external"?

| Link | Treated as |
|---|---|
| `https://example.com` | external |
| `//example.com/page` | external |
| `https://evil.test?ref=https://yoursite` | external |
| `/about`, `page.html`, `#section` | internal |
| `https://yoursite.com/page` | internal |

External links get `target="_blank"`. Existing `rel` tokens are preserved and
merged with (never overwritten by) `noopener`. Internal links are left untouched
unless you opt in to `nofollow`.

## API

- `blanky(options?, root?)` → scan function; call repeatedly for dynamic DOM.
- `classifyLink(element, origin, options)` → classify one anchor.
- `mergeRel(element, token, enabled)` → merge a `rel` token.

## Development

```bash
npm install
npm test       # Vitest + jsdom (core, jQuery adapter, UMD build)
npm run build  # regenerate dist/blanky.umd.js from src/
```

Source & contributing: [gitlab.com/Aldo-f/blanky](https://gitlab.com/Aldo-f/blanky).
