# التثبيت والاستخدام في Cursor

المهارة مثبتة داخل هذا المستودع في `.cursor/skills/scientific-research/`، وهو رابط إلى المجلد المصدر `.agents/skills/scientific-research/`. دليل Cursor: https://cursor.com/docs/skills

## داخل هذا المستودع

1. افتح المستودع في Cursor.
2. من Customize ثم Skills تظهر المهارة `scientific-research` تحت Agent Decides.
3. في محادثة الوكيل اكتب `/scientific-research` ثم الطلب، أو اطلب بحثًا في الترويح الرياضي أو الترقية فيذكر الوصف المهارة تلقائيًا.

## على جهازك لكل المشروعات

```bash
.agents/skills/scientific-research/scripts/install-skill.sh cursor-user
```

يُنسخ المجلد إلى `~/.cursor/skills/scientific-research/`. مهارات هذا المسار تبقى على جهازك إلى أن تفعّل Sync Skills for Cloud Agents من Settings ثم Agents ثم Context and Tools.

## الاستخدام

ابدأ بملء نسخة من `assets/researcher-profile.template.json` في `assets/researcher-profile.json`، ثم اطلب المنتج واللغة والتصميم. مثال: «جهّز خطة مراجعة منهجية عن الجمباز للجميع لكبار السن في الأندية، بنسختين عربية وإنجليزية، واقترح مجلة Scopus بلا رسوم إلزامية بعد التحقق». المهارة تتوقف إذا نقصت بيانات الباحث، ولا تكتب مرجعًا بلا مصدر، وتراجع كل قسم على حدة.
