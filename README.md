# sports-recreation-research-tool

مهارة بحث علمي للترويح الرياضي، والجمباز للجميع، وعلوم الرياضة، والتربية البدنية. تعمل في Cursor وClaude وChatGPT وGemini من مجلد واحد.

تغطي أبحاثًا أصيلة، وأبحاث ترقية وفق قواعد المجلس الأعلى للجامعات في مصر، والرسائل، والمراجعات المنهجية، والتحليل البعدي، وتحويل الرسائل إلى مقالات. اللغة عربية أو إنجليزية أو النسختان. التوثيق الافتراضي APA 7 ويُحوَّل إلى نظام المجلة. لا تُقترح مجلة Scopus قبل التحقق من ربعها ورسوم المؤلف، ولا تُكتب مراجع أو بيانات غير مسترجعة.

## التثبيت

- [Cursor](platforms/cursor.md)
- [Claude](platforms/claude.md)
- [ChatGPT](platforms/chatgpt.md)
- [Gemini](platforms/gemini.md)

المصدر الذي تعدّله هو `.agents/skills/scientific-research/`. مجلدا `.cursor/skills/scientific-research` و`.claude/skills/scientific-research` يشيران إليه.

## الاختبار

```bash
python3 -m unittest discover -s tests -v
```

بيانات الباحث تُنسخ من قالب المهارة إلى `assets/researcher-profile.json` وتبقى خارج Git.
