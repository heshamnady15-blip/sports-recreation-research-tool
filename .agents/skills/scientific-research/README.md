# El-Nady Scientific Research Assistant

**المؤلف / Author:** Dr. Hesham El-Nady  
**الاسم التقني / Technical name:** `scientific-research`  
**الإصدار المرشح / Release candidate:** `2.0.0-rc.1`  
**المستودع / Repository:** [heshamnady15-blip/sports-recreation-research-tool](https://github.com/heshamnady15-blip/sports-recreation-research-tool)

هذا ملف المهارة نفسها. أمر Cursor يبقى `/scientific-research` لأن مواصفة Agent Skills تلزم حقل `name` بأن يطابق اسم المجلد. الاسم الظاهر في الوصف وبيانات المهارة هو El-Nady Scientific Research Assistant.

This file travels with the skill. The Cursor command stays `/scientific-research` because the Agent Skills specification requires `name` to match the folder. The public name in the description and metadata is El-Nady Scientific Research Assistant.

## القدرات / Capabilities

| الوظيفة / Function | الأمر / Command | الشبكة / Network |
|---|---|---|
| اكتمال ملف الباحث / Researcher profile | `profile` | لا / No |
| حد التشابه حسب المنتج / Similarity by product | `similarity` | لا. لقطة الترقية ملف محلي مؤرخ، وليست صفحة المجلس المفتوحة الآن / No. The promotion figure is a dated local snapshot, not a live council page |
| قرار أولي للمجلة من الحقول المعطاة / Preliminary journal decision | `journal` | لا. ليس تحققًا من Scopus أو صفحة الرسوم / No. This is not a Scopus or fee-page check |
| شكل المرجع / Reference shape | `references` | لا / No |
| مراجعة القسم بأربعة معايير / Four-criterion section review | `review` | لا / No |
| تدقيق أنماط المنهج والإحصاء / Methods and statistics patterns | `audit-methods` | لا / No |
| التحقق من DOI / DOI verification | `verify-references` | نعم: `api.crossref.org` ثم `api.datacite.org` / Yes |
| دليل المجلة / Journal evidence | `verify-journal` | نعم: الرابطان المذكوران في السجل فقط / Yes: only the two URLs named in the record |
| التقرير الجامع / Combined report | `audit` | عند إرفاق مراجع أو مجلة / When references or a journal record are included |

نجاح التدقيق الآلي لا يثبت صحة البحث كاملة. تعذر الاتصال يبقى «غير قابل للتحقق» ولا يتحول إلى مرجع أو مجلة مقبولين.

An automated pass does not establish full scientific validity. A failed connection stays unverified and is not turned into an accepted reference or journal.

## التثبيت / Install

الدليل المفصل لمستخدم Cursor جديد: [docs/cursor-install.md](docs/cursor-install.md).

من جذر هذا المستودع:

```bash
.agents/skills/scientific-research/scripts/install-skill.sh cursor-user
```

ينسخ المهارة إلى `~/.cursor/skills/scientific-research/` ولا ينسخ دراسة GfA Active Ageing.

From the repository root, the same command copies only this skill to `~/.cursor/skills/scientific-research/`. It does not copy the GfA Active Ageing study.

## الاستخدام / Use

1. انسخ `assets/researcher-profile.template.json` إلى `assets/researcher-profile.json` واملأ اسمك وجامعتك وقسمك وبريدك المؤسسي وORCID. القالب فارغ عمدًا. اسم مؤلف المهارة لا يملأ هذا الملف.
2. في Cursor اكتب `/scientific-research` ثم الطلب، أو اطلب بحثًا في الترويح أو الجمباز للجميع أو الترقية.
3. نفّذ الأوامر من مجلد المهارة. أمثلة بلا شبكة:

```bash
python3 scripts/policy.py profile
python3 scripts/policy.py similarity --product original
python3 scripts/policy.py journal --index scopus --quartile Q1 \
  --apc-mandatory false --publication-year 2026
python3 scripts/policy.py audit-methods --path manuscript.md
python3 scripts/capability_probe.py
```

الأمر `journal` بلا مصدر فهرسة ومصدر رسوم يعيد `unverified` ولا يوصي بمجلة.

4. التحقق الخارجي، عند وجود الشبكة:

```bash
python3 scripts/policy.py verify-references --path references.json
python3 scripts/policy.py verify-journal --path journal-evidence.json
python3 scripts/capability_probe.py --live-doi 10.1038/171737a0
```

`--live-doi` يطبع السجل الذي تعيده Crossref أو DataCite. لا تستخدم مخرجاته إلا إذا طابق العنوان والمؤلفين والسنة والمجلة. انقطاع الاتصال ليس تطابقًا.

Copy the empty researcher template and fill your own identity. The skill author's name does not fill that file. The `journal` command without an indexing source and a fee source returns `unverified` and recommends nothing. `--live-doi` prints the record returned by Crossref or DataCite.

## التحديث / Update

1. اجلب آخر commit من المستودع.
2. أعد تشغيل سكربت التثبيت نفسه، أو استبدل مجلد `~/.cursor/skills/scientific-research/` بنسخة المجلد الجديدة.
3. شغّل الاختبارات من جذر المستودع، وهي لا تفتح الشبكة:

```bash
python3 -m unittest tests.test_scientific_research tests.test_scientific_research_v2 tests.test_skill_clean_project
```

مثال GfA Active Ageing اختبار منفصل ولا يلزم لتثبيت المهارة:

```bash
python3 -m unittest tests.test_gfa_active_ageing_v21
```

Fetch the repository, install the skill folder again, and run the three skill test modules. Those tests do not open the network. The GfA example tests are separate.

## ما لا تفعله المهارة / What this skill does not do

- لا تخترع مراجعًا أو عينات أو موافقات أو نتائج.
- لا توصي بمجلة قبل فتح مصدر الفهرسة ومصدر الرسوم في السجل.
- لا تضم ملفات دراسة GfA Active Ageing. تلك الدراسة مثال داخل المستودع، كما في [references/applied-example.md](references/applied-example.md).

## الترخيص / License

مستودع المصدر يحمل اليوم ملف `LICENSE` برخصة MIT وحقوق النسخ باسم الحساب `heshamnady15-blip`. اقتراح ترخيص المهارة للمشاركة مع نسب التأليف مكتوب في [docs/license-proposal.md](docs/license-proposal.md) ولم يُعتمد بعد، ولم يُستبدل ملف `LICENSE`.
