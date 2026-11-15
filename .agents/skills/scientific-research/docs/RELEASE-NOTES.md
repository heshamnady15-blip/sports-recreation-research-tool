# Release notes — 2.0.0-rc.1

الحالة: مرشح للنشر. لم يُنشأ GitHub Release، ولم يُدمج الفرع، ولم يُرسل إلى Cursor Marketplace.

Status: release candidate. No GitHub Release has been created, the branch is not merged, and the plugin has not been submitted to the Cursor Marketplace.

## الاسم / Name

- الاسم الرسمي: El-Nady Scientific Research Assistant
- المؤلف الظاهر: Dr. Hesham El-Nady
- الاسم التقني وأمر Cursor: `scientific-research`

## ما يشمله هذا المرشح / What this candidate includes

- توثيق عربي وإنجليزي في `README.md` و`docs/cursor-install.md`.
- هوية المهارة في `assets/skill-identity.json` و`CITATION.cff`، منفصلة عن قالب ملف الباحث.
- `scripts/capability_probe.py` لبيان ما يعمل بلا شبكة وما يحتاج إلى Crossref أو DataCite أو صفحة مذكورة في السجل.
- فصل صريح عن دراسة GfA Active Ageing في `references/applied-example.md`. ملفات الدراسة لم تُنقل ولم تُحذف.
- اختبار مشروع نظيف في `tests/test_skill_clean_project.py`.
- بيان إضافة Cursor في `.cursor-plugin/plugin.json` يشير إلى هذه المهارة فقط.
- اقتراح ترخيص في `docs/license-proposal.md`. ملف `LICENSE` في جذر المستودع لم يتغير.

## ما لم يتغير في قواعد التدقيق / Audit rules that did not change

أوامر `policy.py` و`verify_v2.py` تحتفظ بسلوك الإصدار الثاني: لا يتحول انقطاع الشبكة إلى قبول، ولا يوصي أمر `journal` بمجلة بلا مصادر، ولا يخترع التدقيق بيانات.

## قبل وسم الإصدار / Before tagging a release

1. موافقة صريحة على الدمج.
2. موافقة صريحة على الترخيص المقترح أو الإبقاء على MIT مع سطر نسب التأليف.
3. موافقة صريحة قبل `git tag` وقبل إنشاء GitHub Release.
4. عدم إعلان مجلة أو مرجع على أنه متحقق منه إلا بسجل فتح فعلي.
