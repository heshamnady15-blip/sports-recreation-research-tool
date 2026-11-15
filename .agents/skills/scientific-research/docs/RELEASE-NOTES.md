# Release notes — 2.0.0

الحالة: النسخة 2.0.0 مجهّزة للمراجعة. لم يُنشأ الوسم `v2.0.0`، ولم يُنشر GitHub Release، ولم يُدمج طلب السحب، ولم تُرسل الإضافة إلى Cursor Marketplace.

Status: version 2.0.0 is prepared for review. The `v2.0.0` tag has not been created, no GitHub Release has been published, the pull request is not merged, and the plugin has not been submitted to the Cursor Marketplace.

## الاسم / Name

- الاسم الرسمي: El-Nady Scientific Research Assistant
- المؤلف الظاهر: Dr. Hesham El-Nady
- الاسم التقني وأمر Cursor: `scientific-research`
- رقم الإصدار في الهوية والاستشهاد والإضافة وهذه الملاحظات: `2.0.0`

## ما تغيّر عن المرشح 2.0.0-rc.1 / What changed after 2.0.0-rc.1

- توحيد رقم الإصدار إلى `2.0.0`.
- سطر حقوق النسخ في `LICENSE` أصبح `Copyright (c) 2026 Dr. Hesham El-Nady (github.com/heshamnady15-blip)`. نص إذن MIT لم يتغير.
- `python3 scripts/policy.py profile` يقرأ `assets/researcher-profile.json` عند غياب `--path`. الخيار `--path` ما زال يحدد ملفًا آخر، والملف الغائب يبقي النتيجة غير مكتملة.
- `CITATION.cff` موجود في جذر المستودع وداخل مجلد المهارة، والنسختان متطابقتان.
- أرشيف النشر `dist/scientific-research-2.0.0.zip` يُبنى بأمر `package_skill.py`. مجلد `dist/` خارج Git. الأرشيف يستبعد ملف الباحث المعبأ وملفات الدراسة.

## ما بقي من المرشح / What remains from the candidate

- توثيق عربي وإنجليزي في `README.md` و`docs/cursor-install.md` وأدلة `platforms/`.
- هوية المهارة في `assets/skill-identity.json` منفصلة عن قالب ملف الباحث.
- `scripts/capability_probe.py` لبيان ما يعمل بلا شبكة وما يحتاج إلى Crossref أو DataCite أو صفحة مذكورة في السجل.
- دراسة GfA Active Ageing تبقى مثالًا داخل المستودع في `studies/gfa-active-ageing/`. ملفات الدراسة لم تُنقل إلى المهارة ولم تُحذف.
- بيان إضافة Cursor في `.cursor-plugin/plugin.json` يشير إلى هذه المهارة فقط، بلا حقل ترخيص داخل البيان. الرخصة النافذة هي ملف `LICENSE`.

## قواعد التدقيق / Audit rules

أوامر `policy.py` و`verify_v2.py` تحتفظ بسلوك الإصدار الثاني: لا يتحول انقطاع الشبكة إلى قبول، ولا يوصي أمر `journal` بمجلة بلا مصادر، ولا يخترع التدقيق بيانات.

## قبل الوسم والنشر / Before the tag and the GitHub Release

1. موافقة نهائية صريحة على الدمج.
2. موافقة نهائية صريحة قبل `git tag v2.0.0` وقبل إنشاء GitHub Release.
3. إرفاق `dist/scientific-research-2.0.0.zip` بأمر البناء أدناه، بعد إعادة فحص محتوياته.
4. عدم إعلان مجلة أو مرجع على أنه متحقق منه إلا بسجل فتح فعلي.

```bash
python3 .agents/skills/scientific-research/scripts/package_skill.py \
  --output dist/scientific-research-2.0.0.zip
```
