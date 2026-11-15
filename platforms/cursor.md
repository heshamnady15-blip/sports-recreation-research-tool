# التثبيت والاستخدام في Cursor

الاسم الرسمي: El-Nady Scientific Research Assistant. المؤلف: Dr. Hesham El-Nady. الأمر في المحادثة يبقى `/scientific-research` لأن Cursor يعرض اسم المجلد، ووصف المهارة يبدأ بالاسم الرسمي واسم المؤلف. دليل المستخدم الجديد داخل المهارة: `.agents/skills/scientific-research/docs/cursor-install.md`.

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

ابدأ بملء نسخة من `assets/researcher-profile.template.json` في `assets/researcher-profile.json`، ثم اطلب المنتج واللغة والتصميم. الأمر `python3 scripts/policy.py profile` يقرأ هذا الملف عند غياب `--path`، والخيار `--path` يحدد ملفًا آخر. مثال: «جهّز خطة مراجعة منهجية عن الجمباز للجميع لكبار السن في الأندية، بنسختين عربية وإنجليزية، واقترح مجلة Scopus بلا رسوم نشر إلزامية بعد التحقق». المهارة تتوقف إذا نقصت بيانات الباحث، ولا تكتب مرجعًا بلا مصدر، وتراجع كل قسم على حدة.

الإصدار 2.0.0 من المهارة نفسها يضيف `verify-references` و`verify-journal` و`audit-methods` و`audit` داخل `scripts/policy.py`. أمر `journal` يبقى قرارًا أوليًا، والتوصية بمجلة أو بمرجع تمر من أوامر التحقق. التقرير آلي وبالعربية والإنجليزية، ولا يُقرأ على أنه إثبات لصحة البحث كاملة.

## اختبار إضافة Cursor محليًا

```bash
.agents/skills/scientific-research/scripts/install-skill.sh cursor-plugin-local
```

يُنشئ `~/.cursor/plugins/local/el-nady-scientific-research/` من `.cursor-plugin/plugin.json` ومجلد `skills/scientific-research` فقط. أعد تحميل النافذة ثم افتح Customize. هذا التثبيت لا يرسل الإضافة إلى Cursor Marketplace.

## Install and use in Cursor

The public name is El-Nady Scientific Research Assistant, by Dr. Hesham El-Nady. The slash command stays `/scientific-research` because Cursor shows the folder name. The bilingual new-user guide is `.agents/skills/scientific-research/docs/cursor-install.md`.

In this repository, `.cursor/skills/scientific-research` is a link to `.agents/skills/scientific-research`.

For every project on this machine:

```bash
.agents/skills/scientific-research/scripts/install-skill.sh cursor-user
```

The script copies the skill to `~/.cursor/skills/scientific-research/`. Copy `assets/researcher-profile.template.json` to `assets/researcher-profile.json` and fill your own five fields. `python3 scripts/policy.py profile` reads that file when `--path` is omitted. `--path` selects another file. A missing file stays incomplete. The skill does not invent a researcher, a reference, or a journal.

Version 2.0.0 keeps `verify-references`, `verify-journal`, `audit-methods`, and `audit` in `scripts/policy.py`. The `journal` command is a preliminary decision. An automated report is not proof that the study is valid. The `v2.0.0` tag and the GitHub Release are not published from this branch.
