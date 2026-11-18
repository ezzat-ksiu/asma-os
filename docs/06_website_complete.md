# FOLIAVERE — Complete Storefront, Vault, Trust Centre and Customer Journey

ملخص تنفيذي 1: بنية الموقع مقسمة إلى متجر عام ومركز ثقة وخزنة رقمية وشاشة مؤسس خاصة.
ملخص تنفيذي 2: النصوص متاحة بالإنجليزية والعربية، مع بنية قابلة لإضافة الفرنسية بعد مراجعة الترجمة.
ملخص تنفيذي 3: النسخة الأولى لا تطلب صور أطفال ولا تنشئ قياسات حيوية؛ تعتمد على بيانات يقدّمها ولي الأمر وسمات شخصية اختيارية.
ملخص تنفيذي 4: صفحات الخصوصية والشروط والاسترجاع مسودات تشغيلية ولا تُنشر كوثائق قانونية نهائية قبل مراجعة مختص.
ملخص تنفيذي 5: لا يعد الموقع بمدة توصيل أو حذف أو جودة أو توافر إلا بعد إثبات تشغيلي موثق.

## 1. Information architecture

| Route | Purpose | Main audience | Indexing |
|---|---|---|---|
| `/en` and `/ar` | Home and positioning | B2C and B2B | Index |
| `/en/editions/heirloom` | Entry edition | Families | Index |
| `/en/editions/atelier` | Enhanced edition | Families / gift buyers | Index |
| `/en/editions/grand` | Highest-scope edition | Adult / family / B2B enquiry | Index |
| `/en/how-it-works` | Workflow and approval boundaries | All buyers | Index |
| `/en/trust` | Privacy, AI disclosure and production controls | Parents / institutions | Index |
| `/vault/{serial}` | Public edition verification | Book recipient | Index only with public-record consent; otherwise `noindex` |
| `/en/checkout` | Order and payment | Buyer | `noindex` |
| `/en/for-hospitality` | B2B offer | Hotel operators | Index |
| `/en/about` | Editorial philosophy and operating model | All buyers | Index |
| `/en/faq` | Questions / support | All buyers | Index |
| `/legal/privacy` | Privacy notice draft | All | Index after legal review |
| `/legal/terms` | Terms draft | All | Index after legal review |
| `/legal/refunds` | Cancellation / correction / returns | All | Index after legal review |
| `/legal/shipping` | Shipping scope and import charges | All | Index after legal review |

Each language route uses a real translated page, not an automatically spun translation page. Canonical tags, `hreflang`, titles, descriptions, structured data and Open Graph metadata must be language-specific. All customer-facing copy is authored and reviewed; a generated page is not publishable merely because it validates as HTML.

## 2. Homepage copy

### English

**Eyebrow:** FOLIAVERE — BESPOKE PUBLISHING

**Headline:** A story worth holding on to.

**Subheadline:** Thoughtfully directed books made from the memories, ideas and imaginative briefs you choose to share. Each commission is edited, proofed and prepared as a physical edition with a clear record of what was made.

**Primary CTA:** Explore the editions

**Secondary CTA:** See the sample collection

**Trust line:** Your brief stays private. Public verification is optional. No child likeness is used in our public marketing.

### العربية

**العنوان التمهيدي:** فولياڤير — دار نشر مخصصة

**العنوان الرئيسي:** حكاية تستحق أن تبقى بين يديك.

**النص:** نصمم كتباً مطبوعة بعناية انطلاقاً من الذكريات والأفكار والحكايات التي تختار مشاركتها. تمر كل نسخة بالمراجعة واعتماد النسخة النهائية قبل تجهيزها للطباعة، مع سجل واضح لما تم إنتاجه.

**الزر الأساسي:** اكتشف الإصدارات

**الزر الثانوي:** شاهد مجموعة النماذج

**سطر الثقة:** تُعامل تفاصيل طلبك بسرية. نشر صفحة تحقق عامة اختياري. لا نستخدم صور الأطفال الشخصية في التسويق العام.

## 3. Product pages — exact tier scope

### Heirloom — USD 199

**EN headline:** A personal story, made tangible.

A guided 32-page illustrated edition for one clear idea, dedication or family-friendly story brief. Includes a digital proof, one consolidated correction round, a standard hardcover specification selected from the approved printer catalogue, an edition certificate and tracked fulfilment when the supplier offers tracking.

**EN CTA:** Begin an Heirloom edition

**AR headline:** حكاية شخصية في كتاب ملموس.

إصدار مصور من 32 صفحة لفكرة أو إهداء أو حكاية عائلية محددة. يشمل معاينة رقمية، وجولة واحدة مجمعة للتصحيح، ومواصفة غلاف مقوى من المنتجات التي تم اختبارها، وشهادة إصدار، وتتبع الشحنة عند توفره من المورّد.

**AR CTA:** ابدأ إصدار هيرلوم

### Atelier — USD 399

**EN headline:** More room for the details that matter.

A 32-page edition with expanded editorial direction, a richer illustration plan, a longer dedication or family context, enhanced proof review and a more considered print finish where the selected supplier supports it. The exact paper and finish are shown before payment.

**EN CTA:** Explore Atelier

**AR headline:** مساحة أكبر للتفاصيل التي تصنع الفرق.

إصدار من 32 صفحة بتوجيه تحريري أوسع، وخطة رسوم أغنى، وسياق عائلي أو إهداء أكثر تفصيلاً، ومراجعة معاينة موسعة، وتشطيب مطبعي محسّن عند دعمه من المورّد المختار. نعرض مواصفات الورق والتشطيب قبل الدفع.

**AR CTA:** اكتشف أتيليه

### Grand — USD 649

**EN headline:** A considered edition for an important story.

The most comprehensive 32-page scope: deeper editorial planning, a premium illustration plan, two consolidated proof rounds, a provenance record and priority exception handling. Any rigid gift box, metallic foil, additional copies or extended manuscript is priced separately against a live quote.

**EN CTA:** Request a Grand edition

**AR headline:** إصدار متكامل لحكاية مهمة.

النطاق الأكثر شمولاً ضمن منتج 32 صفحة: تخطيط تحريري أعمق، وخطة رسوم مميزة، وجولتا تصحيح مجمعتان، وسجل توثيق للإصدار، ومعالجة ذات أولوية للاستثناءات. تُسعّر العلبة الصلبة أو الطباعة المعدنية أو النسخ الإضافية أو المخطوط الأطول بشكل منفصل وفق عرض سعر حي.

**AR CTA:** اطلب إصدار جراند

**Pricing boundary:** USD list prices are working price points. Taxes, FX, cross-border delivery, customs and payment fees may alter the checkout total. The customer sees the final payable amount and destination before authorising payment. No tier is sold with unquoted finishing options.

## 4. How it works

### English steps

1. **Choose the edition.** Select the audience, language and scope. The first release supports adult-directed commissioning; children do not create accounts or submit personal details.
2. **Share a brief.** Provide the names and story facts required for the commission. Do not upload a child's photograph in the initial release.
3. **Review the direction.** ASMA-OS prepares the structured specification, outline and sample pages. Unsupported claims and unsafe content are blocked.
4. **Approve the proof.** Review names, text, page sequence and selected images. Printing is blocked until the final file hash is approved by the founder and the customer's proof approval is recorded.
5. **Print and track.** A verified payment and live supplier quote are required before a print order is submitted.
6. **Keep the record.** Receive the edition certificate and optional private audio or vault link if those features are enabled for the order.

### الخطوات بالعربية

1. **اختر الإصدار.** حدد الجمهور واللغة والنطاق. في الإطلاق الأول يكون إنشاء الطلب بإشراف شخص بالغ، ولا ينشئ الأطفال حسابات أو يرسلون بياناتهم بأنفسهم.
2. **شارك موجز الحكاية.** أدخل الأسماء والحقائق الضرورية فقط. لا ترفع صورة طفل في النسخة الأولى من الخدمة.
3. **راجع التوجه الإبداعي.** يُعد ASMA-OS المواصفة والمخطط والصفحات التجريبية، مع إيقاف المحتوى غير الآمن أو الادعاءات غير المدعومة.
4. **اعتمد المعاينة.** راجع الأسماء والنص وترتيب الصفحات والرسوم. لا تبدأ الطباعة قبل اعتماد ملفه النهائي ببصمته الرقمية وتسجيل موافقة العميل على المعاينة.
5. **الطباعة والتتبع.** يتطلب إرسال الطلب إلى المطبعة تأكيد الدفع ووجود عرض سعر حي.
6. **احتفظ بسجل الإصدار.** تستلم شهادة الإصدار ورابطاً صوتياً أو صفحة خزنة خاصة عند تفعيلها لهذا الطلب.

## 5. Trust and privacy centre

### English trust page

**Headline:** Personal stories deserve careful handling.

We collect only the information needed to scope, produce, deliver and support a commissioned book. The customer is the adult commissioning party. The initial release does not ask children to create accounts, does not accept child photographs, and does not create face embeddings or child LoRA models.

A future photo-personalisation feature will remain disabled until the company has verified an appropriate legal basis, parental authority, provider contracts, data-transfer safeguards, deletion controls, security testing and a documented impact assessment where required. A policy statement alone is not proof that deletion has occurred.

Public vault pages are optional. They show only the edition reference and metadata expressly approved for public release. They never display a child's face, private manuscript, home address or contact details.

**AI disclosure:** AI tools may assist with drafting, illustration and layout. A human-directed editorial process selects and arranges the final content. Do not assume that all AI-generated elements receive copyright protection.

### صفحة الثقة والخصوصية بالعربية

**العنوان:** الحكايات الشخصية تستحق عناية حقيقية.

نجمع المعلومات الضرورية فقط لتحديد نطاق الكتاب وإنتاجه وتسليمه ودعم الطلب. العميل هو الشخص البالغ الذي يطلب الإصدار. لا تطلب النسخة الأولى حساباً من الطفل، ولا تقبل صور الأطفال، ولا تنشئ تمثيلات رقمية للوجه أو نماذج LoRA للأطفال.

تبقى أي خاصية مستقبلية لتخصيص الصور معطلة إلى أن يتم التحقق من الأساس القانوني المناسب، وسلطة ولي الأمر، وعقود المزوّدين، وضوابط نقل البيانات، والحذف، والاختبارات الأمنية، وتقييم الأثر عند لزومه. وجود سياسة مكتوبة لا يثبت وحده أن الحذف قد تم بالفعل.

صفحة الخزنة العامة اختيارية، ولا تعرض إلا رقم الإصدار والبيانات التي وافق العميل صراحةً على نشرها. ولا تعرض وجه طفل أو المخطوط الخاص أو عنوان المنزل أو بيانات الاتصال.

**الإفصاح عن الذكاء الاصطناعي:** قد تساعد أدوات الذكاء الاصطناعي في المسودة والرسم والتنسيق، بينما تتم عملية الاختيار والترتيب التحريري النهائي بتوجيه بشري. ولا يعني ذلك أن كل عنصر مولد بالذكاء الاصطناعي يتمتع تلقائياً بحماية حقوق النشر.

## 6. Vault page `/vault/{serial}`

### Public state — English

**FOLIAVERE EDITION RECORD**

Edition reference: `AS-XXXXXXXX`

Status: `Record verified` or `Record not found`

This page confirms that the edition reference exists in the public register. It does not certify copyright ownership, authorship exclusivity, materials, delivery or legal registration. Private customer details and source files are not displayed.

### Public state — العربية

**سجل إصدار فولياڤير**

رقم الإصدار: `AS-XXXXXXXX`

الحالة: `تم التحقق من السجل` أو `السجل غير موجود`

تؤكد الصفحة وجود رقم الإصدار في السجل العام فقط. ولا تمثل شهادة ملكية حقوق النشر أو حصرية التأليف أو مواصفات المواد أو التسليم أو التسجيل القانوني. لا تظهر بيانات العميل الخاصة أو ملفات المصدر.

**Implementation rules:** serials are random and non-sequential; access is rate-limited; public metadata is a separate allowlisted projection; private records are never queried into a public template. Use `noindex` by default until customer-publication permission is recorded. A serial alone must not grant access to the private book PDF or audio.

## 7. Checkout and order flow

1. The buyer selects a tier, destination country, language and approved options.
2. Backend computes the price from Decimal values and retrieves a destination-specific POD quote. No fixed worldwide shipping estimate is inserted as fact.
3. The checkout displays taxes, import charges collected at checkout where applicable, any excluded border charges, revision policy, personalised-goods notice and estimated delivery range supplied by the vendor.
4. Customer accepts the terms and pays through the configured merchant's hosted payment page.
5. Payment status is trusted only after the provider callback signature is checked using that provider's documented algorithm and the event is stored under a unique provider-event key.
6. Order enters `paid_pending_proof`; it does not automatically enter print dispatch.
7. Customer approves the proof; the founder approves the exact print artifact hash and exact supplier quote.
8. The print adapter submits the order. Tracking updates are written to the order timeline.

### Checkout reassurance copy — EN

“Your order will not be sent to print merely because payment succeeds. We prepare a proof, show you the final names and pages, and require the approvals defined for your edition before the print order is submitted.”

### نص الطمأنة في الدفع — AR

«لن يُرسل طلبك إلى الطباعة لمجرد نجاح الدفع. نجهز معاينة، ونعرض الأسماء والصفحات النهائية، ونستكمل الموافقات المحددة لإصدارك قبل إرسال أمر الطباعة».

## 8. B2B hospitality page

### English

**Headline:** Turn a place into a story guests can take home.

FOLIAVERE develops short-run, brand-directed books for hospitality teams: property stories, local culture, architecture, service rituals and curated guest experiences. We begin with a paid five-copy micro-pilot using fictional or institution-approved material. The pilot measures editorial approval, print quality, delivery reliability and recipient feedback before a larger programme is proposed.

**Pilot scope:** five identical or individually addressed copies; one defined audience; one approved language; agreed content-rights schedule; one proof cycle; live print and shipping quote; delivery evidence; post-delivery feedback report.

**Pilot price:** USD 1,500 planning price for the initial five-copy editorial pilot, excluding taxes, extraordinary travel, licensed third-party assets and any custom rigid box. Final proposal depends on scope and live fulfilment quote.

**CTA:** Request a hospitality pilot

### العربية

**العنوان:** حوّل المكان إلى حكاية يأخذها الضيف معه.

تطور فولياڤير كتباً محدودة العدد تقودها هوية المنشأة: قصة المكان، والثقافة المحلية، والعمارة، وطقوس الخدمة، وتجربة الضيف. نبدأ بتجربة مدفوعة من خمس نسخ باستخدام محتوى خيالي أو معتمد من المؤسسة. نقيس اعتماد النص وجودة الطباعة وموثوقية التسليم وتقييم المتلقين قبل اقتراح برنامج أوسع.

**نطاق التجربة:** خمس نسخ متطابقة أو موجهة لأسماء مختلفة، وجمهور محدد، ولغة معتمدة، وجدول واضح لحقوق المحتوى، ودورة معاينة واحدة، وعرض سعر حي للطباعة والشحن، وإثبات تسليم، وتقرير ملاحظات بعد التسليم.

**السعر التخطيطي للتجربة:** 1,500 دولار أمريكي لخمس نسخ، قبل الضرائب والسفر الاستثنائي والأصول الخارجية المرخصة والعلبة الصلبة المخصصة. يتحدد العرض النهائي وفق النطاق وعرض تنفيذ الطلب الحي.

**الزر:** اطلب تجربة للضيافة

## 9. About page

**EN:** FOLIAVERE is an independent bespoke-publishing concept built around careful editorial direction, measured technology and physical production. ASMA-OS is the internal operating system—not a separate consumer product. Our method is evidence-gated: a book progresses only when its brief, proof, costs, payment, privacy controls and approvals are recorded.

**AR:** فولياڤير مشروع نشر مخصص يقوم على التوجيه التحريري الدقيق، والتقنية المنضبطة، والإنتاج المطبوع. ASMA-OS هو نظام التشغيل الداخلي للدار وليس منتجاً مستقلاً للمستهلك. تعتمد طريقتنا على الأدلة: لا ينتقل الكتاب إلى المرحلة التالية إلا بعد تسجيل الموجز والمعاينة والتكاليف والدفع وضوابط الخصوصية والموافقات المطلوبة.

## 10. FAQ — bilingual answers

| Question (EN) | Answer (EN) | السؤال (AR) | الإجابة (AR) |
|---|---|---|---|
| Is every book completely unique? | Each commissioned edition is scoped to its buyer. Generic layouts, fonts, production methods and non-identifying components may be reused; we do not promise that every word or visual technique has never appeared elsewhere. | هل كل كتاب فريد بالكامل؟ | يُحدد كل إصدار وفق طلب العميل. قد نعيد استخدام التخطيطات العامة والخطوط وطرق الإنتاج والعناصر غير التعريفية؛ ولا نعد بأن كل كلمة أو أسلوب بصري لم يظهر في أي مكان سابقاً. |
| Can I upload a child's photo? | Not in the initial release. The first product uses text-led personalisation and fictional illustration. | هل يمكن رفع صورة طفل؟ | ليس في الإطلاق الأول. يعتمد المنتج الأول على التخصيص النصي والرسوم الخيالية. |
| Is the book educational therapy? | No. A story may include a stated discussion theme, but it is not therapy, diagnosis or a guaranteed developmental intervention. | هل الكتاب علاج أو برنامج علاجي؟ | لا. قد تتضمن القصة محوراً للنقاش، لكنها ليست علاجاً أو تشخيصاً أو تدخلاً نمائياً مضمون النتائج. |
| When will it arrive? | The checkout shows the vendor's current production and shipping estimate for your destination. It is an estimate, not a universal guarantee. | متى يصل الكتاب؟ | يعرض الدفع تقدير الإنتاج والشحن الحالي من المورّد لوجهتك. وهو تقدير وليس ضماناً موحداً لجميع الدول. |
| Can I cancel? | Cancellation eligibility depends on the stage of a personalised order and applicable consumer law. Contact support immediately; the published policy controls. | هل يمكن إلغاء الطلب؟ | تعتمد إمكانية الإلغاء على مرحلة الطلب المخصص والقانون الاستهلاكي المنطبق. تواصل مع الدعم فوراً، وتطبق السياسة المنشورة بعد مراجعتها قانونياً. |
| Do you own the copyright? | We do not claim ownership of all AI-assisted output. The customer receives the licence stated in the order; third-party materials remain subject to their own licences. | هل تمتلك الدار حقوق النشر؟ | لا تدعي الدار امتلاك حقوق كل مخرجات الذكاء الاصطناعي. يحصل العميل على الترخيص المحدد في الطلب، وتظل المواد الخارجية خاضعة لتراخيصها. |
| Is the vault public? | Public display is optional and limited to approved, redacted metadata. | هل الخزنة عامة؟ | النشر العام اختياري ومحدود بالبيانات المنقحة التي وافق العميل على نشرها. |
| Can a hotel order multiple editions? | Yes, after a scoped paid pilot and confirmed licensing, supplier capacity and delivery quote. | هل يستطيع الفندق طلب نسخ متعددة؟ | نعم، بعد تجربة مدفوعة محددة والتحقق من الترخيص وقدرة المورّد وعرض التسليم. |

## 11. Email addresses and transactional templates

Create these mailbox names only after the domain is legitimately registered and the mail provider is configured. They are exact address choices, not claims that mailboxes currently exist:

- `hello@foliavere.com` — general enquiries
- `support@foliavere.com` — order support
- `privacy@foliavere.com` — privacy requests
- `b2b@foliavere.com` — institutional enquiries
- `press@foliavere.com` — media enquiries
- `billing@foliavere.com` — receipts and payment questions

### Order confirmation — EN

**Subject:** We have received your FOLIAVERE order

Thank you for commissioning an edition. Your payment status is being verified by the payment provider. We will prepare your proof after the order is confirmed. Your order is not yet in print production. Please keep your order reference for support.

### تأكيد الطلب — AR

**الموضوع:** استلمنا طلب إصدارك من فولياڤير

شكراً لطلب إصدارك. نتحقق من حالة الدفع لدى مزود الخدمة. بعد تأكيد الطلب نجهز المعاينة لإرسالها إليك. لم يدخل طلبك مرحلة الطباعة بعد. احتفظ برقم الطلب عند التواصل مع الدعم.

### Shipping notification — EN

**Subject:** Your FOLIAVERE edition has shipped

The print provider has marked your order as shipped. Your tracking reference and carrier link are shown below when available. Carrier scans can take time to appear; the tracking page is the current source for movement updates.

### إشعار الشحن — AR

**الموضوع:** تم شحن إصدارك من فولياڤير

أفاد مزود الطباعة بأن طلبك شُحن. يظهر رقم التتبع ورابط شركة النقل أدناه عند توفرهما. قد يتأخر ظهور أول تحديث في نظام شركة النقل؛ وتبقى صفحة التتبع هي المصدر الحالي لحركة الشحنة.

### Delivery follow-up — EN

**Subject:** Has your edition arrived safely?

The carrier reports delivery. Please inspect the parcel and book. If the parcel is damaged or the book differs from the approved proof, reply with the order reference and a short description. We will review the evidence under the correction and reprint policy.

### متابعة التسليم — AR

**الموضوع:** هل وصل إصدارك بأمان؟

يفيد نظام شركة النقل بإتمام التسليم. يرجى فحص الطرد والكتاب. إذا وصل الطرد متضرراً أو اختلف الكتاب عن المعاينة المعتمدة، أرسل رقم الطلب ووصفاً مختصراً للمشكلة. سنراجع الحالة وفق سياسة التصحيح وإعادة الطباعة.

### Feedback request — EN

**Subject:** Tell us how the edition worked for you

Your feedback helps us improve proofreading, production and delivery. Please rate the physical quality and the accuracy of the approved names and text. Your feedback is not published publicly unless you separately agree to publication.

### طلب التقييم — AR

**الموضوع:** شاركنا رأيك في الإصدار

تساعدنا ملاحظاتك على تحسين التدقيق والإنتاج والتسليم. نرجو تقييم جودة النسخة المطبوعة ودقة الأسماء والنص المعتمد. لا ننشر رأيك علناً إلا إذا وافقت بصورة منفصلة على النشر.

## 12. Legal page drafts — not publishable until reviewed

### Privacy notice — operational draft

FOLIAVERE processes information supplied by the adult commissioning customer to assess a request, create the agreed manuscript and artwork, collect payment, coordinate printing and delivery, respond to support requests, and meet applicable recordkeeping obligations. The specific data controller, registered address, lawful bases, processor list, transfer mechanisms, retention schedule and supervisory authority details must be added only after the operating entity and counsel have verified them. Do not publish this draft as a legally complete notice until those facts are established.

We do not request children's direct sign-up in the initial release. Child photographs, face embeddings and child-specific LoRA weights are not accepted in the initial release. Marketing consent is separate from order fulfilment. Public vault publication is optional and requires a distinct approval of the exact public metadata.

### إشعار الخصوصية — مسودة تشغيلية

تعالج فولياڤير المعلومات التي يقدمها العميل البالغ لتقييم الطلب وإنشاء المخطوط والرسوم المتفق عليها وتحصيل الدفع وتنسيق الطباعة والتسليم والرد على الدعم والوفاء بالتزامات حفظ السجلات المنطبقة. يجب تحديد جهة التحكم في البيانات وعنوانها وأسس المعالجة وقائمة المعالجين وآليات النقل ومدة الاحتفاظ والجهة الرقابية بعد التحقق من الكيان التشغيلي ومراجعة المختص. لا تُنشر هذه المسودة باعتبارها إشعاراً قانونياً مكتملاً قبل تثبيت تلك الوقائع.

لا نطلب تسجيل الأطفال مباشرة في الإطلاق الأول. ولا نقبل صور الأطفال أو تمثيلات الوجه الرقمية أو أوزان LoRA الخاصة بالأطفال في الإطلاق الأول. موافقة التسويق منفصلة عن تنفيذ الطلب، ونشر صفحة الخزنة العامة اختياري ويتطلب اعتماداً مستقلاً للبيانات العامة المحددة.

### Terms — operational draft

The order describes the edition scope, page count, language, options, proof rounds, price, destination, supplier specification and any third-party licences. The customer confirms that they have authority to provide all text, names, photographs and other materials included in the commission. FOLIAVERE may decline content that violates safety rules, third-party rights or applicable law. AI may assist parts of production; the customer is not promised copyright in elements that are not protectable under applicable law. The customer receives the personal perpetual licence stated on the order confirmation; the licence does not grant ownership of fonts, stock assets, model weights, provider tools or reusable generic layouts.

### Refunds, correction and cancellation — operational draft

Before work starts, cancellation is handled under applicable law and the payment provider's status. Once personalised work has begun, any deduction or limit must be disclosed before purchase and must comply with applicable consumer law. After proof approval, the customer is responsible for errors that were visible and clearly presented in the proof, subject to non-excludable statutory rights. A production defect, damage in transit or material mismatch with the approved proof is reviewed for correction, replacement or refund as required by law and the order policy. Never state that all personalised goods are universally non-refundable; legal rules differ by jurisdiction and by whether the purchase is a physical personalised good, digital content or service.

### Shipping and customs — operational draft

Shipping estimates are supplied from the selected print provider and destination. A local production partner is not guaranteed for every SKU or country. Customs duties, import VAT, brokerage, postal handling charges and delivery attempts may be payable by the customer if they are not collected at checkout. The checkout must show which charges are included and which may be collected at the border. Lost or damaged orders are investigated with the carrier and print provider before a remedy is offered.

## 13. Everything forgotten — operating details

- Publish a customer-facing support-hours statement only after the founder's real availability is defined.
- Provide a support form that asks for order reference, not a child name or image.
- Set SPF, DKIM and DMARC before sending transactional email.
- Use separate sending identities for transactional and marketing email.
- Provide a one-click unsubscribe for optional marketing messages where applicable.
- Keep payment card data on the payment provider's hosted fields; never store raw card numbers or CVV.
- Store order identifiers and supplier references, not private payment credentials.
- Keep sample portfolio pages visibly labelled as fictional demonstrations.
- Disable public customer reviews until moderation, authenticity and privacy processes exist.
- Use accessibility testing for keyboard navigation, focus, screen readers, zoom, contrast and Arabic reading order.
- Implement rate limits, bot protection, upload-size limits and CSRF protections before opening any upload endpoint.
- Ensure the founder screen is behind strong authentication and does not expose service secrets to the browser.
- Make all founder approvals one-time, action-specific and bound to the exact file hash and supplier quote.
- Do not create a public customer page by deriving content directly from the private order database.
- Provide data export and account deletion requests as workflows, while disclosing any lawful financial-record retention exceptions.
- Keep an incident-report address and a tested internal escalation workflow.

## 14. Launch checklist

- [ ] Domain ownership and registrar security verified.
- [ ] Brand name passed professional trademark clearance in the planned territories.
- [ ] Legal entity and contracting authority verified for the actual seller.
- [ ] Privacy notice, terms, refunds, shipping and personalised-goods disclosures reviewed by counsel.
- [ ] Payment merchant account approved for the actual seller and target currencies.
- [ ] Supplier SKU, quote, print file template and delivery destination validated.
- [ ] Physical sample inspected and photographed truthfully.
- [ ] Arabic typography and RTL regression passed on every Arabic template.
- [ ] Public vault has opt-in and data minimisation controls.
- [ ] Mail authentication and support routing verified.
- [ ] Payment callback signature and duplicate-event tests passed against the exact provider documentation.
- [ ] Backup restore and privacy deletion drills passed.
- [ ] Founder approval replay, tamper and wrong-quote tests passed.
- [ ] Customer proof approval is stored and linked to the exact artwork version.
- [ ] Customer communication is ready for delayed, damaged, lost and misprinted orders.

## 15. Decision Log

| Decision | Owner | Why |
|---|---|---|
| Launch without child photo uploads | CPO + Legal | Minimises sensitive data until the full legal and provider-control chain is proven. |
| Use a distinct public vault projection | CTO + Privacy | Prevents accidental disclosure from the private order record. |
| Publish estimates from live supplier quotes | Operations + CFO | Worldwide shipping and production are SKU- and destination-dependent. |
| Treat legal pages as drafts pending counsel | Chief Legal & Compliance Officer | Missing entity facts and jurisdiction-specific terms cannot be invented. |
| Keep customer and founder approval separate | CX + CTO | Payment does not authorise print; founder signature binds the final artifact and quote. |

**Sign-off:** CPO — website journey; Head of Customer Experience — support and transactional copy; Chief Legal & Compliance Officer — legal review gate; CTO — privacy and approval controls.
