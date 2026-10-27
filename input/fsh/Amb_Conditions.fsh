Invariant: amb-oth-code-text
Description: "Если код понятия имеет nullFlavor OTH, сохраняется обязательное текстовое пояснение."
Severity: #error
Expression: "code.extension.where(url = 'http://hl7.org/fhir/StructureDefinition/iso21090-nullFlavor' and value = 'OTH').exists() implies code.text.exists()"

Invariant: amb-oth-value-text
Description: "Если кодированное значение имеет nullFlavor OTH, сохраняется текстовое пояснение."
Severity: #error
Expression: "value.ofType(CodeableConcept).extension.where(url = 'http://hl7.org/fhir/StructureDefinition/iso21090-nullFlavor' and value = 'OTH').exists() implies value.ofType(CodeableConcept).text.exists()"

Invariant: amb-period-pair
Description: "Период сообщённого события или терапии содержит обе границы либо явную причину отсутствия периода."
Severity: #error
Expression: "effective.ofType(Period).all((start.exists() and end.exists()) or extension.where(url = 'http://hl7.org/fhir/StructureDefinition/data-absent-reason' or url = 'http://hl7.org/fhir/StructureDefinition/iso21090-nullFlavor').exists())"

Invariant: amb-score-content
Description: "У3-37: при отсутствии результата шкалы обязательно передаётся интерпретация либо параметры расчёта."
Severity: #error
Expression: "value.exists() or hasMember.exists() or derivedFrom.exists()"

Invariant: amb-smnn-dose-unit
Description: "У3-34.1.7: доза СМНН не имеет единицы; для иного препарата единица обязательна."
Severity: #error
Expression: "iif(medication.concept.coding.where(system = 'urn:oid:1.2.643.5.1.13.13.99.2.611').exists(), dosage.doseAndRate.dose.ofType(Quantity).all(unit.empty() and system.empty() and code.empty()), dosage.doseAndRate.dose.ofType(Quantity).all(unit.exists()))"

Invariant: amb-medication-unknown-code
Description: "У3-34.1.8–9: при неизвестном коде препарата обязательна форма и действующее вещество либо торговое наименование."
Severity: #error
Expression: "code.coding.empty() implies (doseForm.exists() and (ingredient.exists() or extension.where(url = 'https://fhir.ru/ig/semd/amb/StructureDefinition/semd-amb-trade-name').exists()))"

Invariant: amb-other-reason-text
Description: "Для кода иного значения требуется текстовое уточнение согласно условиям редакции 7."
Severity: #error
Expression: "(value.ofType(CodeableConcept).coding.where((system = 'urn:oid:1.2.643.5.1.13.13.11.1506' and code = '10') or (system = 'urn:oid:1.2.643.5.1.13.13.11.1474' and code = '19')).exists()) implies (value.ofType(CodeableConcept).text.exists() or note.text.exists())"

Invariant: amb-allergy-other-manifestation
Description: "У3-22.1.6: для иного клинического проявления (код 15) требуется описание."
Severity: #error
Expression: "reaction.all(manifestation.concept.coding.where(system = 'urn:oid:1.2.643.5.1.13.13.11.1063' and code = '15').exists() implies description.exists())"

Invariant: amb-gestational-unit
Description: "У3-38: срок беременности передаётся в днях или неделях."
Severity: #error
Expression: "value.ofType(Quantity).exists() implies value.ofType(Quantity).where(code = 'd' or code = 'wk' or unit = 'd' or unit = 'wk').exists()"

Invariant: amb-unknown-medication-reference
Description: "При неизвестном коде препарата требуется отдельный Medication с формой и веществом либо торговым наименованием."
Severity: #error
Expression: "medication.concept.coding.empty() implies medication.reference.exists()"

Invariant: amb-document-references
Description: "Все структурированные записи разделов документа и связанные уточнения доступны для проверки в контексте Bundle."
Severity: #error
Expression: "(entry.resource.ofType(Composition).section | entry.resource.ofType(Composition).section.repeat(section)).entry.all(resolve().exists()) and entry.resource.ofType(Observation).hasMember.all(resolve().exists())"
