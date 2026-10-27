Extension: AmbSourceUnit
Id: semd-amb-source-unit
Title: "Исходное кодирование единицы измерения"
Description: "Кодирование translation единицы из НСИ, включая исходную версию, после представления величины или интервала в FHIR/UCUM. Число сохраняется в основной величине; несогласованные исходные числа не исправляются молча."
Context: Quantity, Timing.repeat
* value[x] only Coding
* valueCoding 1..1 MS
* valueCoding.system 1..1 MS
* valueCoding.code 1..1 MS
* valueCoding.version MS
* valueCoding.display MS

Extension: AmbIdentifierSeries
Id: semd-amb-identifier-series
Title: "Серия документа в идентификаторе"
Description: "Серия удостоверяющего документа, полиса или документа-основания; сохраняется отдельно от номера, если источник различает их. Identifier.value сохраняет номер; существующее составное представление допустимо, если серия и номер однозначно различимы."
Context: Identifier
* value[x] only string
* valueString 1..1 MS

Extension: AmbTradeName
Id: semd-amb-trade-name
Title: "Торговое наименование препарата"
Description: "У3-34.1.9.1.1.2: сообщённое торговое наименование без вывода из display справочника СМНН. Обязательно, если назначение выполнено по торговому наименованию."
Context: Medication
* value[x] only string
* valueString 1..1 MS

Extension: AmbParticipantRole
Id: semd-amb-participant-role
Title: "Исходная роль участника клинической записи"
Description: "Роль modeCode из НСИ 1.2.643.5.1.13.13.99.2.368 на ссылке performer. Не заменяет должность PractitionerRole.code. Роль AUTHOR услуги выражается Procedure.recorder согласно conventions.html."
Context: Reference
* value[x] only CodeableConcept
* valueCodeableConcept 1..1 MS
* valueCodeableConcept.coding 1..* MS

Extension: AmbClinicalLinkType
Id: semd-amb-clinical-link-type
Title: "Тип внутренней клинической связи"
Description: "Исходное кодирование типа внутренней ссылки CDA, если оно не полностью выражено полем связи FHIR. Находится на соответствующей Reference; локальная цель разрешается внутри Bundle."
Context: Reference
* value[x] only CodeableConcept
* valueCodeableConcept 1..1 MS

Extension: AmbTherapyDuration
Id: semd-amb-therapy-duration
Title: "Продолжительность лекарственной терапии"
Description: "У3-34.1.4: длительность (width), если источник сообщает её вместо пары дат. Не дополняется вымышленной датой начала. Альтернатива MedicationStatement.effectivePeriod."
Context: MedicationStatement
* value[x] only Duration
* valueDuration 1..1 MS
* valueDuration.value 1..1 MS
* valueDuration.unit MS
* valueDuration.system MS
* valueDuration.code MS

Extension: AmbBoundaryInclusive
Id: semd-amb-boundary-inclusive
Title: "Включение границы в интервал"
Description: "Атрибут inclusive границ исходного IVL_PQ. true — граница включена; false — исключена. Не выводится из отсутствующего значения."
Context: Range.low, Range.high
* value[x] only boolean
* valueBoolean 1..1 MS
