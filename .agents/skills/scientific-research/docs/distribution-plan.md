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
  --output dist/scientific-research-2.0.0.zip
```

الأرشيف جذره `SKILL.md`. البناء يستبعد `researcher-profile.json` وأي مسار يحوي `studies` أو `gfa-active-ageing`. مجلد `dist/` خارج Git، لذلك يُرفق الأرشيف عند إنشاء GitHub Release ولا يُحفظ في التاريخ.

## ما يُرسل للباحث / What a researcher receives

- المهارة العامة: القواعد، والقوالب، وأوامر التدقيق.
- قالب ملف باحث فارغ. كل باحث يكتب بياناته.
- تعليمات التثبيت بالعربية والإنجليزية.

لا تُرسل مع المهارة مسودات الدراسة، ولا نتائج، ولا موافقات، ولا ملف باحث معبّأ.

## خطوات بعد الموافقة النهائية / Steps after final approval

سطر حقوق MIT ورقم `2.0.0` و`CITATION.cff` في الجذر نُفذت في فرع المراجعة. الوسم والنشر ما زالا ينتظران موافقة نهائية.

1. دمج طلب السحب بعد الموافقة النهائية.
2. إنشاء الوسم `v2.0.0` فقط بعد طلب صريح، ثم GitHub Release من ذلك الوسم مع `docs/RELEASE-NOTES.md` وأرشيف `dist/scientific-research-2.0.0.zip`.
3. إرسال رابط المستودع ودليل `docs/cursor-install.md`.
4. إذا طُلب الظهور في سوق Cursor: إرسال المستودع من صفحة النشر بعد المراجعة اليدوية للسوق. هذه الخطوة ليست جزءًا من هذه النسخة.
5. زر Cite في GitHub يقرأ `CITATION.cff` من جذر المستودع. النسخة داخل مجلد المهارة مطابقة له.

## ما يبقى على الباحث المستلم / What the receiving researcher still does

- ملء ملفه هو، لا ملف المؤلف.
- فتح Scopus Sources وصفحة الرسوم قبل قبول أي مجلة.
- قبول أن فشل الشبكة يعني «غير متحقق منها».
