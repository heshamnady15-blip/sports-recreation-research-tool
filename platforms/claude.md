# التثبيت والاستخدام في Claude

مصدر الصيغة: https://code.claude.com/docs/en/skills

هذا المستودع يضع المهارة في `.claude/skills/scientific-research/` عبر رابط إلى `.agents/skills/scientific-research/`. Claude Code يحمّل مهارات المشروع من `.claude/skills/` ومهارات المستخدم من `~/.claude/skills/`.

## Claude Code

1. افتح المستودع في Claude Code. المهارة متاحة في جلسات هذا المشروع.
2. للاستعمال في كل المشروعات:

```bash
.agents/skills/scientific-research/scripts/install-skill.sh claude-user
```

3. استدعها بالأمر `/scientific-research` أو بطلب يقع ضمن وصف المهارة.

## claude.ai

إذا كانت شاشة Skills ظاهرة في حسابك، ارفع مجلد `scientific-research` أو الأرشيف الذي يُنتجه:

```bash
python3 .agents/skills/scientific-research/scripts/package_skill.py --output dist/scientific-research-2.0.0.zip
```

جذر الأرشيف يحتوي `SKILL.md`. حساب claude.ai الذي يزامن المهارات يجعلها متاحة في الجلسات المرتبطة بذلك الحساب، وفق وثيقة Claude Code.

## الاستخدام

الطلب نفسه المستعمل في Cursor. اذكر المنتج (بحث أصيل، ترقية، رسالة، مراجعة منهجية، تحليل بعدي، أو تحويل رسالة إلى مقال) واللغة. Claude يتبع `SKILL.md` ويقرأ مراجع المهارة عند الحاجة.

الإصدار 2.0.0 يبقى اسم المهارة `scientific-research` في المسار نفسه. أوامر تدقيق DOI والمجلة والمنهج موثقة في `SKILL.md`، وتعذر الاتصال بمصدر خارجي يبقى «غير متحقق منها» ولا يتحول إلى نجاح. `python3 scripts/policy.py profile` يقرأ `assets/researcher-profile.json` عند غياب `--path`.

## Install and use in Claude

The skill command is `/scientific-research`. Claude Code reads the project skill from `.claude/skills/scientific-research/`, which links to `.agents/skills/scientific-research/`. For every project on this machine:

```bash
.agents/skills/scientific-research/scripts/install-skill.sh claude-user
```

On claude.ai, upload `dist/scientific-research-2.0.0.zip` when the Skills screen is available. The archive root contains `SKILL.md`. It does not contain a filled researcher profile or the GfA Active Ageing study files.

`python3 scripts/policy.py profile` reads `assets/researcher-profile.json` when `--path` is omitted. Name the product and the language in the request. A failed connection to an external source stays unverified. Version 2.0.0 is prepared for review and has not been tagged.
