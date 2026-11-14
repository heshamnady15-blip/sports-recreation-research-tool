#!/usr/bin/env python3
"""Build GfA Active Ageing document version 2.1. Originals are not overwritten."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "v2.1"

SESSIONS = [
    (1, "I", 1, "30–35", "التعارف والإيقاع", "Introductions and rhythm", "حركة الذراعين والقدمين من الجلوس وتقليد إيقاع بسيط", "Seated arm and foot movements and simple rhythm imitation", "اختيار أغنية مناسبة والتعارف", "Choose suitable music and make introductions"),
    (2, "I", 1, "30–35", "مرونة الأطراف العليا", "Upper-limb mobility", "رفع الذراعين في المدى المريح وتحريك الكتفين", "Comfortable-range arm raising and shoulder movement", "ابتكار حركة تحية جماعية", "Create a shared greeting movement"),
    (3, "I", 1, "30–35", "التوافق مع الموسيقى", "Coordination with music", "حركات متبادلة للذراعين والقدمين", "Alternating arm and foot movements", "اختيار ترتيب الحركات", "Choose the movement order"),
    (4, "I", 2, "30–35", "التوافق الثنائي", "Paired coordination", "حركات متماثلة ثم متبادلة للأطراف", "Symmetrical then alternating limb movements", "نشاط المرآة بين المشاركين في الجلسة", "Partner mirroring during the session"),
    (5, "I", 2, "30–35", "الكرة الإسفنجية", "Soft-ball play", "تمرير كرة خفيفة والتقاطها من الجلوس", "Seated passing and receiving of a light ball", "دائرة تمرير جماعية", "Group passing circle"),
    (6, "I", 2, "30–35", "السلسلة الأولى", "First movement sequence", "ربط 3–4 حركات بسيطة مع راحة", "Link 3–4 simple movements with rests", "اختيار اسم للسلسلة", "Name the sequence"),
    (7, "II", 3, "35–45", "القيام والجلوس", "Adapted sit-to-stand", "القيام المدعوم عند السماح الصحي؛ ومد الركبة بديلًا", "Supported sit-to-stand only when health screening allows; seated knee extension as the alternative", "اختيار تسلسل آمن", "Select a safe sequence"),
    (8, "II", 3, "35–45", "نقل الوزن", "Weight shifting", "نقل الوزن جلوسًا أو وقوفًا مدعومًا", "Seated or supported-standing weight shifts", "تبادل قيادة الحركة", "Take turns leading"),
    (9, "II", 3, "35–45", "توافق الجذع والذراعين", "Trunk and arm coordination", "الوصول للأمام والجانبين ضمن مدى مريح", "Comfortable forward and lateral reaching", "تشكيل حركي ثنائي", "Paired movement pattern"),
    (10, "II", 4, "35–45", "الوصول الوظيفي", "Functional reaching", "الوصول إلى أهداف قريبة ضمن حدود الاتزان", "Reach nearby targets within balance limits", "لعبة أهداف غير تنافسية", "Noncompetitive target game"),
    (11, "II", 4, "35–45", "التمرير والاستقبال", "Passing and receiving", "تمرير كرة خفيفة في اتجاهات متعددة", "Light-ball passing in several directions", "اختيار مسار الكرة", "Choose the passing route"),
    (12, "II", 4, "35–45", "سلسلة جماعية قصيرة", "Short group sequence", "ربط حركات الأطراف والتوازن", "Link limb and balance movements", "ترتيب سلسلة جماعية داخل الجلسة", "Arrange a group sequence during the session"),
    (13, "II", 5, "35–45", "وظيفة الأطراف السفلية", "Lower-limb function", "مد الركبة والقيام المعدل حسب الفحص الصحي", "Seated knee extension or adapted sit-to-stand according to health screening", "اختيار البديل الفردي المناسب", "Choose the suitable individual alternative"),
    (14, "II", 5, "35–45", "الخطو المعدل", "Adapted stepping", "خطوات مدعومة أو محاكاة الخطو من الجلوس", "Supported stepping or seated step simulation", "اختيار إيقاع جماعي", "Choose a group rhythm"),
    (15, "II", 5, "35–45", "لعبة حركية تعاونية", "Cooperative movement game", "تنسيق التمرير والوصول والإيقاع", "Combine passing, reaching, and rhythm", "تطوير قواعد لعب آمنة داخل الجلسة", "Develop safe game rules during the session"),
    (16, "III", 6, "40–50", "مراجعة السلاسل", "Sequence review", "مراجعة الحركات السابقة دون زيادة مفاجئة", "Review learned movements without a sudden increase", "اختيار الحركات المفضلة", "Select preferred movements"),
    (17, "III", 6, "40–50", "تشكيلات ثنائية", "Paired formations", "حركات متزامنة بمناديل خفيفة", "Synchronized movement with light scarves", "اختيار الثنائيات", "Choose partners"),
    (18, "III", 6, "40–50", "تشكيل جماعي", "Group formation", "تنسيق حركات من أماكن ثابتة", "Coordinate movements from stable positions", "اختيار شكل المجموعة", "Choose the group shape"),
    (19, "III", 7, "40–50", "التوازن حسب القدرة", "Adapted balance", "نقل الوزن واتزان مدعوم أو بديل من الجلوس", "Supported balance or a seated alternative", "تبادل قيادة الإيقاع", "Rotate rhythm leadership"),
    (20, "III", 7, "40–50", "الإيقاع الجماعي", "Group rhythm", "حركات متتابعة للذراعين والقدمين", "Sequential arm and foot movements", "اختيار الموسيقى", "Choose the music"),
    (21, "III", 7, "40–50", "ترتيب داخل الجلسة", "In-session sequence choice", "ربط الحركات المختارة أثناء الجلسة", "Link movements selected during the session", "التصويت على الترتيب", "Vote on the order"),
    (22, "III", 8, "40–50", "التنسيق الجماعي", "Group coordination", "تمرير متتابع وحركات إيقاعية", "Sequential passing and rhythmic movement", "توزيع الأدوار", "Allocate roles"),
    (23, "III", 8, "40–50", "وظيفة خفيفة وتوافق", "Light function and coordination", "حركات وظيفية معتدلة حسب التحمل", "Adapted functional movements as tolerated", "اختيار البدائل", "Choose alternatives"),
    (24, "III", 8, "40–50", "الانتقال بين التشكيلات", "Formation transitions", "تغيير اتجاه الحركة أو ترتيبها بأمان", "Safe changes of direction or order", "اعتماد تشكيل ثابت عند الحاجة", "Use a stationary formation when needed"),
    (25, "III", 9, "40–50", "حركة متعددة المكونات", "Multicomponent movement", "دمج خفيف للقوة والتوازن والتوافق", "Combine light strength, balance, and coordination", "اختيار تسلسل مشترك", "Choose a shared sequence"),
    (26, "III", 9, "40–50", "تدريب السلسلة", "Sequence rehearsal", "تكرار السلسلة مع راحة", "Rehearse the sequence with rests", "تبادل الملاحظات", "Exchange feedback"),
    (27, "III", 9, "40–50", "مراجعة تشاركية", "In-session review", "تعديل الحركات التي يجدها الحاضرون صعبة", "Modify movements the people present find difficult", "الاتفاق على التعديل داخل الجلسة", "Agree the change during the session"),
    (28, "IV", 10, "45–60", "الحركات المفضلة", "Preferred movements", "تكرار أنشطة المراحل السابقة", "Repeat preferred earlier activities", "اختيار محتوى هذه الجلسة", "Choose this session's content"),
    (29, "IV", 10, "45–60", "الانتقالات الآمنة", "Safe transitions", "التبديل بين الجلوس والوقوف عند السماح الصحي", "Sitting and standing transitions only when health screening allows", "تحديد تسلسل شخصي", "Set a personal sequence"),
    (30, "IV", 10, "45–60", "التحضير لعرض اختياري", "Optional showcase preparation", "تنسيق حركات جماعية غير تنافسية", "Coordinate noncompetitive group movement", "اختيار المشاركة أو نشاط بديل", "Opt in or choose an alternative activity"),
    (31, "IV", 11, "45–60", "مراجعة التوازن", "Balance review", "تكرار مهارات التوازن والتوافق", "Review balance and coordination", "قيادة بعض الفقرات", "Lead selected parts"),
    (32, "IV", 11, "45–60", "السلسلة الجماعية", "Group sequence", "تنفيذ السلسلة وفق القدرة", "Perform the sequence according to ability", "تعديل التشكيلات", "Adjust formations"),
    (33, "IV", 11, "45–60", "نشاط يختاره الحاضرون", "Activity chosen in session", "لعبة حركية آمنة يختارها الحاضرون", "A safe movement game chosen by the people present", "تصويت جماعي", "Group vote"),
    (34, "IV", 12, "45–60", "المراجعة الوظيفية", "Functional review", "مراجعة الوصول والقيام المعدل والتوافق", "Review reaching, adapted sit-to-stand, and coordination", "اختيار أنشطة يمكن الاستمرار عليها", "Select activities that could continue"),
    (35, "IV", 12, "45–60", "احتفال غير تنافسي", "Noncompetitive celebration", "عرض اختياري أو نشاط بديل", "Optional showcase or an alternative activity", "الاحتفاء بالمشاركة دون تصوير أو تسجيل", "Celebrate participation without photography or recording"),
    (36, "IV", 12, "45–60", "جلسة الاستمرار", "Continuation session", "حركات مفضلة ثم تهدئة", "Preferred movements and cool-down", "مناقشة إمكانية الاستمرار وتقبل البرنامج كتابة", "Discuss continuation and record acceptability in writing"),
]

DOSE = "التكرارات والشدة والراحة وقواعد التدرج: معلّقة حتى الفحص الصحي ومراجعة الاستطلاع. لا تُوصف في هذا الإصدار. / Repetitions, intensity, rest, and progression rules: pending health screening and pilot review. Not prescribed in this version."
ADAPT = "بديل الجلوس متاح. الوقوف المدعوم فقط بعد السماح الصحي. لا يُفترض وقوف مستقل موحّد. تُسمح فواصل الراحة. / A seated option is available. Supported standing only after health clearance. Independent standing is not assumed. Rest breaks are allowed."


def _doc() -> Document:
    document = Document()
    section = document.sections[0]
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(1.5)
    section.right_margin = Cm(1.5)
    style = document.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    return document


def add_h(document: Document, text: str, level: int = 1) -> None:
    document.add_heading(text, level=level)


def add_p(document: Document, text: str) -> None:
    document.add_paragraph(text)


def add_pair(document: Document, arabic: str, english: str) -> None:
    add_p(document, arabic)
    add_p(document, english)


def add_table(document: Document, headers: list[str], rows: list[list[str]]) -> None:
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    for index, header in enumerate(headers):
        table.rows[0].cells[index].text = header
    for row in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row):
            cells[index].text = value
    document.add_paragraph("")


def banner(document: Document) -> None:
    add_h(document, "GfA Active Ageing — V2.1", 0)
    add_pair(
        document,
        "الإصدار 2.1، 14 نوفمبر 2026. مسودة تخطيط. هذا الملف لا يسجل موافقة أخلاقية، ولا ترخيص أداة، ولا نتيجة، ولا بيانات أشخاص، ولا حجم عينة محسوبًا.",
        "Version 2.1, 14 November 2026. Planning draft. This file records no ethics approval, instrument licence, result, personal data, or calculated sample size.",
    )
    add_pair(
        document,
        "النسخ الأصلية محفوظة في studies/gfa-active-ageing/original ولم تُستبدل. التصحيحات التالية داخلة في أقسامها الأصلية.",
        "The original files remain in studies/gfa-active-ageing/original and are not replaced. The corrections below sit in their original sections.",
    )


def design_block(document: Document) -> None:
    add_h(document, "التصميم المنفذ / Executed design", 2)
    add_pair(
        document,
        "التصميم المنفذ: غير مسمى في هذا الإصدار. توجد ثلاثة تصميمات بديلة، ويُسمى لاحقًا تصميم بديل واحد فقط بعد معرفة عدد دور الرعاية وإمكاناتها الميدانية: تخصيص عشوائي على مستوى الشخص، أو تخصيص عشوائي عنقودي على مستوى الدار، أو مقارنة شبه تجريبية مضبوطة. هذه المسودة لا تعتمد أي تصميم بديل تصميمًا منفذًا، وليست تجربة عشوائية.",
        "Executed design: not named in this version. Three alternative designs exist, and exactly one alternative design may be named later, after the number of care facilities and their field feasibility are known: individual-level randomization, cluster-randomization by facility, or a quasi-experimental controlled comparison. This draft names no alternative design as executed, and it is not a randomized trial.",
    )
    add_pair(
        document,
        "تعمية مقيمي النتائج مطلوبة إذا اعتُمد لاحقًا أي تصميم بديل من الثلاثة: التخصيص العشوائي على مستوى الشخص، والتخصيص العشوائي العنقودي على مستوى الدار، والمقارنة شبه التجريبية المضبوطة. الإجراء معلّق ولم يُنفذ. انكشاف التخصيص أو تعذر التعمية يُوثق كتابة: من انكشفت له المعلومة، ومتى، وما المعلومة، وأي قياسات تأثرت، ولماذا تعذرت التعمية. هذا التوثيق بلا تصوير وبلا تسجيل صوتي أو مرئي.",
        "Outcome-assessor blinding is required if any one of the three alternative designs is later adopted: individual-level randomization, cluster-randomization by facility, and the quasi-experimental controlled comparison. The procedure is pending and has not been carried out. Allocation unblinding, or an inability to blind, is documented in writing: who learned the allocation, when, what information was revealed, which assessments were affected, and why blinding could not be maintained. That record uses no photography and no audio or video.",
    )
    add_pair(
        document,
        "مجموعة المقارنة موجودة في الخطة: أنشطة اجتماعية منظمة من دون التمرين الوظيفي المخطط. فصل المكان والزمن بين المجموعتين معلّق حتى تُعرف الدور.",
        "A comparison group is in the plan: structured social activities without the planned functional exercise. Place and time separation between the groups is pending until the facilities are known.",
    )


def attendance_block(document: Document) -> None:
    add_h(document, "معادلات الحضور والالتزام / Attendance and adherence equations", 2)
    add_pair(
        document,
        "الجلسات المخططة للبرنامج الكامل: 36 جلسة لكل شخص ملتحق. الجلسة المتاحة فعلًا هي جلسة مخططة عُرضت على الشخص وهو ما زال ملتحقًا وقادرًا على تلقي العرض. الجلسة الملغاة، أو الجلسة بعد الانسحاب، ليست جلسة متاحة فعلًا.",
        "Planned sessions for the full program: 36 sessions for each enrolled person. A session actually available is a planned session offered to the person while that person was still enrolled and able to receive the offer. A cancelled session, or a session after withdrawal, is not a session actually available.",
    )
    add_pair(
        document,
        "نسبة الحضور = الجلسات المتاحة التي حُضرت ÷ الجلسات المتاحة فعلًا. إذا عُرضت كل الجلسات المخططة على كل الملتحقين، صار المقام = عدد الملتحقين × 36.",
        "Attendance proportion = available sessions attended ÷ sessions actually available. When every planned session is offered to every enrolled person, the denominator equals the enrolled count × 36.",
    )
    add_pair(
        document,
        "نسبة التزام المكونات في جلسة نُفذت = المكونات الأساسية المنفذة ÷ المكونات الأساسية المخططة لتلك الجلسة. المدة تُسجل منفصلة عن الحضور. عتبة تحليل per-protocol معلّقة حتى اعتماد الجرعة، وهذا التحليل ليس تحليلًا تأكيديًا.",
        "Component adherence for a delivered session = core components delivered ÷ core components planned for that session. Duration is recorded separately from attendance. The per-protocol threshold stays pending until the dose is adopted, and that analysis is not a confirmatory analysis.",
    )


def outcome_block(document: Document) -> None:
    add_h(document, "النتائج / Outcomes", 2)
    add_pair(
        document,
        "نتيجة الدراسة اللاحقة الأساسية، لا نتيجة إثبات فاعلية للاستطلاع: مجموع SPPB من 0 إلى 12 عند الأسبوع 12 بعد ضبط قياس البداية. النسخة والترخيص وطريقة التصحيح معلّقة.",
        "The later study's single primary outcome, not a pilot efficacy result: total SPPB from 0 to 12 at week 12, adjusted for the baseline score. Version, licence, and scoring rules are pending.",
    )
    add_pair(
        document,
        "OPQOL-Brief مرشحة لنتيجة ثانوية عن جودة الحياة، رهن النسخة العربية والإذن والتصحيح. LSNS-6 مرشحة لنتيجة ثانوية عن شبكة الأسرة والأصدقاء فقط. LSNS-6 لا يقيس الترابط الاجتماعي داخل الدار. أداة الترابط داخل الدار غير مختارة في هذا الإصدار ومعلّقة، ولا يُنسب أثر إليها.",
        "OPQOL-Brief is a candidate secondary outcome for quality of life, subject to an Arabic version, permission, and scoring rules. LSNS-6 is a candidate secondary outcome for the family and friend network only. LSNS-6 does not measure within-facility social connectedness. No within-facility connectedness instrument is selected in this version; that choice is pending, and no effect is attributed to it.",
    )
    add_pair(
        document,
        "نقاط القياس: T0 قبل البرنامج، وT1 في الأسبوع 12. T2 في الأسبوع 20 معلّق. الاستطلاع يصف الجدوى ولا يختبر الفاعلية.",
        "Assessment times: T0 before the program and T1 at week 12. T2 at week 20 is pending. The pilot describes feasibility and does not test efficacy.",
    )


def dose_block(document: Document) -> None:
    add_pair(document, DOSE.split(" / ")[0], DOSE.split(" / ")[1])


def pending_items() -> list[str]:
    return [
        "التصميم المنفذ ووحدة التخصيص بعد معرفة عدد الدور / Executed design and allocation unit after the facility count is known",
        "أسماء الدور وعددها / Facility names and count",
        "معايير الأهلية والموانع الصحية / Eligibility criteria and health contraindications",
        "حجم العينة ومعامل التجمع عند الحاجة / Sample size and the clustering coefficient if needed",
        "التكرارات والشدة والراحة وقواعد التدرج / Repetitions, intensity, rest, and progression rules",
        "عتبة الالتزام لأي تحليل لاحق وفق البروتوكول / Adherence threshold for any later per-protocol analysis",
        "نسخ الأدوات وتراخيصها وتصحيحها، وأداة الترابط داخل الدار إن اختيرت لاحقًا / Instrument versions, licences, scoring, and a within-facility connectedness instrument if one is later chosen",
        "فصل المكان والزمن لمنع التلوث / Place and time separation for contamination control",
        "تنفيذ مرحلة البناء التشاركي المقترحة: البروتوكول مكتوب والتنفيذ لم يبدأ / Conduct of the proposed co-design phase: the protocol is written and delivery has not started",
        "تنفيذ تعمية مقيمي النتائج وتوثيق أي انكشاف: القاعدة مكتوبة والتنفيذ لم يبدأ / Carrying out outcome-assessor blinding and any unblinding record: the rule is written and has not been carried out",
        "تنفيذ T2 في الأسبوع 20 / Whether T2 at week 20 is conducted",
        "مجموعة المتغيرات الضابطة / Covariate set",
        "اختيار الخبراء وجمع تقديراتهم / Expert selection and collection of ratings",
        "الموافقات والتسجيل: غير مسجلة في هذه المسودة / Approvals and registration: not recorded in this draft",
        "هوية الفريق البحثي والبريد المؤسسي وORCID / Investigator identity, institutional email, and ORCID",
        "اختيار المجلة بعد فتح سجل الفهرسة وصفحة الرسوم / Journal selection after an indexing record and a fee page are opened",
    ]


def add_pending(document: Document) -> None:
    add_h(document, "قرارات معلّقة / Pending decisions", 2)
    for item in pending_items():
        document.add_paragraph(item, style="List Bullet")


def build_manual() -> None:
    document = _doc()
    banner(document)
    add_h(document, "1. الإطار البحثي / Research framework", 1)
    add_pair(
        document,
        "هذا الدليل يصف الجلسات الست والثلاثين للاستطلاع وللدراسة المقارنة اللاحقة. الاستطلاع لا يثبت الفاعلية. الاختيار داخل الجلسة جزء من التنفيذ. مرحلة البناء التشاركي السابقة بروتوكول مقترح مستقل في الملف GfA_Active_Ageing_CoDesign_Phase_Protocol_v2.1، ولم تبدأ، ولا تغني عن مجموعة المقارنة.",
        "This manual specifies the 36 sessions for the pilot and for the later comparative study. The pilot does not establish effectiveness. Choice during a session is part of delivery. The prior co-design phase has its own proposed protocol in GfA_Active_Ageing_CoDesign_Phase_Protocol_v2.1. It has not started, and it does not replace the comparison group.",
    )
    add_table(
        document,
        ["البند / Item", "المواصفة في V2.1 / V2.1 specification"],
        [
            ["الفئة / Population", "رجال وسيدات 60–75 سنة في دور رعاية بالقاهرة. الدور غير مسماة. / Men and women aged 60–75 in Cairo care homes. Facilities are not named."],
            ["الجلسات / Sessions", "12 أسبوعًا، 3 جلسات أسبوعيًا، 36 جلسة. / 12 weeks, 3 sessions a week, 36 sessions."],
            ["المدة / Duration", "الأسابيع 1–2: 30–35 دقيقة؛ 3–5: 35–45؛ 6–9: 40–50؛ 10–12: 45–60. / Weeks 1–2: 30–35 min; 3–5: 35–45; 6–9: 40–50; 10–12: 45–60."],
            ["الاختيار / In-session choice", "موسيقى وترتيب وتشكيل يختارها الحاضرون داخل الجلسة. / Music, order, and formation chosen by the people present during the session."],
            ["العرض / Showcase", "اختياري وغير تنافسي ومن دون تصوير أو تسجيل صوتي أو مرئي. / Optional, noncompetitive, and without photography or audio or video recording."],
            ["المقارنة / Comparison", "أنشطة اجتماعية منظمة بلا تمرين وظيفي مخطط. / Structured social activities without planned functional exercise."],
        ],
    )
    design_block(document)
    outcome_block(document)
    add_h(document, "2. بروتوكول الجلسة / Session protocol", 1)
    add_pair(
        document,
        "مثال بنية 45 دقيقة: إحماء 8 دقائق، نشاط وظيفي معدل 27 دقيقة، نشاط تعاوني 5 دقائق، تهدئة وملاحظات 5 دقائق. البنية تتقلص أو تمتد داخل مدى الأسبوع.",
        "An example 45-minute structure is an 8-minute warm-up, 27 minutes of adapted functional activity, 5 minutes of cooperative activity, and 5 minutes of cool-down and comments. The structure shortens or lengthens within the week's range.",
    )
    add_pair(
        document,
        "في كل جلسة: سؤال عن الأعراض، وبديل مناسب، وإحماء، وجزء حركي، واختيار داخل الجلسة، وتهدئة، وتسجيل الحضور والالتزام والسلامة.",
        "Every session includes a symptom check, a suitable alternative, warm-up, movement, an in-session choice, cool-down, and a record of attendance, fidelity, and safety.",
    )
    dose_block(document)
    add_p(document, ADAPT)
    add_h(document, "3. الجلسات الست والثلاثون / Thirty-six sessions", 1)
    add_table(
        document,
        ["#", "الأسبوع / Week", "الدقائق / Minutes", "النشاط", "Activity", "الاختيار داخل الجلسة / In-session choice", "الجرعة / Dose"],
        [
            [
                str(number),
                str(week),
                minutes,
                f"{arabic_title}: {arabic_activity}",
                f"{english_title}: {english_activity}",
                f"{arabic_choice} / {english_choice}",
                "معلّقة / Pending",
            ]
            for number, _phase, week, minutes, arabic_title, english_title, arabic_activity, english_activity, arabic_choice, english_choice in SESSIONS
        ],
    )
    add_p(document, ADAPT)
    add_h(document, "4. المجموعة المقارنة / Comparison group", 1)
    add_pair(
        document,
        "الجدول نفسه: ثلاث جلسات أسبوعيًا لاثني عشر أسبوعًا، مع تقريب زمن التواصل قدر الإمكان. لا تمارين وظيفية مخططة. تُسجل الرعاية المعتادة والنشاط الخارجي. أي حركة وظيفية غير مخططة تُسجل تلوثًا.",
        "The same three sessions a week for twelve weeks, with facilitator contact matched as far as practical. No planned functional exercise. Usual care and outside activity are logged. Any unplanned functional movement is logged as contamination.",
    )
    add_table(
        document,
        ["الأسابيع / Weeks", "النشاط / Activity"],
        [
            ["1–3", "تعارف وحوار وذكريات وألعاب ذهنية / Introductions, conversation, reminiscence, and cognitive games"],
            ["4–6", "قراءة جماعية ومناقشة وأنشطة ثقافية / Group reading, discussion, and cultural activities"],
            ["7–9", "أنشطة فنية بسيطة وحل مشكلات جماعية / Simple arts and collaborative problem-solving"],
            ["10–12", "أنشطة اجتماعية يختارها الحاضرون وتغذية راجعة مكتوبة، بلا مكونات التدخل الحركي / Social activities chosen by the people present and written feedback, without the intervention movement components"],
        ],
    )
    add_pair(
        document,
        "فصل المكان والزمن بين التدخل والمقارنة معلّق. حتى يُحسم، لا تُعد خطة منع التلوث قابلة للتنفيذ.",
        "Place and time separation between the intervention and the comparison is pending. Until it is decided, contamination control is not operational.",
    )
    add_h(document, "5. السلامة والالتزام / Safety and fidelity", 1)
    add_pair(
        document,
        "قبل الجلسة: فحص طبي معلّق، وأعراض حالية، وكرسي ثابت، وأرضية غير زلقة، وشرب، ووسيلة استدعاء. يُوقف النشاط عند ألم صدري أو دوار شديد أو ضيق نفس غير معتاد أو اضطراب اتزان مقلق، ثم تُتبع خطة الطوارئ عند اعتمادها.",
        "Before a session: health screening is pending, and the session checks current symptoms, a stable chair, a non-slip surface, drinking water, and a way to call for help. Activity stops for chest pain, marked dizziness, unusual breathlessness, or concerning instability, then follows the emergency plan once that plan is adopted.",
    )
    add_pair(
        document,
        "لا تصوير ولا تسجيل صوتي أو مرئي. الملاحظات المكتوبة فقط هي سجل التقبل في الاستطلاع. تعمية مقيمي النتائج وتوثيق الانكشاف هما القاعدة الواردة في قسم التصميم المنفذ، وهما معلّقان ولم يُنفذا.",
        "There is no photography and no audio or video recording. Written notes are the only pilot acceptability record. Outcome-assessor blinding and the unblinding record are the rule in the executed-design section. Assessor blinding is pending and has not been carried out.",
    )
    attendance_block(document)
    add_h(document, "6. الاستمارات الفارغة / Blank forms", 1)
    forms = [
        ("GFA-01 تنفيذ الجلسة / Session delivery", ["الدار / Facility", "التاريخ / Date", "رقم الجلسة / Session index", "الميسر / Facilitator", "المدة المخططة / Planned duration", "المدة الفعلية / Actual duration", "جلسات البرنامج المخططة / Planned program sessions: 36 for the full program", "هل هذه الجلسة متاحة فعلًا؟ / Was this session actually available?", "الحضور من الجلسات المتاحة / Attendance among sessions actually available", "المكونات المخططة / Planned components", "المكونات المنفذة / Delivered components", "التزام المكونات = المنفذة ÷ المخططة لهذه الجلسة المنفذة / Component adherence = delivered ÷ planned for this delivered session", "الاختيار داخل الجلسة / In-session choice", "التعديلات / Adaptations", "أحداث السلامة / Safety events", "ملاحظات / Notes"]),
        ("GFA-02 متابعة فردية / Individual participation", ["الرمز / Code", "الجلسة / Session", "هل الجلسة مخططة لهذا الشخص؟ / Was the session planned for this person?", "هل الجلسة متاحة فعلًا لهذا الشخص؟ / Was the session actually available to this person?", "هل حضر الجلسة المتاحة؟ / Attended the available session?", "دقائق المشاركة / Participation minutes", "جلوس أو دعم أو وقوف / Seated, supported, or standing", "الراحة / Rest breaks", "سبب الغياب أو التوقف أو عدم الإتاحة / Reason for absence, stop, or unavailability", "ملاحظات / Notes"]),
        ("GFA-03 حدث ضار / Adverse event", ["رمز الحدث / Event code", "رمز الشخص / Person code", "التاريخ والوقت / Date and time", "الوصف / Description", "النشاط وقت الحدث / Activity at the time", "الإجراء الفوري / Immediate response", "مراجعة المختص / Health-professional review", "الشدة / Severity", "المتابعة / Follow-up", "حالة الإبلاغ / Reporting status"]),
        ("GFA-04 الالتزام / Fidelity", ["الجلسة / Session", "المخطط / Planned", "المنفذ / Delivered", "المدة / Duration", "الموسيقى / Music", "الاختيار داخل الجلسة / In-session choice", "التعديلات / Modifications", "الانحرافات / Deviations", "المراجع / Reviewer", "حالة الجرعة / Dose status: pending", "عتبة per-protocol معلّقة وليست تحليلًا تأكيديًا / Per-protocol threshold pending and not a confirmatory analysis"]),
        ("GFA-05 الاختيار داخل الجلسة / In-session choice", ["الجلسة / Session", "خيارات الحركة / Movement options", "خيارات الموسيقى / Music options", "خيارات التشكيل / Formation options", "ما اختير / What was chosen", "ما لم يُعتمد وسببه / What was not adopted and why"]),
        ("GFA-06 المقارنة / Comparison", ["الدار / Facility", "التاريخ / Date", "الجلسة / Session", "النشاط الاجتماعي / Social activity", "الدقائق المخططة والفعلية / Planned and actual minutes", "الحضور / Attendance", "زمن التواصل / Facilitator contact", "تلوث حركي؟ / Movement contamination?", "الانحرافات / Deviations"]),
        ("GFA-07 التقبل / Acceptability", ["الرمز / Code", "التاريخ / Date", "سجل التقبل المعتمد للاستطلاع: ملاحظات مكتوبة فقط / Pilot acceptability record: written notes only", "بنود 1–5 للمتعة والملاءمة والصوت في القرار والتفاعل والرغبة في الاستمرار: مسودة غير معتمدة وليست نتيجة تحليل / Draft 1–5 items for enjoyment, suitability, voice, interaction, and willingness to continue: unvalidated and not an analysis outcome"]),
        ("GFA-08 سجل القياس / Measurement log", ["الرمز / Code", "المجموعة / Group", "تاريخ T0 / T0 date", "تاريخ T1 / T1 date", "تاريخ T2 إن نُفذ / T2 date if conducted", "حالة SPPB: مكتمل أو تعذر أداء حسب دليل الأداة أو غياب / SPPB status: complete, unable to perform per the instrument rules, or absent", "حالة OPQOL-Brief / OPQOL-Brief status", "حالة LSNS-6 / LSNS-6 status", "سبب النقص / Missingness reason", "رمز المقيم / Assessor code", "حالة تعمية المقيم: معلّقة / Assessor-blinding status: pending", "حالة إخفاء التخصيص: معلّقة / Allocation-concealment status: pending", "توثيق الانكشاف أو تعذر التعمية: من، ومتى، وما المعلومة، وأي قياسات، ولماذا / Unblinding or inability-to-blind record: who, when, what, which assessments, why", "نسخة الأداة وترخيصها: معلّقان / Instrument version and licence: pending"]),
    ]
    for title, fields in forms:
        add_h(document, title, 2)
        add_pair(document, "نموذج فارغ. لا تُدخل بيانات أشخاص.", "Blank form. Enter no personal data.")
        add_table(document, ["الحقل / Field", "الخانة / Entry"], [[field, "________"] for field in fields])
    add_h(document, "7. أمثلة افتراضية مستبعدة من التحليل / Fictional examples excluded from analysis", 1)
    add_pair(
        document,
        "الأمثلة التالية افتراضية لتعليم ملء الاستمارة فقط. ليست دور رعاية، ولا أشخاصًا، ولا أحداثًا، ولا نتائج، وتُستبعد من أي تحليل.",
        "The following examples are fictional and only show how to complete a form. They are not care homes, people, events, or results, and they are excluded from every analysis.",
    )
    add_table(
        document,
        ["الاستمارة / Form", "قيمة افتراضية / Fictional value"],
        [
            ["GFA-01", "دار افتراضية؛ 15/01/20XX؛ الجلسة 07؛ الميسر FAC-EX؛ 40 ثم 36 دقيقة؛ حضور 8؛ مكونات 4 مخططة و3 منفذة؛ لا حدث سلامة في المثال"],
            ["GFA-02", "رمز P-EX-001؛ جلسة 07؛ حاضر؛ 28 دقيقة؛ جلوس؛ فترتا راحة"],
            ["GFA-03", "رمز AE-EX-001؛ رمز P-EX-002؛ دوار بسيط افتراضي أثناء جلوس؛ أوقف المثال النشاط"],
            ["GFA-04", "جلسة 07؛ 4 مخطط و3 منفذ؛ 36 دقيقة؛ تأجيل مكون في المثال"],
            ["GFA-05", "حركتان ومقطوعتان؛ اعتماد إيقاع أبطأ في المثال"],
            ["GFA-06", "حوار وذكريات؛ 40/38 دقيقة؛ حضور 7؛ التلوث في المثال: لا"],
            ["GFA-07", "الملاحظات المكتوبة فقط هي السجل. درجات 1–5 في النسخة السابقة لا تُنقل إلى التحليل"],
            ["GFA-08", "T2 غير منفذ في المثال؛ لا درجات مقاييس؛ حالة التعمية معلّقة"],
        ],
    )
    add_h(document, "8. قائمة ما قبل التنفيذ / Pre-implementation checklist", 1)
    add_pending(document)
    add_pair(
        document,
        "اختيار المجلة معلّق. هذه المسودة لا توصي بمجلة، ولا تذكر ربعًا، ولا رسوم نشر، لأن سجل الفهرسة وصفحة الرسوم لم يُرفقا.",
        "Journal selection is pending. This draft recommends no journal and states no quartile and no publication fee, because no indexing record and no fee page are attached.",
    )
    document.save(OUT / "GfA_Active_Ageing_Bilingual_Intervention_Manual_v2.1.docx")


def build_pilot() -> None:
    document = _doc()
    banner(document)
    add_h(document, "A. البروتوكول العربي", 1)
    add_h(document, "عنوان الدراسة", 2)
    add_p(document, "دراسة استطلاعية لقابلية تنفيذ برنامج ترويحي للجمباز للجميع، مع اختيار داخل الجلسة، لدى الرجال والسيدات من 60 إلى 75 سنة المقيمين بدور الرعاية في القاهرة.")
    add_h(document, "الهدف", 2)
    add_p(document, "تقدير جدوى الاستقطاب والاحتفاظ والحضور واكتمال القياسات والالتزام والقبول المكتوب والسلامة. الدراسة الاستطلاعية لا تثبت الفاعلية.")
    add_h(document, "المكان", 2)
    add_p(document, "دور رعاية كبار السن في القاهرة. العدد والأسماء معلّقان. القدرات الحركية متفاوتة. معايير الاشتمال والاستبعاد والفحص الصحي معلّقة قبل أي استقطاب.")
    design_block(document)
    add_h(document, "التدخل", 2)
    add_p(document, "GfA Active Ageing: 12 أسبوعًا، 3 جلسات أسبوعيًا، 36 جلسة، 30–60 دقيقة حسب مدى الأسبوع والتحمل. الحركات من الجلوس أو الوقوف المدعوم بعد السماح الصحي. الموسيقى والاختيار داخل الجلسة. عرض ختامي اختياري غير تنافسي. لا تصوير ولا تسجيل.")
    dose_block(document)
    add_h(document, "المقارنة", 2)
    add_p(document, "أنشطة اجتماعية منظمة من دون تمرين وظيفي مقصود، مع تقريب زمن التواصل، وتسجيل الرعاية المعتادة والنشاط الخارجي. فصل المكان والزمن معلّق.")
    outcome_block(document)
    add_h(document, "مؤشرات الجدوى", 2)
    add_p(document, "مؤشرات الاستطلاع هي الاستقطاب، والاحتفاظ حتى الأسبوع 12، والحضور، واكتمال SPPB بين المؤهلين، واكتمال الاستبيانين، والتزام الميسر، والملاحظات المكتوبة للتقبل، والسلامة. سجل التقبل في الاستطلاع ملاحظات مكتوبة فقط. بنود الدرجات في GFA-07 مسودة غير معتمدة وليست مؤشرًا.")
    add_h(document, "تعريفات المقامات", 2)
    add_p(document, "مقام الاحتفاظ هو عدد الملتحقين. بسطه من بقي في الأسبوع 12.")
    attendance_block(document)
    add_p(document, "مقام الاستبيانات عند T1 هو عدد الملتحقين مضروبًا في أداتين: OPQOL-Brief وLSNS-6. البسط هو الاستمارات القابلة للتصحيح. إضافة T2 معلّقة وتغير المقام إذا اعتُمدت.")
    add_p(document, "مقام اكتمال SPPB هو عدد المؤهلين للتقييم حسب قواعد الأداة بعد اعتمادها. من يتعذر عليه الأداء حسب دليل الأداة لا يُحسب غيابًا عشوائيًا. قواعد الأهلية معلّقة.")
    add_h(document, "العينة والتحليل", 2)
    add_p(document, "حجم الاستطلاع معلّق. يُبرر لاحقًا بدقة نسب الجدوى وعدد الدور والتصميم بعد حسمه والانسحاب المتوقع. أثر استطلاعي لا يُستخدم وحده لتقدير حجم الدراسة اللاحقة.")
    add_p(document, "التحليل وصفي: أعداد ونسب ومقاماتها وفواصل ثقة مناسبة، وأسباب الفقد والانسحاب والانحراف والأحداث. لا اختبار تأكيدي للفاعلية. إذا سُمي لاحقًا التخصيص العشوائي العنقودي على مستوى الدار، يراعى التجمع في وصف الجدوى أيضًا. تحليل per-protocol ليس تحليلًا تأكيديًا.")
    add_h(document, "العتبات الأولية للانتقال", 2)
    add_p(document, "عتبات أولية غير معتمدة: الاحتفاظ 85% أو أكثر، اكتمال SPPB بين المؤهلين 90% أو أكثر، الحضور 80% أو أكثر، اكتمال الاستبيانات 85% أو أكثر. تبقى معلّقة حتى مراجعة الخبراء ومعلومات السلامة والتصميم. لا تُستخدم وحدها لقرار الانتقال.")
    add_h(document, "السلامة", 2)
    add_p(document, "يُوقف النشاط عند ألم صدري أو دوار شديد أو ضيق نفس غير معتاد أو اضطراب اتزان مقلق. خطة الطوارئ والإبلاغ معلّقة. تعمية مقيمي النتائج وتوثيق انكشاف التخصيص أو تعذر التعمية هما القاعدة في فقرة التصميم المنفذ، وهما معلّقان ولم يُنفذا.")
    add_h(document, "B. English protocol", 1)
    add_p(document, "Title: pilot feasibility study of a Gymnastics for All recreational program, with in-session choice, among men and women aged 60–75 living in Cairo residential care facilities.")
    add_p(document, "Purpose: estimate recruitment, retention, attendance, measurement completion, fidelity, written acceptability, and safety. The pilot does not establish efficacy.")
    add_p(document, "Setting and population: Cairo care homes, names and count pending. Mobility is heterogeneous. Eligibility, exclusion, and health screening are pending before any recruitment.")
    add_p(document, "Intervention: 12 weeks, three sessions a week, 36 sessions, 30–60 minutes by week range and tolerance. Movement is seated, or supported standing after health clearance. Music and other choices occur in the session. The closing showcase is optional and noncompetitive. There is no recording.")
    add_p(document, "Comparator: structured social activities without intended functional exercise, with contact time matched as far as practical. Usual care and outside activity are logged. Place and time separation is pending.")
    add_p(document, "Feasibility endpoints: recruitment, retention to week 12, attendance, SPPB completion among people eligible for assessment, completion of the two questionnaires, facilitator fidelity, written acceptability notes, and safety. Written notes are the only pilot acceptability record. The 1–5 draft items on GFA-07 are not an endpoint.")
    add_p(document, "Retention denominator: enrolled count. Numerator: still in the study at week 12.")
    add_p(document, "Planned sessions for the full program: 36 sessions for each enrolled person. A session actually available is a planned session offered while the person was still enrolled and able to receive the offer. A cancelled session, or a session after withdrawal, is not a session actually available.")
    add_p(document, "Attendance proportion = available sessions attended ÷ sessions actually available. When every planned session is offered to every enrolled person, the denominator equals the enrolled count multiplied by 36.")
    add_p(document, "Component adherence for a delivered session = core components delivered ÷ core components planned for that session. The per-protocol threshold stays pending until the dose is adopted, and that analysis is not a confirmatory analysis.")
    add_p(document, "T1 questionnaire denominator: enrolled count multiplied by two instruments, OPQOL-Brief and LSNS-6. Numerator: scorable forms. Adding T2 is pending and would change the denominator.")
    add_p(document, "SPPB completion denominator: count eligible for assessment under the instrument rules once those rules are adopted. Inability to perform, scored by those rules, is not treated as an ordinary absence. Eligibility rules are pending.")
    add_p(document, "Pilot sample size is pending. It will be justified from the precision of feasibility proportions, the facility count, the design after it is named, and expected attrition. An unstable pilot efficacy estimate is not the sole basis for the later sample size.")
    add_p(document, "Analysis is descriptive, with counts, proportions, denominators, and suitable confidence intervals, plus reasons for missingness, withdrawal, deviation, and adverse events. There is no confirmatory efficacy test. If cluster-randomization by facility is later named, clustering is also respected in the feasibility description. A per-protocol analysis is not a confirmatory analysis.")
    add_p(document, "Provisional progression thresholds, not adopted: retention at least 85 percent, eligible SPPB completion at least 90 percent, attendance at least 80 percent, questionnaire completion at least 85 percent. They stay pending expert review and safety and design information. They are not used alone.")
    add_p(document, "Stop activity for chest pain, marked dizziness, unusual breathlessness, or concerning instability. The emergency and reporting plan is pending. Outcome-assessor blinding and the written unblinding record follow the executed-design section. Assessor blinding is pending and has not been carried out.")
    add_h(document, "C. Readiness checklist PILOT-R01", 1)
    add_p(document, "Blank form. Mark Yes, No, or Pending. Attach evidence only when it exists. This draft marks no item Yes.")
    add_table(
        document,
        ["البند / Item", "الحالة / Status", "الدليل / Evidence", "المسؤول / Owner"],
        [[item, "Pending", "________", "________"] for item in [
            "موافقة لجنة الأخلاقيات / Ethics committee decision",
            "موافقات دور الرعاية / Care-home permissions",
            "إجراء الموافقة الفردية / Individual consent process",
            "الفحص الصحي ومسار الإحالة / Health screening and referral",
            "الطوارئ والإبلاغ / Emergency response and reporting",
            "تأهيل الفريق / Staff preparation",
            "استقلال المقيم وتعميته / Independent assessor and blinding",
            "اعتماد دليل الجلسات الست والثلاثين / Adoption of the 36-session manual",
            "دليل المقارنة وفصل المكان والزمن / Comparison manual and place-time separation",
            "صلاحية الأدوات والإذن / Instrument suitability and permission",
            "حسم التخصيص / Allocation decision",
            "مبرر حجم الاستطلاع / Pilot sample-size rationale",
            "نظام بيانات مرمز / Coded data system",
            "قرار التسجيل / Registration decision",
            "استمارات الالتزام والسلامة / Fidelity and safety forms",
        ]],
    )
    add_h(document, "D. Feasibility tracking PILOT-R02", 1)
    add_table(
        document,
        ["المؤشر / Indicator", "البسط / Numerator", "المقام / Denominator", "المستهدف الأولي / Provisional target"],
        [
            ["الاحتفاظ حتى الأسبوع 12 / Retention to week 12", "_____", "الملتحقون / Enrolled count _____", "85% أو أكثر / at least 85%"],
            ["اكتمال SPPB / SPPB completion", "_____", "المؤهلون للتقييم / Eligible for assessment _____", "90% أو أكثر / at least 90%"],
            ["الحضور / Attendance", "الجلسات المتاحة التي حُضرت / Available sessions attended _____", "الجلسات المتاحة فعلًا. عند عرض كل المخطط: الملتحقون × 36 / Sessions actually available. When every planned session is offered: enrolled count × 36", "80% أو أكثر / at least 80%"],
            ["اكتمال الاستبيانات عند T1 / T1 questionnaire completion", "_____", "الملتحقون × 2 / Enrolled count × 2", "85% أو أكثر / at least 85%"],
            ["الأحداث الضارة / Adverse events", "العدد / Count _____", "جلسات التعرض / Exposure sessions _____", "مراجعة مستقلة / Independent review"],
        ],
    )
    add_p(document, "تُثبت تعريفات المقامات قبل بدء الجمع. / Lock the denominator definitions before collection begins.")
    add_h(document, "E. Progression decision PILOT-R03", 1)
    add_table(
        document,
        ["المجال / Domain", "التقييم / Assessment", "الدليل / Evidence"],
        [[item, "☐ Green  ☐ Amend  ☐ Stop", "________________"] for item in [
            "الاحتفاظ / Retention",
            "اكتمال SPPB / SPPB completion",
            "الحضور / Attendance",
            "الاستبيانات / Questionnaires",
            "السلامة / Safety",
            "الموافقات: الحالة في هذه المسودة معلّقة / Approvals: status in this draft is pending",
            "التخصيص والتلوث / Allocation and contamination",
            "الالتزام / Fidelity",
            "إمكانات الدور / Facility feasibility",
        ]],
    )
    add_p(document, "القرار: ☐ الاستمرار  ☐ تعديل وإعادة اختبار  ☐ عدم الانتقال. المبرر: ________  مراجع السلامة: ________  التاريخ: ________")
    add_p(document, "Decision: ☐ Proceed unchanged  ☐ Amend and re-pilot  ☐ Do not proceed. Rationale: ________  Safety reviewer: ________  Date: ________")
    add_h(document, "F. أمثلة حسابية افتراضية مستبعدة من النتائج / Fictional arithmetic excluded from results", 1)
    add_pair(
        document,
        "الحساب التالي يشرح المقامات فقط. ليس ملاحظة ميدانية ولا قرار انتقال.",
        "The following arithmetic only shows the denominators. It is not a field observation and not a progression decision.",
    )
    add_table(
        document,
        ["المؤشر / Indicator", "حساب افتراضي / Fictional arithmetic", "القراءة / Reading"],
        [
            ["الاحتفاظ / Retention", "17/20 = 85%", "يلامس المستهدف الأولي في المثال فقط / Meets the provisional target in the example only"],
            ["اكتمال SPPB / SPPB completion", "16/18 = 88.9%", "دون 90% في المثال فقط / Below 90% in the example only"],
            ["الحضور / Attendance", "576/(20×36) = 576/720 = 80%", "المثال يفترض أن كل الجلسات المخططة كانت متاحة فعلًا، فيساوي المقام 20 × 36 = 720، لا 600 / The example assumes every planned session was actually available, so the denominator is 20 × 36 = 720, not 600"],
            ["الاستبيانات / Questionnaires", "33/(20×2) = 33/40 = 82.5%", "دون 85% في المثال فقط / Below 85% in the example only"],
        ],
    )
    add_p(document, "مثال قرار PILOT-R03: تعديل الإجراءات قبل أي استقطاب للدراسة اللاحقة. هذا مثال، لا استنتاج دراسة.")
    add_p(document, "Illustrative PILOT-R03 decision: amend procedures before any later-study recruitment. This is an example, not a study conclusion.")
    add_h(document, "G. القرارات المعلقة في موضعها / Pending decisions in place", 1)
    add_pending(document)
    document.save(OUT / "GfA_Active_Ageing_Pilot_Protocol_Step21_v2.1.docx")


def build_expert() -> None:
    document = _doc()
    banner(document)
    add_h(document, "A. التعليمات / Instructions", 1)
    add_pair(
        document,
        "لم يُستقطب خبير، ولم تُجمع درجات، ولم يُحسب معامل. قيّم بشكل مستقل الملاءمة والوضوح وقابلية التنفيذ والسلامة. المقياس المقترح من 1 إلى 4: 1 غير ملائم، 2 ملائم بدرجة محدودة، 3 ملائم بدرجة جيدة، 4 ملائم بدرجة عالية. الدرجات لا تغني عن الفحص الصحي.",
        "No expert has been recruited, no ratings have been collected, and no coefficient has been calculated. Independently rate relevance, clarity, feasibility, and safety. The proposed scale is 1 to 4: 1 not relevant, 2 somewhat relevant, 3 quite relevant, 4 highly relevant. Ratings do not replace health screening.",
    )
    add_p(document, "رمز الخبير / Expert code: ________  التخصص / Discipline: ________  سنوات الخبرة / Years of experience: ________")
    add_h(document, "B. التحكيم العام بأربعة أبعاد / Overall rating on four dimensions", 1)
    domains = [
        "وضوح الأهداف / Clarity of objectives",
        "ملاءمة المحتوى الحركي / Movement content",
        "التدرج / Progression",
        "السلامة والبدائل / Safety and alternatives",
        "الاستمتاع / Enjoyment",
        "اللياقة / Fitness",
        "الأساسيات / Fundamentals",
        "الصداقة / Friendship",
        "الاستمرار / Continuation",
        "الاختيار داخل الجلسة / In-session choice",
        "سجل التقبل المكتوب / Written acceptability record",
        "عتبة الاحتفاظ الأولية 85% / Provisional retention threshold 85%",
        "عتبة اكتمال SPPB الأولية 90% / Provisional eligible SPPB completion threshold 90%",
        "عتبة الحضور الأولية 80% / Provisional attendance threshold 80%",
        "عتبة الاستبيانات الأولية 85% / Provisional questionnaire threshold 85%",
        "تعمية مقيمي النتائج وتوثيق الانكشاف في التصميمات البديلة الثلاثة، من غير اعتماد تصميم بديل منفذ / Outcome-assessor blinding and the unblinding record for the three alternative designs, with no alternative design adopted as executed",
    ]
    add_pair(
        document,
        "عناوين الاستمتاع واللياقة والأساسيات والصداقة والاستمرار بنود مراجعة فقط. مطابقتها لدليل FIG للجمباز للجميع إصدار 2025 غير متحققة هنا لأن المقتطف المفتوح غير مرفق.",
        "The enjoyment, fitness, fundamentals, friendship, and continuation headings are review labels only. Alignment with the FIG Gymnastics for All manual, 2025 edition, is unverified here because no opened excerpt is attached.",
    )
    add_table(
        document,
        ["المحور / Domain", "الملاءمة / Relevance", "الوضوح / Clarity", "قابلية التنفيذ / Feasibility", "السلامة / Safety", "التعديل / Revision"],
        [[domain, "____", "____", "____", "____", "____________________"] for domain in domains],
    )
    add_h(document, "C. الجلسات الست والثلاثون / Thirty-six sessions", 1)
    add_table(
        document,
        ["الجلسة / Session", "الملاءمة / Relevance", "الوضوح / Clarity", "قابلية التنفيذ / Feasibility", "علم سلامة / Safety flag", "ملاحظة / Note"],
        [[str(number), "____", "____", "____", "____", "____________"] for number, *_rest in SESSIONS],
    )
    add_h(document, "D. كتل المقارنة الأربع / Four comparison blocks", 1)
    add_pair(
        document,
        "المقارنة ليست 36 جلسة حركية. تُحكم الكتل الأربع الواردة في دليل المقارنة، كل كتلة على الأبعاد الأربعة.",
        "The comparison is not 36 movement sessions. Rate the four blocks in the comparison manual, each on the four dimensions.",
    )
    add_table(
        document,
        ["الكتلة / Block", "الملاءمة / Relevance", "الوضوح / Clarity", "قابلية التنفيذ / Feasibility", "علم سلامة أو تلوث / Safety or contamination flag", "ملاحظة / Note"],
        [[block, "____", "____", "____", "____", "____________"] for block in ["أسابيع 1–3 / Weeks 1–3", "أسابيع 4–6 / Weeks 4–6", "أسابيع 7–9 / Weeks 7–9", "أسابيع 10–12 / Weeks 10–12"]],
    )
    add_h(document, "E. أسئلة مفتوحة / Open questions", 1)
    for question in [
        "ما الحركات التي ينبغي تعديلها أو حذفها؟ / Which movements should be changed or removed?",
        "هل بدائل الجلوس والوقوف المدعوم كافية؟ / Are the seated and supported-standing alternatives sufficient?",
        "ما قاعدة المكان والزمن التي تقلل التلوث؟ / What place and time rule would reduce contamination?",
        "ما كفاءات الميسر اللازمة؟ / Which facilitator competencies are required?",
        "هل العتبات الأولية للانتقال مناسبة قبل حسم المقامات؟ / Are the provisional progression thresholds suitable before the denominators are locked?",
    ]:
        add_p(document, question)
        add_p(document, "______________________________________________________________________")
    add_h(document, "F. خطة تحليل التحكيم / Rating analysis plan", 1)
    add_pair(
        document,
        "I-CVI لبند ملاءمة محدد مسبقًا يساوي عدد الخبراء الذين أعطوا ذلك البند 3 أو 4 مقسومًا على عدد من قيّموا البند. الوضوح وقابلية التنفيذ يُعرضان كلًا على حدة ولا يُدمجان في I-CVI الملاءمة. أعلام السلامة والتلوث مراجعة نوعية ولا تتحول إلى معامل. S-CVI/Ave هو متوسط I-CVI لبنود الملاءمة المحددة مسبقًا فقط. لا يُستخدم حد قطعي عام. يمكن لاحقًا حساب كابا معدلة بعد تحديد عدد الخبراء. هذه الاستمارة لا تحتوي درجاتًا ولا معاملات.",
        "I-CVI for a prespecified relevance item equals the number of experts rating that item 3 or 4 divided by the number who rated the item. Clarity and feasibility are reported separately and are not folded into the relevance I-CVI. Safety and contamination flags stay qualitative and are not turned into a coefficient. S-CVI/Ave is the mean relevance I-CVI across the prespecified relevance items only. No universal cutoff is used. A modified kappa may be calculated later, after the expert count is known. This form contains no ratings and no coefficients.",
    )
    add_h(document, "G. سجل التعديلات / Revision log", 1)
    add_table(
        document,
        ["البند / Item", "ملاحظة الخبير / Expert concern", "الإجراء / Action", "السبب / Rationale", "الإصدار / Version"],
        [["________", "________", "________", "________", "________"] for _ in range(4)],
    )
    add_h(document, "H. خلاصة الرأي / Advisory summary", 1)
    add_p(document, "☐ قبول المسودة  ☐ قبول مع تعديل  ☐ مراجعة كبيرة  ☐ غير مناسب")
    add_p(document, "☐ Accept as drafted  ☐ Accept with revisions  ☐ Major revision required  ☐ Not suitable")
    add_pair(
        document,
        "الرأي استشاري. ليس موافقة أخلاقية ولا إذنًا صحيًا.",
        "The opinion is advisory. It is not an ethics approval and not health clearance.",
    )
    add_p(document, "التوقيع / Signature: ________  التاريخ / Date: ________")
    add_h(document, "I. الخطوات التالية / Next steps", 1)
    for step in [
        "اختيار خبراء مستقلين مؤهلين. / Recruit qualified independent experts.",
        "إرسال الدليل والاستمارة نفسهما إلى كل خبير. / Send every expert the same manual and form.",
        "جمع الإجابات ثم حساب معاملات الملاءمة فقط كما في القسم F. / Collect responses and calculate relevance coefficients only as in section F.",
        "معالجة ملاحظات السلامة مع مختص قبل أي تنفيذ. / Resolve safety comments with a clinician before any delivery.",
        "تعديل الدليل مع رقم إصدار. / Revise the manual with a version number.",
        "الاستطلاع بعد استكمال البنود المعلقة، لا قبلها. / Pilot only after the pending items are completed, not before.",
    ]:
        document.add_paragraph(step, style="List Number")
    add_pending(document)
    document.save(OUT / "GfA_Expert_Validation_Forms_v2.1.docx")


def build_sap() -> None:
    document = _doc()
    banner(document)
    add_h(document, "خطة التحليل الإحصائي V2.1 / Statistical analysis plan V2.1", 1)
    add_pair(
        document,
        "دراسة مقارنة لاحقة لبرنامج ترويحي للجمباز للجميع لدى الرجال والسيدات من 60 إلى 75 سنة في دور رعاية بالقاهرة. النتيجة الأساسية المرشحة هي الأداء الوظيفي بمقياس SPPB. جودة الحياة مرشحة عبر OPQOL-Brief. LSNS-6 نتيجة ثانوية مرشحة لشبكة الأسرة والأصدقاء، وليس مقياس الترابط داخل الدار.",
        "Later comparative study of a Gymnastics for All recreational program among men and women aged 60–75 in Cairo care homes. The candidate primary outcome is functional performance by the SPPB. Quality of life is a candidate outcome through OPQOL-Brief. LSNS-6 is a candidate secondary outcome for the family and friend network, not a measure of within-facility social connectedness.",
    )
    add_h(document, "1. الحالة / Status", 2)
    add_pair(
        document,
        "هذه خطة مشروطة. تُقفل نسخة مؤرخة قبل الاطلاع على مقارنات النتائج. هذه النسخة ليست ذلك الإقفال.",
        "This is a conditional plan. A dated version must be locked before anyone inspects comparative outcome results. This version is not that lock.",
    )
    design_block(document)
    outcome_block(document)
    add_h(document, "2. التدخل والقياس / Intervention and assessment", 2)
    add_p(document, "12 أسبوعًا، 3 جلسات أسبوعيًا، 36 جلسة، 30–60 دقيقة. " + DOSE)
    add_h(document, "3. مجموعات التحليل / Analysis sets", 2)
    add_pair(
        document,
        "إذا اعتُمد لاحقًا تخصيص عشوائي، فالمجموعة الأساسية تتبع التخصيص الأصلي مع خطة الفقد المقفلة. نسبة التزام المكونات وصفية ولا تحل محلها. تحليل per-protocol غير معرّف الآن لأن عتبة الالتزام معلّقة حتى اعتماد الجرعة، وهو ليس تحليلًا تأكيديًا. إذا اعتُمدت المقارنة شبه التجريبية المضبوطة، تُحدد المجموعة بالتعرض المسجل ومعايير الأهلية، ولا تُسمى تحليلًا حسب النية.",
        "If random assignment is later adopted, the primary set follows the original assignment together with the locked missing-data plan. Component adherence is descriptive and does not replace it. A per-protocol analysis is not defined because the adherence threshold is pending until the dose is adopted, and that analysis is not a confirmatory analysis. If the quasi-experimental controlled comparison is adopted, the set is defined by recorded exposure and eligibility, and it is not named an intention-to-treat analysis.",
    )
    add_h(document, "4. نماذج مشروطة بتصميم بديل واحد / Models conditional on one alternative design", 2)
    add_pair(
        document,
        "إذا كان التصميم البديل المعتمد لاحقًا تخصيصًا عشوائيًا على مستوى الشخص: انحدار يضبط SPPB عند T0. مقيمو النتائج يُعمون عن التخصيص، ويُوثق انكشاف التخصيص أو تعذر التعمية كتابة. الإجراء معلّق ولم يُنفذ. إذا تكرر الأشخاص داخل الدار يراعى ذلك في الاستدلال.",
        "If the alternative design later adopted is individual-level randomization: regression adjusted for SPPB at T0. Outcome assessors are blinded to allocation, and allocation unblinding or an inability to blind is documented in writing. The procedure is pending and has not been carried out. If several people share a facility, inference respects that dependence.",
    )
    add_pair(
        document,
        "إذا كان التصميم البديل المعتمد لاحقًا تخصيصًا عشوائيًا عنقوديًا على مستوى الدار: نموذج يضبط القياس القبلي مع استدلال يراعي التجمع وعدد الدور الفعلي، بما في ذلك عندما يكون عدد الدور قليلًا. لا يُستخدم نموذج مختلط تقليدي وحده عند عدد قليل من الدور من غير تقييمه. مقيمو النتائج يُعمون عن التخصيص، ويُوثق انكشاف التخصيص أو تعذر التعمية كتابة. الإجراء معلّق ولم يُنفذ.",
        "If the alternative design later adopted is cluster-randomization by facility: a baseline-adjusted model with inference that respects clustering and the actual number of facilities, including when the number of facilities is small. A conventional mixed model is not used alone for a small number of facilities without assessing it. Outcome assessors are blinded to allocation, and allocation unblinding or an inability to blind is documented in writing. The procedure is pending and has not been carried out.",
    )
    add_pair(
        document,
        "إذا كان التصميم البديل المعتمد لاحقًا مقارنة شبه تجريبية مضبوطة: انحدار يضبط القياس القبلي ومربِكات تُسمى مسبقًا. الضبط لا يزيل التحيز غير المقاس. مقيمو النتائج يُعمون عن التخصيص، ويُوثق انكشاف التخصيص أو تعذر التعمية كتابة. الإجراء معلّق ولم يُنفذ.",
        "If the alternative design later adopted is a quasi-experimental controlled comparison: regression adjusted for baseline and for confounders named in advance. Adjustment does not remove unmeasured bias. Outcome assessors are blinded to allocation, and allocation unblinding or an inability to blind is documented in writing. The procedure is pending and has not been carried out.",
    )
    add_h(document, "5. المتغيرات المشتركة / Covariates", 2)
    add_pair(
        document,
        "مرشحون غير مقفلين: العمر، والنوع، والقدرة الحركية القبلية. الدار لا تدخل متغيرًا عاديًا وعنقودًا معًا إلا بقاعدة تُكتب مع التصميم المسمى. لا تُختار المتغيرات بعد رؤية النتائج. تفاعل النوع أو الحركة ليس تحليلًا أساسيًا في هذه النسخة.",
        "Candidates, not locked: age, sex, and baseline mobility. Facility is not entered as both an ordinary covariate and the cluster unless a rule is written with the named design. Covariates are not chosen after seeing outcomes. Sex or mobility interaction is not a primary analysis in this version.",
    )
    add_h(document, "6. البيانات المفقودة / Missing data", 2)
    add_pair(
        document,
        "يُعرض الفقد وأسبابه حسب المجموعة والزمن. تعذر أداء SPPB حسب دليل الأداة يُفصل عن غياب القياس. التعويض المتعدد خيار لاحق إذا سمحت الافتراضات والحجم، مع حساسية لافتراضات أخرى. لا يُستخدم حمل آخر ملاحظة حلًا افتراضيًا.",
        "Report missingness and its reasons by group and time. Inability to perform the SPPB under the instrument rules is separated from an absent assessment. Multiple imputation is a later option if the assumptions and the amount of data allow it, with sensitivity under other assumptions. Last observation carried forward is not the default.",
    )
    add_h(document, "7. التعددية / Multiplicity", 2)
    add_pair(
        document,
        "للنتيجة الأساسية الواحدة مستوى ثنائي الطرف 0.05. النتائج الثانوية وفواصلها تعرض بحذر. أي استنتاج تأكيدي عنها يحتاج خطة تعدد تُقفل مسبقًا. T2 استكشافي إذا نُفذ. القيمة الاحتمالية لا تُقرأ وحدها أهمية عملية.",
        "The single primary outcome uses a two-sided 0.05 level. Secondary outcomes and their intervals are reported cautiously. Any confirmatory claim about them needs a multiplicity plan locked in advance. T2 is exploratory if it is conducted. A probability value is not read on its own as practical importance.",
    )
    add_h(document, "8. الحساسية / Sensitivity", 2)
    add_pair(
        document,
        "تُفحص البواقي والقيم المؤثرة ومدى SPPB. حساسية مقترحة بعد الإقفال: بنية التجمع، والقياسات المكتملة، وافتراضات الفقد، ومجموعة ضبط بديلة محددة مسبقًا. تحليل per-protocol يضاف فقط بعد اعتماد الجرعة وتعريف العتبة، وهو ليس تحليلًا تأكيديًا.",
        "Inspect residuals, influential values, and the SPPB range. Sensitivity analyses proposed after lock: clustering structure, complete measurements, missingness assumptions, and an alternative prespecified adjustment set. A per-protocol analysis is added only after the dose is adopted and the threshold is defined, and it is not a confirmatory analysis.",
    )
    add_h(document, "9. الاستطلاع والسلامة / Pilot and safety", 2)
    add_pair(
        document,
        "الاستطلاع يُلخص وصفيًا بالاستقطاب والاحتفاظ والحضور واكتمال SPPB واكتمال الاستبيانين والتزام المكونات والملاحظات المكتوبة والأحداث. نسبة الحضور = الجلسات المتاحة التي حُضرت ÷ الجلسات المتاحة فعلًا. عند عرض كل الجلسات المخططة يكون المقام = عدد الملتحقين × 36. التزام المكونات = المنفذة ÷ المخططة للجلسة المنفذة. عتبة per-protocol معلّقة وليست تحليلًا تأكيديًا. مقام استبيانات T1 هو عدد الملتحقين مضروبًا في 2. العتبات الأولية 85% و90% و80% و85% غير معتمدة. لا اختبار تأكيدي للفاعلية. الأحداث تُعرض بالنوع والشدة والعلاقة المحتملة من دون إخفاء حدث خطير.",
        "The pilot is summarized descriptively: recruitment, retention, attendance, SPPB completion, completion of the two questionnaires, component adherence, written notes, and events. Attendance proportion = available sessions attended ÷ sessions actually available. When every planned session is offered, the denominator equals the enrolled count multiplied by 36. Component adherence = delivered ÷ planned for the delivered session. The per-protocol threshold is pending and is not a confirmatory analysis. The T1 questionnaire denominator is the enrolled count multiplied by 2. The provisional thresholds 85, 90, 80, and 85 percent are not adopted. There is no confirmatory efficacy test. Events are shown by type, severity, and possible relation, and a serious event is not hidden.",
    )
    add_h(document, "10. البيانات والبرمجيات / Data and software", 2)
    add_pair(
        document,
        "يستخدم رمز منفصل عن الهوية عند الجمع. البرمجيات وإصداراتها تُسجل عند اختيار فريق التحليل. لا برمجية معتمدة في هذه المسودة.",
        "A code separate from identity is used when collection starts. Software and versions are recorded when the analysis team is chosen. No software is adopted in this draft.",
    )
    add_h(document, "11. قوالب الجداول الفارغة / Empty table shells", 2)
    add_pair(document, "كل الخانات فارغة عمدًا. لا أعداد ولا آثار ولا قيم احتمالية.", "Every cell is intentionally blank. There are no counts, effects, or probability values.")
    shells = [
        ("جدول 1. الخصائص عند T0 / Table 1. Characteristics at T0", ["المتغير / Characteristic", "التدخل / Intervention", "المقارنة / Comparison", "المجموع / Total"], ["العدد / Count", "العمر / Age", "النوع / Sex", "SPPB عند T0 / SPPB at T0", "OPQOL-Brief عند T0 / OPQOL-Brief at T0", "LSNS-6 عند T0 / LSNS-6 at T0", "توزيع الدور / Facility distribution", "فئة الحركة / Mobility category"]),
        ("جدول 2. السريان / Table 2. Flow", ["البند / Flow item", "التدخل / Intervention", "المقارنة / Comparison", "المجموع / Total"], ["فُحصوا / Screened", "مؤهلون / Eligible", "وافقوا / Consented", "خُصصوا / Allocated", "قياس T0 / T0 assessment", "أكملوا T1 / Completed T1", "أكملوا T2 إن نُفذ / Completed T2 if conducted", "انسحبوا أو فُقدوا / Withdrew or were lost"]),
        ("جدول 3. النتيجة الأساسية / Table 3. Primary outcome", ["النتيجة / Outcome", "تدخل T0 / Intervention T0", "تدخل T1 / Intervention T1", "مقارنة T0 / Comparison T0", "مقارنة T1 / Comparison T1", "الفرق المعدل وفترته / Adjusted difference and interval", "قيمة الاحتمال / Probability value"], ["مجموع SPPB / Total SPPB"]),
        ("جدول 4. نتائج ثانوية مرشحة / Table 4. Candidate secondary outcomes", ["النتيجة / Outcome", "تدخل T0 / Intervention T0", "تدخل T1 / Intervention T1", "مقارنة T0 / Comparison T0", "مقارنة T1 / Comparison T1", "الأثر المعدل وفترته / Adjusted effect and interval"], ["OPQOL-Brief", "LSNS-6 شبكة الأسرة والأصدقاء فقط / LSNS-6 family and friend network only", "T2 اختياري إن نُفذ / Optional T2 if conducted"]),
        ("جدول 5. التنفيذ / Table 5. Delivery", ["المؤشر / Indicator", "التدخل / Intervention", "المقارنة / Comparison", "التعريف / Definition"], ["جلسات مخططة / Planned sessions", "جلسات متاحة فعلًا / Sessions actually available", "نسبة الحضور = الجلسات المتاحة التي حُضرت ÷ الجلسات المتاحة فعلًا. عند عرض كل الجلسات المخططة: المقام = الملتحقون × 36 / Attendance proportion = available sessions attended ÷ sessions actually available. When every planned session is offered: denominator = enrolled count × 36", "التزام المكونات = المنفذة ÷ المخططة للجلسة المنفذة / Component adherence = delivered ÷ planned for the delivered session", "متوسط الدقائق / Mean minutes", "انحرافات / Deviations", "أحداث / Events", "أحداث خطيرة / Serious events"]),
        ("جدول 6. الفقد / Table 6. Missingness", ["المقياس والزمن / Measure and time", "نقص التدخل / Missing in intervention", "نقص المقارنة / Missing in comparison", "الأسباب / Reasons"], ["SPPB T0", "SPPB T1", "تعذر أداء SPPB حسب الدليل / SPPB unable to perform per the instrument rules", "OPQOL-Brief T1", "LSNS-6 T1", "T2 اختياري / Optional T2"]),
        ("جدول 7. الحساسية / Table 7. Sensitivity", ["التحليل / Analysis", "الافتراض / Assumption", "الأثر المعدل / Adjusted effect", "القراءة / Reading"], ["النموذج المقفَل لاحقًا / Model locked later", "قياسات مكتملة / Complete measurements", "حساسية الفقد / Missingness sensitivity", "طريقة تجمع بديلة عند عدد قليل من الدور / Alternative clustering method when the number of facilities is small", "تحليل per-protocol: العتبة معلّقة حتى اعتماد الجرعة وليس تحليلًا تأكيديًا / Per-protocol analysis: threshold pending until the dose is adopted and not a confirmatory analysis"]),
    ]
    for title, headers, labels in shells:
        add_h(document, title, 3)
        add_table(document, headers, [label.split("|") if False else [label] + ["—"] * (len(headers) - 1) for label in labels])
    add_h(document, "12. سجل ما قبل الإقفال / Pre-lock register", 2)
    add_pending(document)
    add_pair(
        document,
        "هذه الوثيقة لا تشهد على موافقة، ولا استقطاب، ولا تخصيص منفذ، ولا بيانات، ولا أثر ملاحظ.",
        "This document does not attest to an approval, recruitment, an executed allocation, data, or an observed effect.",
    )
    document.save(OUT / "GfA_Active_Ageing_SAP_Step24_v2.1.docx")


def build_codesign() -> None:
    document = _doc()
    banner(document)
    add_h(document, "بروتوكول مقترح لمرحلة البناء التشاركي السابقة / Proposed protocol for the prior co-design phase", 1)
    add_pair(
        document,
        "هذا بروتوكول مقترح ومستقل عن دليل الجلسات الست والثلاثين. المرحلة لم تبدأ. ليست تدخل الدراسة، ولا مجموعة المقارنة، ولا اختبار فاعلية، ولا تصميمًا منفذًا.",
        "This is a proposed protocol and it is independent of the 36-session manual. The phase has not started. It is not the study intervention, not the comparison group, not an efficacy test, and not an executed design.",
    )
    add_h(document, "1. المشاركون / People who would take part", 2)
    add_pair(
        document,
        "كبار السن المقيمون في دور الرعاية بالقاهرة، والعاملون في تلك الدور. الأسماء والأعداد وعدد اللقاءات معلّقة. لا تُنقل أسماء إلى ملف التحليل.",
        "Older adults living in the Cairo care homes, and the staff of those homes. Names, counts, and the number of meetings are pending. Names are not copied into the analysis file.",
    )
    add_h(document, "2. العمل المكتوب / Written work", 2)
    add_pair(
        document,
        "يناقش الحاضرون كتابة خيارات الحركة والموسيقى والتشكيل وملاحظات السلامة والتقبل. الناتج قائمة مكتوبة من الاقتراحات ورقم إصدار للدليل. الاقتراحات ليست نتائج وليست بيانات مقاييس.",
        "The people present discuss, in writing, movement options, music, formations, safety comments, and acceptability. The output is a written list of suggestions and a version note for the manual. Suggestions are not results and are not measurement data.",
    )
    add_h(document, "3. التوثيق / Documentation", 2)
    add_pair(
        document,
        "التوثيق ملاحظات مكتوبة فقط. لا تصوير، ولا تسجيل صوتي، ولا تسجيل مرئي.",
        "Documentation is written notes only. There is no photography, no audio recording, and no video recording.",
    )
    add_h(document, "4. الموافقة قبل أي لقاء / Consent before any meeting", 2)
    add_pair(
        document,
        "قرار اللجنة والموافقة المكتوبة الفردية مطلوبان قبل أي لقاء. كلاهما غير مسجل في هذه المسودة. هذه الصفحة لا تحمل معرف موافقة.",
        "A committee decision and individual written consent are required before any meeting. Neither is recorded in this draft. This page carries no approval identifier.",
    )
    add_h(document, "5. السلامة / Safety", 2)
    add_pair(
        document,
        "لا تُوصف جرعة تمرين في هذه المرحلة. الجلوس متاح. يُوقف اللقاء عند ألم صدري أو دوار شديد أو ضيق نفس غير معتاد أو اضطراب اتزان مقلق. خطة الطوارئ معلّقة حتى اعتمادها.",
        "No exercise dose is prescribed in this phase. Seating is available. A meeting stops for chest pain, marked dizziness, unusual breathlessness, or concerning instability. The emergency plan stays pending until it is adopted.",
    )
    add_h(document, "6. ما يبقى معلّقًا / What stays pending", 2)
    add_pair(
        document,
        "الدور، ومن يحضر، وعدد اللقاءات، ونص الموافقة، وخطة الطوارئ. لا يُحسم هنا عدد الدور ولا العينة ولا التصميم النهائي للدراسة اللاحقة.",
        "The facilities, who attends, the number of meetings, the consent text, and the emergency plan stay pending. The facility count, the sample size, and the final design of the later study are not decided here.",
    )
    document.save(OUT / "GfA_Active_Ageing_CoDesign_Phase_Protocol_v2.1.docx")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    build_manual()
    build_pilot()
    build_expert()
    build_sap()
    build_codesign()
    print(f"Wrote V2.1 documents to {OUT}")


if __name__ == "__main__":
    main()
