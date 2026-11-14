# التثبيت والاستخدام في Gemini

المصدر: https://support.google.com/gemini/answer/17094296

في تطبيق Gemini على الويب، من صفحة Skills اختر Create ثم Upload. يمكن رفع ملف `SKILL.md` أو مجلدًا أو أرشيفًا يحتوي `SKILL.md` في مجلده الرئيسي. اسم المهارة داخل الملف يجب أن يبقى `scientific-research` بحروف صغيرة وشرطات.

## تجهيز الملف

ارفع المجلد `.agents/skills/scientific-research/` لأن اسمه يطابق اسم المهارة، أو ابنِ أرشيفًا جذوره `SKILL.md`:

```bash
python3 .agents/skills/scientific-research/scripts/package_skill.py --output dist/scientific-research.zip
```

راجع المهارة بعد الرفع ثم اضغط Create. في حسابات Gemini Enterprise يكون المسار من Skills ثم Add ثم Upload skill، كما في https://support.google.com/g/answer/18067667

## الاستخدام

اكتب `/scientific-research` في المحادثة، أو اذكر المهارة، أو اطلب مباشرة مراجعة منهجية في الترويح الرياضي أو نشاطًا بدنيًا لكبار السن. Gemini يستطيع اختيار المهارة من وصفها. اجمع المهارة مع غيرها في المحادثة نفسها إذا لزم. الإصدار الثاني موثق داخل `SKILL.md` في المهارة نفسها، لا في مهارة منفصلة.

الرفع من ملف متاح في تطبيق Gemini على الويب وعلى Mac حسب صفحة المساعدة. إذا لم يظهر Create Upload، فالحساب ما زال على Gems؛ انقل التعليمات من `SKILL.md` إلى Gem إلى أن يكتمل التحويل إلى Skills في حسابك.
