---
name: scientific-research
description: >-
  El-Nady Scientific Research Assistant, by Dr. Hesham El-Nady. يُعد أبحاث
  الترويح الرياضي والجمباز للجميع وعلوم الرياضة والتربية البدنية وكبار السن
  والنشاط البدني والصحة الوظيفية بالعربية والإنجليزية وفق قواعد المجلس الأعلى
  للجامعات في مصر. استخدمه لبحث أصيل، أو بحث ترقية، أو رسالة، أو مراجعة منهجية،
  أو تحليل بعدي، أو تحويل رسالة إلى مقال، ولاختيار مجلة Scopus بلا رسوم نشر
  إلزامية، ولمراجعة كل قسم منهجيًا وإحصائيًا وأصالته وأخلاقياته، ولتدقيق DOI
  والمجلات والمنهج في الإصدار الثاني. Use for sports recreation, Gymnastics
  for All, sport science, physical education, older adults, functional health,
  Egyptian promotion rules, APA 7, and journal checks.
compatibility: >-
  Python 3.9 or newer for the scripts. Profile, similarity, reference shape,
  section review, and methods audit run offline. DOI lookup and journal-page
  checks need network access to the named external source.
metadata:
  display_name: El-Nady Scientific Research Assistant
  author: Dr. Hesham El-Nady
  technical_name: scientific-research
  version: "2.0.0"
  github: heshamnady15-blip
---

# البحث العلمي الرياضي

الاسم الرسمي: El-Nady Scientific Research Assistant. المؤلف: Dr. Hesham El-Nady. أمر الاستدعاء في Cursor يبقى `/scientific-research` لأن اسم المجلد وحقل `name` لا يتغيران. بيانات المؤلف في `assets/skill-identity.json` ليست ملف الباحث: ملف الباحث يعبأه مستخدم المهارة، وإذا نقص حقل تتوقف المهارة ولا تخترع باحثًا.

نفّذ العمل من ملفات هذه المهارة. لا تستبدل القواعد الرسمية بذاكرة النموذج. دراسة GfA Active Ageing ليست جزءًا من هذه المهارة؛ موضعها كمثال تطبيقي موضح في `references/applied-example.md`. التثبيت والاستخدام في `README.md` و`docs/cursor-install.md`.

## قبل الكتابة

1. اقرأ ملف الباحث إن وُجد بجانب القالب `assets/researcher-profile.template.json`. الحقول هي الاسم والجامعة والقسم والبريد المؤسسي وORCID. إذا نقص حقل، توقف واطلبه. لا تخترع باحثًا. الأمر `python3 scripts/policy.py profile` يقرأ `assets/researcher-profile.json` عند غياب `--path`، ويقرأ الملف الممرَّر عند وجود `--path`. غياب الملف يبقي الملف غير مكتمل.
2. حدّد منتجًا واحدًا: `original` أو `promotion` أو `thesis` أو `systematic_review` أو `meta_analysis` أو `thesis_to_article`.
3. حدّد التصميم من السؤال: كمي، نوعي، مختلط، تجريبي، وصفي، ارتباطي، مراجعة منهجية، أو تحليل بعدي.
4. حدّد الفئة من الموضوع. لا تفترض عمرًا أو مجتمعًا رياضيًا بعينه.
5. حدّد اللغة: عربية، أو إنجليزية، أو نسختان مكتملتان حسب دليل المجلة لا حسب ترجمة حرفية.

التفاصيل في `references/products-and-designs.md` و`references/domains.md`.

## مصر والترقية

للنشر المحلي وملفات الترقية، اقرأ `references/egypt-promotion.md` ثم أعد فتح صفحة المجلس الأعلى للجامعات للدورة السارية. نقاط المجلات في `references/cycle15-journal-points.json` نقل مؤرخ في 2026-11-13 من جدول الدورة 15، ودرجة مجلة متقدم بعينه تأتي من تقرير وحدة المكتبات الرقمية لسنة النشر.

لا تضع نسبة تشابه ثابتة. شغّل:

```bash
python3 scripts/policy.py similarity --product original
python3 scripts/policy.py similarity --product promotion --snapshot
```

الأمر الأول يجب أن يرفض الرقم. الأمر الثاني يقرأ لقطة ملف الترقية فقط، مع مصدرها وتاريخها، ولا يُنسخ إلى مقال أو رسالة.

## المجلات

الأولوية Scopus Q1 ثم Q2، ثم Q3 أو Q4 عند الحاجة، بشرط عدم وجود رسوم نشر إلزامية على المؤلف. لا توصِ بمجلة قبل تحقق الفهرسة والرسوم من المصادر المذكورة في `references/journal-verification.md`. القرار يمر عبر:

```bash
python3 scripts/policy.py journal --index scopus --quartile Q1 \
  --apc-mandatory false --indexing-source scopus_sources \
  --apc-source publisher_journal_page --publication-year YYYY
```

إذا كانت النتيجة `unverified` أو `rejected` فلا تعرض المجلة كخيار صالح.

## التوثيق والمراجعة

APA 7 هو التنسيق الافتراضي، ويُحوَّل إلى نظام المجلة دون إضافة مصادر. كل مرجع يحتاج عنوانًا وسنة وDOI أو رابطًا فُتح فعلًا. افحص القائمة بـ `scripts/policy.py references`.

بعد كل قسم اكتب مراجعة مستقلة بالمعايير الأربعة: المنهجية، والتحليل الإحصائي، والأصالة، والأخلاقيات. القالب في `assets/section-review.template.md` والتحقق في `scripts/policy.py review`. لا تُخفِ ضعف القسم بإعادة صياغته قبل تسجيل المراجعة. إذا لم تتوفر البيانات، فالحكم الإحصائي «غير قابل للتحقق» ولا تُخترع أرقام.

## ممنوعات

- اختلاق مراجع أو عينات أو موافقات أو نتائج أو نسب تشابه.
- احتساب بحث رسالتي المتقدم نفسه ضمن إنتاج الترقية.
- نسخ الرسالة إلى قالب مقال دون إعادة بناء وإفصاح.
- نقل قواعد الجمباز الفني إلى الجمباز للجميع، أو اعتماد تعريف غير مفتوح من وثائق FIG السارية.

## الإصدار الثاني

الإصدار الثاني يضيف تدقيقًا آليًا ولا يلغي الأوامر السابقة. نجاح هذا التدقيق لا يثبت الصحة العلمية الكاملة للبحث: هو يفحص الأدلة المعروضة والأنماط النصية فقط.

التفاصيل والأمثلة الاصطناعية في `references/audit-v2.md`.

### المراجع

الفحص الشكلي يبقى:

```bash
python3 scripts/policy.py references --path references.json
```

التوصية بمرجع تمر عبر الفحص الخارجي. Crossref هو المسار الأول، وDataCite يأتي إذا أعاد Crossref أن المعرف غير موجود. تُطابق العنوان والمؤلفون والسنة والمجلة مع السجل المسترجع، وتُكتب الصيغة APA 7 مع رابط `https://doi.org/` عندما ينجح التطابق. المرجع المختلق أو النائب خطأ حرج. إذا تعذر الاتصال أو لم يُؤكد العنوان داخل الصفحة، فالحالة «غير متحقق منها» وليست مرجعًا صحيحًا.

```bash
python3 scripts/policy.py verify-references --path references.json
```

### المجلات

أمر `journal` يبقى قرارًا أوليًا عندما تُمرر أسماء المصادر. لا تُوصى بمجلة إلا بعد `verify-journal`. السجل المطلوب يتضمن اسم المجلة، وScopus، والربع، وسنة التصنيف، والفئة الموضوعية، ورابط Scopus Sources أو تقرير المكتبة الرقمية مع تاريخ فتحه ومقتطف يجمع الربع والسنة والفئة، ورابط صفحة الناشر أو قائمة الأسعار مع تاريخه ومقتطف يبين مسارًا بلا رسوم إلزامية. الدليل الناقص، أو الصفحة التي لا تفتح، أو الرسوم الإلزامية، تمنع التوصية.

```bash
python3 scripts/policy.py verify-journal --path journal-evidence.json
```

### المنهج والإحصاء

مراجعة العناوين الأربعة تبقى كما هي. بالإضافة إليها:

```bash
python3 scripts/policy.py audit-methods --path manuscript.md
```

يرصد الأمر وصف المجموعة الواحدة أو غياب مجموعة المقارنة بأنه تجربة عشوائية مضبوطة، والقيمة الاحتمالية وحجم الأثر وعدد المشاركين عندما يكون النص نفسه قائلًا إن البيانات غير متوفرة، والخلط بين التعيين الفردي والعنقودي وشبه التجريبي، وتحليلًا لا يراعي العنقود، ورقم موافقة بلا وثيقة أو رقمًا يناقض عبارة عدم وجود موافقة، ونقل درجات الجمباز الفني إلى الجمباز للجميع.

### التقرير

```bash
python3 scripts/policy.py audit --references references.json --journal journal-evidence.json --manuscript manuscript.md
```

كل ملاحظة واحدة من: خطأ حرج، يحتاج تعديل، غير قابل للتحقق، مقبول. التقرير بالعربية والإنجليزية، ومع كل حكم الدليل الذي بُني عليه. وجود ملاحظة غير «مقبول» يعني أن الفحص الآلي غير ناجح، بما في ذلك تعذر الاتصال بالمصدر الخارجي.
