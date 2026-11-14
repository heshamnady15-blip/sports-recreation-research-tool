# التثبيت والاستخدام في ChatGPT

المصدر: https://help.openai.com/en/articles/20001066-skills-in-chatgpt

مهارات ChatGPT متاحة لحسابات Business وEnterprise وHealthcare وEdu وفق إعدادات مساحة العمل. المسار في المساعدة: الشريط الجانبي، Plugins، تبويب Skills، ثم Create، ثم Upload from your computer.

## تجهيز الملف

```bash
python3 .agents/skills/scientific-research/scripts/package_skill.py --output dist/scientific-research.zip
```

الأرشيف يضع `SKILL.md` في جذره. راجع المحتوى قبل الرفع. ChatGPT يفحص المهارة المرفوعة، وقد تظهر Needs Review أو Blocked.

## بعد التثبيت

من Skills اختر المهارة أو اطلب مهمة تقع في وصفها، مثل إعداد مقال ترقية في علوم الرياضة بالعربية والإنجليزية. إن لم تظهر Skills، فإعدادات مساحة العمل أو نوع الخطة لا يتيحان الرفع، والمهارة نفسها تبقى قابلة للاستخدام في Cursor وClaude وGemini.

للاستعمال الشخصي خارج مساحة العمل، يمكن لصق تعليمات `SKILL.md` في محادثة، لكن الرفع هو مسار ChatGPT الموثق للمهارة القابلة لإعادة الاستخدام.

ارفع الأرشيف بعد بناء الإصدار الثاني. قسم الإصدار الثاني في `SKILL.md` هو الذي يفرض فحص DOI وصفحات المجلات وتدقيق المنهج.
