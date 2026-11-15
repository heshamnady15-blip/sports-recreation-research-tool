# تثبيت المهارة في Cursor لمستخدم جديد

# Install the skill in Cursor for a new user

الاسم الظاهر: **El-Nady Scientific Research Assistant**.  
المؤلف: **Dr. Hesham El-Nady**.  
الأمر الذي تكتبه في المحادثة: `/scientific-research`.

Cursor shows the folder name in the slash menu. That name is `scientific-research`. The public title and the author live in the skill description, in `assets/skill-identity.json`, and in Customize as the description text. Cursor does not replace the slash command with the public title.

## الطريق 1: نسخ المهارة فقط / Path 1: copy only the skill

يحتاج هذا الطريق إلى Git وPython 3.9 أو أحدث. لا يحتاج إلى ملفات دراسة GfA Active Ageing.

```bash
git clone https://github.com/heshamnady15-blip/sports-recreation-research-tool.git
cd sports-recreation-research-tool
.agents/skills/scientific-research/scripts/install-skill.sh cursor-user
python3 ~/.cursor/skills/scientific-research/scripts/capability_probe.py
```

الناتج المتوقع للسطر الأخير قائمة وظائف. وظائف DOI والمجلة معلّمة بأنها تحتاج إلى إنترنت. لا يثبت هذا الأمر مجلة ولا مرجعًا.

Then reload Cursor, open Customize, then Skills. The skill appears as `scientific-research`. Its description begins with El-Nady Scientific Research Assistant, by Dr. Hesham El-Nady.

في محادثة الوكيل:

```text
/scientific-research
جهّز خطة مراجعة منهجية عن الجمباز للجميع لكبار السن في الأندية، بنسختين عربية وإنجليزية. لا تقترح مجلة قبل التحقق من فهرسة Scopus ورسوم المؤلف.
```

## الطريق 2: فتح المستودع نفسه / Path 2: open this repository

1. افتح المجلد في Cursor.
2. المهارة محمّلة من `.cursor/skills/scientific-research`، وهو رابط إلى `.agents/skills/scientific-research`.
3. اكتب `/scientific-research`.

هذا الطريق يفتح أيضًا مثال الدراسة. المثال ليس مطلوبًا لتشغيل المهارة.

## أوامر عملية بعد التثبيت / Practical commands after install

استبدل المسار إذا ثبّتت المهارة داخل المستودع فقط.

```bash
SKILL=~/.cursor/skills/scientific-research
cd "$SKILL"

python3 scripts/policy.py profile

python3 scripts/policy.py similarity --product original

python3 scripts/policy.py similarity --product promotion --snapshot

python3 scripts/policy.py journal \
  --index scopus \
  --quartile Q1 \
  --apc-mandatory false \
  --publication-year 2026

python3 scripts/policy.py audit-methods --path manuscript.md
```

الأمر الثالث يقرأ لقطة الترقية المحلية المؤرخة في `references/official-snapshot.json`. لا يفتح صفحة المجلس الأعلى للجامعات. الأمر الرابع بلا مصدري الفهرسة والرسوم يعيد `unverified` ولا يوصي بمجلة.

للتحقق الخارجي، جهّز `references.json` بنفسك ثم:

```bash
python3 scripts/policy.py verify-references --path references.json
python3 scripts/policy.py verify-references --path references.json --offline
```

`--offline` يجب أن يبقي المرجع «غير متحقق منها» إذا كان الفحص يحتاج إلى Crossref أو DataCite.

## ملف الباحث / Researcher profile

```bash
cp assets/researcher-profile.template.json assets/researcher-profile.json
python3 scripts/policy.py profile
```

املأ الحقول الخمسة ببياناتك. لا تضع اسم مؤلف المهارة مكان اسمك. الأمر بلا `--path` يقرأ `assets/researcher-profile.json`. إذا لم يوجد الملف تبقى النتيجة غير مكتملة وتُطلب الحقول. لتحديد ملف آخر:

```bash
python3 scripts/policy.py profile --path /path/to/researcher-profile.json
```

الملف الناتج يبقى خارج Git عند التثبيت من المستودع، وسكربت التثبيت يحذفه من النسخة المنسوخة إن وُجد.

Fill the five fields with your own data. Do not enter the skill author's name in place of yours. Without `--path`, the command reads `assets/researcher-profile.json`. A missing file stays incomplete. `--path` selects a different file. The install script removes a filled profile from the copied skill, and Git ignores that file in this repository.

## التحديث / Update

```bash
cd sports-recreation-research-tool
git pull
.agents/skills/scientific-research/scripts/install-skill.sh cursor-user
```

مهارات `~/.cursor/skills/` تبقى على جهازك إلى أن تفعّل Sync Skills for Cloud Agents من Settings ثم Agents ثم Context and Tools. المزامنة لا تشارك المهارة مع باحثين آخرين. المشاركة موضحة في `docs/distribution-plan.md`.

## ما لا يكفي للتثبيت من واجهة Cursor وحدها / What the Cursor screen does not do yet

Cursor لا يستورد مهارة من رابط GitHub مباشرة. الاستيراد للآخرين يتم بنسخ المجلد، أو بتثبيت إضافة بعد اعتمادها في سوق Cursor. ملف `.cursor-plugin/plugin.json` في المستودع مرشح توزيع ولم يُرسل إلى السوق.
