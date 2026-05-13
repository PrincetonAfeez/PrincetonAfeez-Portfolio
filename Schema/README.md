# Schema Folder

This folder contains simple JSON-LD schema files for the Princeton Afeez portfolio website.

## Files

- `person.schema.json` — describes the portfolio owner.
- `website.schema.json` — describes the website.
- `portfolio-page.schema.json` — describes the portfolio/profile page.
- `breadcrumb.schema.json` — describes the home breadcrumb.
- `combined-schema.json` — combines all schema objects into one JSON-LD graph.

## How to use

Use `combined-schema.json` if you want one schema block on your portfolio page.

Add it to your HTML inside a `<script type="application/ld+json">` tag:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": []
}
</script>
```

Replace the empty `@graph` array with the content from `combined-schema.json`.

## Update before publishing

Check these values and edit them if needed:

- Website URL
- Job title
- Description
- Social/profile links
- Project-specific links
