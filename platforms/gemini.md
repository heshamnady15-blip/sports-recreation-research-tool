# التثبيت والاستخدام في Gemini

المصدر: https://support.google.com/gemini/answer/17094296

في تطبيق Gemini على الويب، من صفحة Skills اختر Create ثم Upload. يمكن رفع ملف `SKILL.md` أو مجلدًا أو أرشيفًا يحتوي `SKILL.md` في مجلده الرئيسي. اسم المهارة داخل الملف يجب أن يبقى `scientific-research` بحروف صغيرة وشرطات.

## تجهيز الملف

ارفع المجلد `.agents/skills/scientific-research/` لأن اسمه يطابق اسم المهارة، أو ابنِ أرشيفًا جذوره `SKILL.md`:

```bash
python3 .agents/skills/scientific-research/scripts/package_skill.py --output dist/scientific-research-2.0.0.zip
```

راجع المهارة بعد الرفع ثم اضغط Create. في حسابات Gemini Enterprise يكون المسار من Skills ثم Add ثم Upload skill، كما في https://support.google.com/g/answer/18067667

## الاستخدام

اكتب `/scientific-research` في المحادثة، أو اذكر المهارة، أو اطلب مباشرة مراجعة منهجية في الترويح الرياضي أو نشاطًا بدنيًا لكبار السن. Gemini يستطيع اختيار المهارة من وصفها. اجمع المهارة مع غيرها في المحادثة نفسها إذا لزم. الإصدار 2.0.0 موثق داخل `SKILL.md` في المهارة نفسها، لا في مهارة منفصلة. `python3 scripts/policy.py profile` يقرأ `assets/researcher-profile.json` عند غياب `--path`.

## Install and use in Gemini

On the Gemini web app, open Skills, choose Create, then Upload. Upload `.agents/skills/scientific-research/` or `dist/scientific-research-2.0.0.zip`. The skill name inside the file stays `scientific-research`. The archive root contains `SKILL.md` and does not contain a filled researcher profile or the GfA Active Ageing study files.

```bash
python3 .agents/skills/scientific-research/scripts/package_skill.py --output dist/scientific-research-2.0.0.zip
```

Review the skill after upload, then press Create. In Gemini Enterprise the path is Skills, Add, Upload skill. In the conversation, type `/scientific-research` or ask for the research task directly. `python3 scripts/policy.py profile` reads `assets/researcher-profile.json` when `--path` is omitted. Version 2.0.0 is prepared for review and has not been tagged.

الرفع من ملف متاح في تطبيق Gemini على الويب وعلى Mac حسب صفحة المساعدة. إذا لم يظهر Create Upload، فالحساب ما زال على Gems؛ انقل التعليمات من `SKILL.md` إلى Gem إلى أن يكتمل التحويل إلى Skills في حسابك.
