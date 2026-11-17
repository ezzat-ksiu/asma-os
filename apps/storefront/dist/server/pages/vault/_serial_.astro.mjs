import { e as createComponent, k as renderComponent, r as renderTemplate, h as createAstro, m as maybeRenderHead } from '../../chunks/astro/server_DWnod6f9.mjs';
import 'piccolore';
import { $ as $$SiteLayout } from '../../chunks/SiteLayout_CDwskgjt.mjs';
export { renderers } from '../../renderers.mjs';

const $$Astro = createAstro();
const prerender = false;
const $$serial = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$serial;
  const serial = Astro2.params.serial ?? "";
  let issue = "Vault record is unavailable. Please try again later.";
  return renderTemplate`${renderComponent($$result, "SiteLayout", $$SiteLayout, { "title": `Edition ${serial} | ASMA-OS Vault` }, { "default": async ($$result2) => renderTemplate` ${maybeRenderHead()}<main class="shell" style="padding:70px 0;max-width:850px"><a href="/" style="color:#7bd9e3">← ASMA-OS</a><p style="color:#35c6d8;text-transform:uppercase;letter-spacing:.16em;font-size:12px;margin-top:52px">Public edition vault</p><h1 style="font-size:44px;margin:12px 0 32px">Edition ${serial}</h1> ${renderTemplate`<section style="padding:24px;border:1px solid #27384e;border-radius:10px;background:#0d1a2b;color:#a7b5c8"><p>${issue}</p>${renderTemplate`<p>Public vault API is not configured for this deployment.</p>`}</section>`} </main> ` })}`;
}, "C:/Users/Giagbyte dell/OneDrive - King Salman International University/Desktop/asma-os/apps/storefront/src/pages/vault/[serial].astro", void 0);
const $$file = "C:/Users/Giagbyte dell/OneDrive - King Salman International University/Desktop/asma-os/apps/storefront/src/pages/vault/[serial].astro";
const $$url = "/vault/[serial]";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$serial,
  file: $$file,
  prerender,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
