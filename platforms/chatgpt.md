# التثبيت والاستخدام في ChatGPT

المصدر: https://help.openai.com/en/articles/20001066-skills-in-chatgpt

مهارات ChatGPT متاحة لحسابات Business وEnterprise وHealthcare وEdu وفق إعدادات مساحة العمل. المسار في المساعدة: الشريط الجانبي، Plugins، تبويب Skills، ثم Create، ثم Upload from your computer.

## تجهيز الملف

```bash
python3 .agents/skills/scientific-research/scripts/package_skill.py --output dist/scientific-research-2.0.0.zip
```

الأرشيف يضع `SKILL.md` في جذره. راجع المحتوى قبل الرفع. ChatGPT يفحص المهارة المرفوعة، وقد تظهر Needs Review أو Blocked.

## بعد التثبيت

من Skills اختر المهارة أو اطلب مهمة تقع في وصفها، مثل إعداد مقال ترقية في علوم الرياضة بالعربية والإنجليزية. إن لم تظهر Skills، فإعدادات مساحة العمل أو نوع الخطة لا يتيحان الرفع، والمهارة نفسها تبقى قابلة للاستخدام في Cursor وClaude وGemini.

للاستعمال الشخصي خارج مساحة العمل، يمكن لصق تعليمات `SKILL.md` في محادثة، لكن الرفع هو مسار ChatGPT الموثق للمهارة القابلة لإعادة الاستخدام.

ارفع أرشيف الإصدار 2.0.0. قسم التحقق في `SKILL.md` هو الذي يفرض فحص DOI وصفحات المجلات وتدقيق المنهج. الأرشيف لا يحوي ملف باحث معبّأ ولا ملفات دراسة GfA Active Ageing.

## Install and use in ChatGPT

ChatGPT skills are available on Business, Enterprise, Healthcare, and Edu plans, according to the workspace settings. The help path is the sidebar, Plugins, the Skills tab, then Create, then Upload from your computer.

Build the archive from the repository root:

```bash
python3 .agents/skills/scientific-research/scripts/package_skill.py --output dist/scientific-research-2.0.0.zip
```

`SKILL.md` is at the archive root. Review the archive before upload. ChatGPT may mark an upload Needs Review or Blocked. The archive does not contain a filled researcher profile or the GfA Active Ageing study files.

After upload, select the skill or ask for a task inside its description. `python3 scripts/policy.py profile` reads `assets/researcher-profile.json` when `--path` is omitted. Version 2.0.0 is prepared for review and has not been tagged.
