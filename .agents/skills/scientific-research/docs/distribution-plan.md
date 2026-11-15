# خطة التوزيع للباحثين / Distribution plan for researchers

هذه خطة. التنفيذ العلني ينتظر الموافقة. لا يوجد Release منشور.

## من يستطيع التثبيت اليوم / Who can install it today

| الطريق / Path | باحث آخر / Another researcher | يظهر الاسم / Name shown |
|---|---|---|
| نسخ المجلد أو `install-skill.sh cursor-user` | نعم، بعد سحب المستودع العام | الأمر `/scientific-research`، والوصف يبدأ بـ El-Nady Scientific Research Assistant, by Dr. Hesham El-Nady |
| فتح المستودع في Cursor | نعم | المسار نفسه |
| رفع الأرشيف إلى Claude أو ChatGPT أو Gemini | نعم، بعد بناء الأرشيف محليًا | اسم المهارة داخل الأرشيف `scientific-research` |
| Cursor Marketplace أو فريق Teams | لا، لم يُرسل | ملف `.cursor-plugin/plugin.json` جاهز كمرشح فقط |

بناء الأرشيف من جذر المستودع:

```bash
python3 .agents/skills/scientific-research/scripts/package_skill.py \
  --output dist/scientific-research-2.0.0-rc.1.zip
```

الأرشيف جذره `SKILL.md`. لا يحتوي مجلد `studies/` ولا ملفات GfA Active Ageing.

## ما يُرسل للباحث / What a researcher receives

- المهارة العامة: القواعد، والقوالب، وأوامر التدقيق.
- قالب ملف باحث فارغ. كل باحث يكتب بياناته.
- تعليمات التثبيت بالعربية والإنجليزية.

لا تُرسل مع المهارة مسودات الدراسة، ولا نتائج، ولا موافقات، ولا ملف باحث معبّأ.

## خطوات بعد الموافقة / Steps after approval

1. اعتماد الترخيص المقترح أو الإبقاء على MIT.
2. دمج طلب السحب.
3. إنشاء GitHub Release من الوسم الذي يُطلب صراحة، مع هذه الملاحظات.
4. إرسال رابط المستودع ودليل `docs/cursor-install.md`.
5. إذا طُلب الظهور في سوق Cursor: إرسال المستودع من صفحة النشر بعد المراجعة اليدوية للسوق. هذه الخطوة ليست جزءًا من هذا المرشح.
6. لظهور زر Cite في GitHub باسم المؤلف، يمكن لاحقًا وضع `CITATION.cff` في جذر المستودع. النسخة الحالية داخل مجلد المهارة حتى لا تُنسب كل محتويات المستودع قبل الموافقة.

## ما يبقى على الباحث المستلم / What the receiving researcher still does

- ملء ملفه هو، لا ملف المؤلف.
- فتح Scopus Sources وصفحة الرسوم قبل قبول أي مجلة.
- قبول أن فشل الشبكة يعني «غير متحقق منها».
