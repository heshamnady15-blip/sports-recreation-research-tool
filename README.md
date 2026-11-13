# مهارة بحث الترويح والجمباز للجميع

مهارة واحدة بصيغة [Agent Skills](https://agentskills.io/specification) تأخذ بحث علوم الرياضة، في تخصص الترويح والجمباز للجميع، من سؤال الدراسة حتى مراجعة كل قسم وترشيح مجلات سكوبس بلا رسوم على المؤلف.

النسخة الأصلية:

`.agents/skills/sport-recreation-gymnastics-research/`

هذا المسار يكفي لـ Cursor وChatGPT عبر Codex وGemini CLI. Claude Code يقرأ الرابط في `.claude/skills/`. الرفع إلى مواقع Claude وChatGPT وGemini يتم بملف مضغوط من `dist/`.

## ماذا تفعل المهارة

- تسأل عن نظام الجامعة ونوع البحث والتصميم والعينة والأخلاق وحد التشابه قبل كتابة المتن.
- تراجع كل قسم بحكم: مقبول، أو تعديل، أو غير صالح للإرسال.
- تفرّق بين خطة لم تُجمع بياناتها وبين نتائج مبنية على ملف الباحث.
- ترشّح المجلات بعد فتح صفحة الرسوم وسجل سكوبس في يوم الترشيح نفسه، وتستبعد أي مجلة ذات رسوم أو فهرسة موقوفة أو نطاق بعيد.

لا تخترع مراجعًا ولا نتائج ولا أرباع مجلات، ولا تضمن قبول النشر.

## تشغيلها

في Cursor اكتب `/sport-recreation-gymnastics-research` أو اطلب مراجعة بحث في الترويح أو الجمباز للجميع.

في Claude Code اكتب `/sport-recreation-gymnastics-research`.

في Codex اكتب `$sport-recreation-gymnastics-research`. في تطبيق ChatGPT المكتبي اذكر المهارة بـ `@` بعد ظهورها في المهارات.

في Gemini CLI اطلب تفعيل المهارة بالاسم. في تطبيق Gemini ارفع ملف `dist/sport-recreation-gymnastics-research-gemini.zip` من صفحة المهارات.

## تثبيت المهارة خارج هذا المستودع

Cursor وCodex وGemini CLI على جهازك: انسخ المجلد إلى `~/.agents/skills/`.

Claude Code على جهازك: انسخ المجلد إلى `~/.claude/skills/`.

Claude على الويب: ارفع `dist/sport-recreation-gymnastics-research-claude-chatgpt.zip`. داخل الأرشيف يجب أن يظهر المسار `sport-recreation-gymnastics-research/SKILL.md`.

ChatGPT: من المهارات اختر الإنشاء ثم الرفع، واستخدم أرشيف Claude نفسه.

Gemini على الويب أو التطبيق: ارفع `dist/sport-recreation-gymnastics-research-gemini.zip`، حيث يقع `SKILL.md` في المجلد الرئيسي للأرشيف.

## تحديث الأرشيف

```bash
python3 .agents/skills/sport-recreation-gymnastics-research/scripts/run_checks.py
```

يفحص ملفات المهارة، والروابط الداخلية، ورابط Claude، وبيانات ChatGPT، وجذر أرشيف كل منصة. فحص اختلاف اسم المجلد عن اسم المهارة اختبار سلبي: نجاحه أن يرفض المدقق المجلد، وهذا رفض متوقع لا عيب في المهارة.
