# خطة التوزيع للباحثين / Distribution plan for researchers

إصدار GitHub `v2.0.0` منشور. إدراج Cursor Marketplace لم يُرسل ولم يُقبل.

## من يستطيع التثبيت اليوم / Who can install it today

| الطريق / Path | باحث آخر / Another researcher | يظهر الاسم / Name shown |
|---|---|---|
| نسخ المجلد أو `install-skill.sh cursor-user` | نعم، بعد سحب المستودع العام | الأمر `/scientific-research`، والوصف يبدأ بـ El-Nady Scientific Research Assistant, by Dr. Hesham El-Nady |
| فتح المستودع في Cursor | نعم | المسار نفسه |
| رفع الأرشيف إلى Claude أو ChatGPT أو Gemini | نعم، بعد بناء الأرشيف محليًا | اسم المهارة داخل الأرشيف `scientific-research` |
| Cursor Marketplace | لا، لم يُرسل ولم يُقبل | الإضافة تكتشف `skills/scientific-research` فقط |

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

الوسم `v2.0.0` وأرشيف GitHub Release منشوران. هذا التعديل لا يعيد إنشاء الوسم ولا يستبدل الأرشيف المنشور.

1. بيان الإضافة يشير إلى المجلد الأب `skills/`، وفيه مهارة `scientific-research` فقط.
2. اختبار التثبيت المحلي: `scripts/install-skill.sh cursor-plugin-local` ثم Reload Window في Cursor.
3. إرسال رابط المستودع العام من https://cursor.com/marketplace/publish يتم يدويًا بحساب صاحب المستودع. القبول يظهر لاحقًا في https://cursor.com/marketplace.
4. زر Cite في GitHub يقرأ `CITATION.cff` من جذر المستودع. النسخة داخل مجلد المهارة مطابقة له.

## ما يبقى على الباحث المستلم / What the receiving researcher still does

- ملء ملفه هو، لا ملف المؤلف.
- فتح Scopus Sources وصفحة الرسوم قبل قبول أي مجلة.
- قبول أن فشل الشبكة يعني «غير متحقق منها».
