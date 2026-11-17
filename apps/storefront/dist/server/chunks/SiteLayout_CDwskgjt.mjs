import { e as createComponent, l as renderHead, n as renderSlot, r as renderTemplate, h as createAstro } from './astro/server_DWnod6f9.mjs';
import 'piccolore';
import 'clsx';
/* empty css                         */

const $$Astro = createAstro();
const $$SiteLayout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$SiteLayout;
  const { title = "ASMA-OS | Stories with provenance" } = Astro2.props;
  return renderTemplate`<html lang="en"> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="theme-color" content="#091321"><title>${title}</title>${renderHead()}</head> <body>${renderSlot($$result, $$slots["default"])}</body></html>`;
}, "C:/Users/Giagbyte dell/OneDrive - King Salman International University/Desktop/asma-os/apps/storefront/src/layouts/SiteLayout.astro", void 0);

export { $$SiteLayout as $ };
