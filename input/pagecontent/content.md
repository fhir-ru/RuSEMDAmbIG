### Каталог данных редакции 7

Каталог задаёт область поддержки получателя по [правилу MustSupport](support.html). Основание: руководство СЭМД 290 редакции 7, таблица 6 и требования У1–У3. Перечень разделов взят из руководства, а не из комплектного примера.

### Разделы документа

| Код | Содержание | Наличие секции |
|---|---|---|
| DOCINFO | Сведения о документе | 1..1 |
| BENEFITS | Льготы | 0..1 |
| COMPLNTS | Жалобы | 0..1 |
| ANAM | Анамнез заболевания | 0..1 |
| LANAM | Анамнез жизни | 0..1 |
| DISABILITY | Инвалидность | 0..1 |
| SOCANAM | Социальный анамнез | 0..1 |
| OBSTETRICANAMN | Акушерский анамнез | 0..1 |
| ALL | Аллергии и непереносимость | 0..1 |
| EPIDEM | Эпидемиологический анамнез | 0..1 |
| RESCONS | Результаты консультации/осмотра врача | 0..1 |
| CONSILIUMDECISION | Решение консилиума | 0..1 |
| COMMISSION | Решение врачебной комиссии | 0..1 |
| RESLAB | Результаты лабораторного исследования | 0..1 |
| RESINSTR | Результаты инструментального исследования | 0..1 |
| GISTRESULT | Результаты прижизненного патолого-анатомического исследования | 0..1 |
| SUR | Оперативное вмешательство | 0..1 |
| TRANSFUSINFO | Сведения о трансфузии | 0..1 |
| ELSEPROCEDURE | Прочие медицинские процедуры и манипуляции | 0..1 |
| IMM | Иммунизация | 0..1 |
| DRUG | Медикаментозное лечение | 0..1 |
| MEDDEVICE | Медицинские изделия | 0..1 |
| VITALPARAM | Витальные параметры | 0..1 |
| SCORES | Объективизированная оценка состояния пациента | 0..1 |
| DGN | Диагнозы | 1..1 |
| REGIME | Режим и рекомендации | 0..1 |
| SERVICES | Оказанные услуги | 0..1 |
| LINKDOCS | Связанные документы | 0..1 |

### Клинические записи

Кратность ниже действует **внутри присутствующей секции**. Условные правила дополняют её. В IMM допустима вакцинация вместо применения невакцинного препарата; в ALL обязательно хотя бы текстовое или структурированное описание.

| Требование | Раздел | Профиль | Кратность |
|---|---|---|---|
| У3-1 | DOCINFO | [Вид обращения](StructureDefinition-semd-amb-entry-1.html) | 1..1 |
| У3-2 | DOCINFO | [Место проведения](StructureDefinition-semd-amb-entry-2.html) | 0..1 |
| У3-3 | DOCINFO | [Способ выявления заболевания](StructureDefinition-semd-amb-entry-3.html) | 0..1 |
| У3-4 | DOCINFO | [Состояние пациента](StructureDefinition-semd-amb-entry-4.html) | 1..1 |
| У3-5 | DOCINFO | [Объективные данные](StructureDefinition-semd-amb-entry-5.html) | 0..1 |
| У3-6 | DOCINFO | [Заключение консультации](StructureDefinition-semd-amb-entry-6.html) | 1..1 |
| У3-7 | DOCINFO | [Выявленные патологии](StructureDefinition-semd-amb-entry-7.html) | 0..* |
| У3-8 | BENEFITS | [Льготная категория](StructureDefinition-semd-amb-entry-8.html) | 1..* |
| У3-9 | COMPLNTS | [Жалобы](StructureDefinition-semd-amb-entry-9.html) | 1..1 |
| У3-10 | ANAM | [Анамнез заболевания](StructureDefinition-semd-amb-entry-10.html) | 1..1 |
| У3-11 | LANAM | [Анамнез жизни (текстом)](StructureDefinition-semd-amb-entry-11.html) | 1..1 |
| У3-12 | DISABILITY | [Сведения об инвалидности](StructureDefinition-semd-amb-entry-12.html) | 1..* |
| У3-13 | SOCANAM | [Сведения об утрате профессиональной трудоспособности](StructureDefinition-semd-amb-entry-13.html) | 0..* |
| У3-14 | SOCANAM | [Сведения о нетрудоспособности](StructureDefinition-semd-amb-entry-14.html) | 0..1 |
| У3-15 | SOCANAM | [Потенциально-опасные для здоровья социальные факторы](StructureDefinition-semd-amb-entry-15.html) | 0..* |
| У3-16 | SOCANAM | [Вредные производственные факторы](StructureDefinition-semd-amb-entry-16.html) | 0..* |
| У3-17 | SOCANAM | [Вредные привычки и зависимости](StructureDefinition-semd-amb-entry-17.html) | 0..* |
| У3-18 | SOCANAM | [Сведения о занятости](StructureDefinition-semd-amb-entry-18.html) | 0..1 |
| У3-19 | OBSTETRICANAMN | [Акушерский анамнез](StructureDefinition-semd-amb-entry-19.html) | 1..1 |
| У3-20 | OBSTETRICANAMN | [Порядковый номер текущей беременности](StructureDefinition-semd-amb-entry-20.html) | 1..1 |
| У3-21 | ALL | [Сведения об аллергических реакциях в анамнезе](StructureDefinition-semd-amb-entry-21.html) | 0..1 |
| У3-22 | ALL | [Аллергические реакции в анамнезе](StructureDefinition-semd-amb-allergy-intolerance.html) | 0..* |
| У3-23 | EPIDEM | [Эпидемиологический анамнез](StructureDefinition-semd-amb-entry-23.html) | 1..1 |
| У3-24 | RESCONS | [Сведения о результате проведения консультации/осмотра врача-специалиста](StructureDefinition-semd-amb-entry-24.html) | 1..* |
| У3-25 | CONSILIUMDECISION | [Сведения о результате проведения консилиума врачей](StructureDefinition-semd-amb-entry-25.html) | 1..* |
| У3-26 | COMMISSION | [Сведения о результатах проведения врачебной комиссии](StructureDefinition-semd-amb-entry-26.html) | 1..* |
| У3-27 | RESLAB | [Сведения о результатах проведения лабораторного исследования](StructureDefinition-semd-amb-entry-27.html) | 1..* |
| У3-28 | RESINSTR | [Сведения о результатах проведения инструментального исследования](StructureDefinition-semd-amb-entry-28.html) | 1..* |
| У3-29 | GISTRESULT | [Сведения о результатах проведения патолого-анатомического исследования](StructureDefinition-semd-amb-entry-29.html) | 1..* |
| У3-30 | SUR | [Сведения о результатах проведения оперативного вмешательства](StructureDefinition-semd-amb-entry-30.html) | 1..* |
| У3-31 | TRANSFUSINFO | [Сведения о проведенной трансфузиии](StructureDefinition-semd-amb-entry-31.html) | 1..* |
| У3-32 | ELSEPROCEDURE | [Медицинские процедуры и манипуляции](StructureDefinition-semd-amb-entry-32.html) | 1..* |
| У3-33 | IMM | [Сведения о применении иммунобиологического лекарственного препарата](StructureDefinition-semd-amb-medication-administration.html) | 1..* |
| У3-34 | DRUG | [Сведения о применении лекарственного препарата](StructureDefinition-semd-amb-medication-statement.html) | 1..* |
| У3-35 | MEDDEVICE | [Сведения о применении медицинского изделия](StructureDefinition-semd-amb-entry-35.html) | 1..* |
| У3-36 | VITALPARAM | [Сведения об измерении витального параметра](StructureDefinition-semd-amb-entry-36.html) | 1..* |
| У3-37 | SCORES | [Сведения о расчете клинической шкалы или опросника](StructureDefinition-semd-amb-entry-37.html) | 1..* |
| У3-38 | DGN | [Сведения об установленном диагнозе](StructureDefinition-semd-amb-condition.html) | 1..* |
| У3-39 | REGIME | [Режим и рекомендации](StructureDefinition-semd-amb-care-plan.html) | 1..1 |
| У3-40 | SERVICES | [Сведения об оказанных медицинских услугах](StructureDefinition-semd-amb-procedure.html) | 1..* |
| У3-41 | LINKDOCS | [Сведения о связанном документе](StructureDefinition-semd-amb-linked-document.html) | 1..* |

### Уточняющие сведения

Связанные Observation сохраняют исходное кодирование уточнения, значение, дату, примечание и собственные уточнения через hasMember. Входы шкалы 8020 связываются через derivedFrom, интерпретация 8019 — через hasMember. Уточнения диагноза и реквизитов документа имеют focus на соответствующий Condition/DocumentReference и включаются в секцию вместе с ним. Обязательность значения уточнения задаёт его профиль.

| Код | Сведения | Разделы |
|---|---|---|
| 815 | [Сведения о порядке установления инвалидности](StructureDefinition-semd-amb-qualifier-815.html) | DISABILITY |
| 8040 | [Сведения о причине инвалидности](StructureDefinition-semd-amb-qualifier-8040.html) | DISABILITY |
| 8041 | [Дополнительная запись к причине инвалидности](StructureDefinition-semd-amb-qualifier-8041.html) | DISABILITY |
| 4083 | [Срок, на который установлена степень утраты профессиональной трудоспособности](StructureDefinition-semd-amb-qualifier-4083.html) | SOCANAM |
| 12328 | [Клинические проявления патологической реакции](StructureDefinition-semd-amb-qualifier-12328.html) | ALL |
| 6026 | [Цель проведения консилиума](StructureDefinition-semd-amb-qualifier-6026.html) | CONSILIUMDECISION |
| 12475 | [Цель проведения врачебной комиссии](StructureDefinition-semd-amb-qualifier-12475.html) | COMMISSION |
| 7028 | [Сведения об исследовании лабораторного показателя](StructureDefinition-semd-amb-qualifier-7028.html) | RESLAB |
| 8102 | [Дополнительные сведения](StructureDefinition-semd-amb-qualifier-8102.html) | RESLAB |
| 12154 | [Серийный номер](StructureDefinition-semd-amb-qualifier-12154.html) | MEDDEVICE |
| 9078 | [Количество использованных единиц](StructureDefinition-semd-amb-qualifier-9078.html) | MEDDEVICE |
| 6034 | [Латеральность](StructureDefinition-semd-amb-qualifier-6034.html) | VITALPARAM |
| 8034 | [Порядковый номер](StructureDefinition-semd-amb-qualifier-8034.html) | VITALPARAM |
| 8019 | [Интерпретация результата расчета клинической шкалы или опросника](StructureDefinition-semd-amb-qualifier-8019.html) | SCORES |
| 8020 | [Параметр клинической шкалы или опросника](StructureDefinition-semd-amb-qualifier-8020.html) | SCORES |
| 8037 | [Анатомическая локализация](StructureDefinition-semd-amb-qualifier-8037.html) | SCORES |
| 7026 | [Степень обоснованности диагноза](StructureDefinition-semd-amb-qualifier-7026.html) | DGN |
| 12014 | [Уточнение характера заболевания](StructureDefinition-semd-amb-qualifier-12014.html) | DGN |
| 823 | [Уточнение внешней причины](StructureDefinition-semd-amb-qualifier-823.html) | DGN |
| 824 | [Уточнение вида травмы по способу получения](StructureDefinition-semd-amb-qualifier-824.html) | DGN |
| 12120 | [Сведения об установлении диагноза впервые в жизни](StructureDefinition-semd-amb-qualifier-12120.html) | DGN |
| 12393 | [Возраст пациента на дату установления диагноза](StructureDefinition-semd-amb-qualifier-12393.html) | DGN |
| 8004 | [Сведения о сроке беременности](StructureDefinition-semd-amb-qualifier-8004.html) | DGN |
| 8045 | [Дополнительные сведения о заболевании](StructureDefinition-semd-amb-qualifier-8045.html) | DGN |
| 11002 | [Серия документа](StructureDefinition-semd-amb-qualifier-11002.html) | LINKDOCS |
| 11003 | [Номер документа](StructureDefinition-semd-amb-qualifier-11003.html) | LINKDOCS |
| 6058 | [Форма документа](StructureDefinition-semd-amb-qualifier-6058.html) | LINKDOCS |

### Контекст и общие поля

| Данные руководства | Представление и поддерживаемые поля |
|---|---|
| У1-4–У1-11: документ | Bundle.identifier; Composition.identifier, version, type, title, date, language, meta.security |
| У1-12: пациент | Patient.identifier (МИС, СНИЛС, удостоверяющий документ, полис), type, value, assigner, period; name.family/given (отчество — следующее given); gender, birthDate, address, telecom, managingOrganization |
| Представительство | RelatedPerson.patient, identifier, relationship, name, address, telecom; Patient.contact.organization для представителя-организации; тип документа о полномочиях — Identifier.type |
| У1-13–У1-15: участники | Composition.author, custodian; PractitionerRole.identifier, code, practitioner, organization, contact; Practitioner.identifier, name, address, telecom; получатели — вложенный раздел контекста Composition.section с ролью recipient и ссылкой на Organization |
| Организация и подразделение | Organization.identifier (ФРМО, лицензия, ОГРН/ОГРНИП, ОКПО, ОКАТО), name, partOf, contact.address, contact.telecom; подразделение — отдельная Organization |
| Адрес | text, postalCode, use; расширения RuCore address-type, regionRF, fias с aoguid и houseguid; исходная точность сохраняется |
| У1-17: оплата | Coverage.type, identifier.type/value/assigner, period.start/end, insurer, paymentBy.party; идентификатор организации-плательщика сохраняет ИНН и другие переданные реквизиты |
| Направление | ServiceRequest.identifier, authoredOn, requester; PractitionerRole и Organization направившей стороны; ссылка в разделе контекста Composition; реквизиты направления могут передаваться DocumentReference без вымышленного заказа |
| Документируемое событие | Procedure.code, occurrence, performer.function/actor, recorder; Composition.event.detail; статус не выводится из отсутствующих сведений |
| У1-21: случай помощи | Encounter.identifier, subject, serviceProvider, class, priority, serviceType, actualPeriod.start/end, partOf.identifier.type/value, diagnosis.condition/use |
| Лекарственная терапия | MedicationStatement.effectivePeriod либо расширение длительности; dosage.timing.repeat, route, doseAndRate.doseQuantity, patientInstruction; Medication.code, doseForm, ingredient и расширение торгового наименования |
| Результаты вмешательств, трансфузия, изделия | Observation с кодом вмешательства/компонента крови/наименованием изделия, датой/периодом, результатом, исполнителями и уточнениями. Это сообщённые сведения источника, не новое назначение или самостоятельно подтверждённое событие |
| Анестезиологическое пособие | Связанная Observation с исходным видом пособия и текстом; NA при неприменении и OTH при некодируемом виде не подменяются фактом введения лекарства |
| Числовые, интервальные и кодированные значения | valueQuantity/Range, comparator и границы, valueCodeableConcept, valueString, valueBoolean; referenceRange.low/high/text; Coding.system/code/display/version; оригинальная единица НСИ — расширение semd-amb-source-unit |
| Внутренние ссылки | Reference на ресурс в Bundle; derivedFrom для результата и документа, hasMember для уточнений, focus для характеристики диагноза/документа; дополнительный тип связи — semd-amb-clinical-link-type |
| Связанные документы | DocumentReference.type, identifier, description, content.attachment.creation; серия/номер/форма — связанные Observation либо типизированный Identifier, без обязательного наличия файла |

В профилях открытые срезы и расширения сохраняют допустимые дополнительные сведения. Неизвестный клинический вариант нельзя молча свести к ближайшему коду или заменить только narrative. Поддержка всех допустимых типов отмеченного value[x] обязательна для получателя; выбор типа определяется содержанием и справочником параметра.

### Условные требования

| Условие | Требование к передаваемым данным | Проверка |
|---|---|---|
| Телемедицинская консультация (У3-2) | DOCINFO содержит место проведения, код 8 НСИ 1.2.643.5.1.13.13.11.1008 | Контекстная проверка: признак телемедицины не выводится из отсутствия места |
| Нет текстового аллергоанамнеза (У3-22) | В ALL есть хотя бы одна структурированная аллергологическая запись | Минимум одна ссылка ALL; типы ссылок ограничены профилями |
| OTH для кодируемого понятия | Сохраняется текстовое пояснение, если оно предписано руководством: выявленная патология, аллерген, подкомиссия, отдельные лабораторные тесты, вмешательство, анестезия, изделие | Инвариант общего Observation для code/value с OTH; специальные требования текста остаются контекстными |
| Причина инвалидности 19, проявление реакции 15, цель комиссии/консилиума 10 | Обязательно соответствующее текстовое уточнение | Проверка кодированного значения вместе с текстом/примечанием |
| Бессрочная инвалидность | Для верхней границы сохраняется PINF | Проверка исходного смысла; отсутствие end само по себе не означает бессрочность |
| Результаты исследований с периодом | Передаются начало и конец согласно руководству; точечная дата не превращается в период | Проверка формы effective[x] и границ |
| Шкала: нет результата и интерпретации | Обязателен хотя бы один параметр; иначе обязателен результат либо интерпретация (У3-37) | value или hasMember/derivedFrom; профили связанных записей различают их смысл |
| Продолжительность терапии | Пара дат либо длительность; две формы взаимоисключающие (У3-34.1.4) | Инвариант периода/длительности; пара границ периода |
| Доза СМНН / не СМНН | Для СМНН нет единицы и есть пояснение потребительской единицы; для другого препарата единица обязательна | Инвариант дозы и правило conventions.html |
| Неизвестен код препарата | Обязательна лекарственная форма; вещество обязательно при отсутствии торгового наименования; назначение по торговому наименованию требует его сохранения | Контекстная проверка Medication и ссылки на него |
| Схема приёма | Однократное применение допускает NA; иначе сохраняются интервал и точность, без подмены периодичности длительностью | Timing.repeat и timing-exact; неизвестные значения явно обозначаются |
| Вид оплаты и тип полиса | ОМС/ДМС/договор, серия, номер, ИНН, срок действия и причины NA/NAV/NASK должны согласовываться с видом оплаты (У1-17) | Контекстная проверка Coverage, Identifier и организации |
| Передано подразделение организации | Сохраняются идентификатор и наименование подразделения (У1-12) | Organization.partOf и отдельная Organization |

Условия, зависящие от факта вне документа (например, назначение по торговому наименованию), проверяются отправителем по исходным данным. Валидатор экземпляра не доказывает выполнение таких условий. Сведения, отсутствующие в источнике, не создают ради прохождения проверки.
