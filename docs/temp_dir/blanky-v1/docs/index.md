# blanky v1 — jQuery plugin

This is the documentation for blanky **v1**, the classic jQuery plugin.

For the current version (v2: dependency-free ESM core + UMD + optional jQuery
layer), see [blanky v2](https://aldo-f.github.io/blanky/docs/).

## Install

Include after jQuery:

```html
<script src="jquery.min.js"></script>
<script src="blanky.js"></script>
```

Or `npm install blanky@1`.

## Usage

```js
// defaults
$("body").blanky({
    blank: true,      // add target="_blank" to external links
    noopener: true,   // merge rel="noopener" into external links
    nofollow: false,  // add rel="nofollow" to internal links
    debug: false      // log classification decisions to the console
});

$("#content").blanky(); // scoped: only links inside #content
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

Source: [gitlab.com/Aldo-f/blanky](https://gitlab.com/Aldo-f/blanky) (tag `v1.0.0`).
