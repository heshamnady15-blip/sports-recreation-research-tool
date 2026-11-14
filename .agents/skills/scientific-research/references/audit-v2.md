# تدقيق الإصدار الثاني

هذا الملف يشرح السجلات التي تمر إلى أوامر الإصدار الثاني. الأمثلة اصطناعية. نجاح التقرير لا يثبت أن البحث صحيح علميًا.

الأحكام الأربعة: خطأ حرج، يحتاج تعديل، غير قابل للتحقق، مقبول. كل حكم يحمل الدليل الذي استُخدم: معرفًا، أو رابطًا، أو مقتطفًا، أو نمطًا نصيًا.

## مرجع

```json
{
  "title": "Synthetic movement study for fixture residents",
  "year": 2024,
  "doi": "10.5555/fixture.v2.match",
  "authors": ["Ada Lovelace", "Grace Hopper"],
  "container": "Journal of Fixture Studies"
}
```

- التطابق مع Crossref أو DataCite في العنوان والسنة والمؤلفين والمجلة: مقبول، وتُعرض صيغة APA 7 ورابط `https://doi.org/`.
- اختلاف العنوان أو السنة أو المؤلفين أو المجلة، أو معرف غير موجود، أو معرف نائب: خطأ حرج.
- انقطاع الاتصال، أو استجابة بلا تأكيد للعنوان: غير قابل للتحقق، والحقل النصي «غير متحقق منها». لا يُقلب هذا إلى مقبول.

## مجلة

```json
{
  "name": "Fixture Ageing Journal",
  "index": "scopus",
  "quartile": "Q1",
  "subject_category": "Physiotherapy",
  "classification_year": 2026,
  "indexing_source": "scopus_sources",
  "indexing_url": "https://fixture.local/scopus-sources",
  "indexing_opened_on": "2026-11-14",
  "indexing_excerpt": "Scopus Q1 2026 Physiotherapy",
  "apc_mandatory": false,
  "apc_source": "publisher_journal_page",
  "apc_url": "https://fixture.local/publisher-fees",
  "apc_opened_on": "2026-11-14",
  "apc_excerpt": "No mandatory author fee. Optional open access is separate."
}
```

مقتطف الفهرسة يجمع الربع وسنة التصنيف والفئة الموضوعية، ويظهر في الصفحة المفتوحة. مقتطف الرسوم يبين مسارًا بلا رسوم إلزامية. الحقل الناقص أو الصفحة التي لا تفتح: غير قابل للتحقق. المقتطف الغائب عن الصفحة: يحتاج تعديل. `apc_mandatory: true`: خطأ حرج. القبول يعني اكتمال الدليل المعروض، لا إعادة قراءة مستقلة لقاعدة Scopus.

`indexing_source` هو `scopus_sources` أو `scu_digital_library_report`. `apc_source` هو `publisher_journal_page` أو `publisher_price_list`.

## منهج

`audit-methods` يقرأ النص ولا ينشئ عينة أو موافقة أو نتيجة. من الأنماط الحرجة: مجموعة واحدة أو غياب مجموعة مقارنة مع وصف التجربة العشوائية المضبوطة؛ قيمة p أو حجم أثر أو عدد مشاركين مع عبارة أن البيانات غير متوفرة؛ رقم موافقة في نص ينفي وجود الموافقة؛ درجات الجمباز الفني داخل نص الجمباز للجميع.

يحتاج تعديلًا: جمع التعيين الفردي والعنقودي وشبه التجريبي كتصميم منفذ واحد، واختبار للمستقلين مع تصميم عنقودي بلا تحليل يراعي العنقود، ونواتج أولية متعددة مع قيمة p بلا ذكر لتعدد المقارنات.

رقم موافقة بلا وثيقة مذكورة في النص: غير قابل للتحقق. خلو النص من هذه الأنماط: مقبول آليًا فقط، مع عبارة أن ذلك ليس حكمًا بصحة المنهج.
