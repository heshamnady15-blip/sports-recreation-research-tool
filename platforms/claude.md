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
python3 .agents/skills/scientific-research/scripts/package_skill.py --output dist/scientific-research.zip
```

جذر الأرشيف يحتوي `SKILL.md`. حساب claude.ai الذي يزامن المهارات يجعلها متاحة في الجلسات المرتبطة بذلك الحساب، وفق وثيقة Claude Code.

## الاستخدام

الطلب نفسه المستعمل في Cursor. اذكر المنتج (بحث أصيل، ترقية، رسالة، مراجعة منهجية، تحليل بعدي، أو تحويل رسالة إلى مقال) واللغة. Claude يتبع `SKILL.md` ويقرأ مراجع المهارة عند الحاجة.
