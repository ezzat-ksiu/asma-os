import { e as createComponent, h as createAstro } from '../chunks/astro/server_DWnod6f9.mjs';
import 'piccolore';
import 'clsx';
export { renderers } from '../renderers.mjs';

const $$Astro = createAstro();
const prerender = false;
const $$Index = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Index;
  const serial = Astro2.url.searchParams.get("serial")?.trim();
  if (!serial) return Astro2.redirect("/#provenance", 302);
  return Astro2.redirect(`/vault/${encodeURIComponent(serial)}`, 302);
}, "C:/Users/Giagbyte dell/OneDrive - King Salman International University/Desktop/asma-os/apps/storefront/src/pages/vault/index.astro", void 0);

const $$file = "C:/Users/Giagbyte dell/OneDrive - King Salman International University/Desktop/asma-os/apps/storefront/src/pages/vault/index.astro";
const $$url = "/vault";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
	__proto__: null,
	default: $$Index,
	file: $$file,
	prerender,
	url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
