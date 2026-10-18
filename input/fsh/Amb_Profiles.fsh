Alias: $CoreBundle = https://fhir.ru/ig/core/StructureDefinition/core-bundle|0.26.0
Alias: $CoreComposition = https://fhir.ru/ig/core/StructureDefinition/core-composition|0.26.0
Alias: $CorePatient = https://fhir.ru/ig/core/StructureDefinition/core-patient
Alias: $CoreEncounter = https://fhir.ru/ig/core/StructureDefinition/core-encounter
Alias: $SemdTypes = urn:oid:1.2.643.5.1.13.13.11.1520
Alias: $SectionTypes = urn:oid:1.2.643.5.1.13.13.99.2.197

Profile: AmbBundle
Parent: $CoreBundle
Id: semd-amb-bundle
Title: "Документ амбулаторной консультации"
Description: "Документ FHIR, передающий клиническое содержание протокола консультации СЭМД 290 редакции 7. Профиль задаёт оболочку документа; проверенное покрытие маппинга ограничено опубликованным примером."
* ^status = #draft
* ^baseDefinition = "https://fhir.ru/ig/core/StructureDefinition/core-bundle|0.26.0"
* type = #document
* identifier 1..1
* identifier.system 1..1
* identifier.value 1..1
* timestamp 1..1
* entry 1..*
* entry.fullUrl 1..1
* entry.resource 1..1
* entry ^slicing.discriminator.type = #type
* entry ^slicing.discriminator.path = "resource"
* entry ^slicing.rules = #open
* entry contains consultation 1..1
* entry[consultation].resource only AmbComposition
* entry[consultation] ^short = "Composition протокола консультации; первая запись документа"
* obeys amb-composition-first

Invariant: amb-composition-first
Description: "Первая запись документа содержит Composition протокола консультации."
Severity: #error
Expression: "entry.first().resource.is(Composition)"

Profile: AmbComposition
Parent: $CoreComposition
Id: semd-amb-composition
Title: "Содержание протокола амбулаторной консультации"
Description: "Структура документа консультации СЭМД 290: пациент, посещение, автор и разделы с исходным клиническим содержанием. Перечень и число разделов не фиксируются по единственному примеру."
* ^status = #draft
* ^baseDefinition = "https://fhir.ru/ig/core/StructureDefinition/core-composition|0.26.0"
* type.coding ^slicing.discriminator.type = #value
* type.coding ^slicing.discriminator.path = "system"
* type.coding ^slicing.rules = #open
* type.coding contains semd 1..1
* type.coding[semd].system = $SemdTypes (exactly)
* type.coding[semd].code = #290 (exactly)
* type.coding[semd] ^short = "СЭМД 290 — протокол консультации, редакция 7"
* subject 1..1
// Published RuCore snapshots use versioned base target canonicals. Setting the
// target directly avoids SUSHI 3.15's reference-narrowing resolution issue.
* subject ^type[0].targetProfile[0] = $CorePatient
* encounter 1..1
* encounter ^type[0].targetProfile[0] = $CoreEncounter
* section 1..*
* section.code 0..1
* section.code ^comment = "Исходные коды разделов СЭМД сохраняются. Дополнительный служебный раздел контекста документа может не иметь кода; код отсутствующему в источнике разделу не присваивается."
* section.code.coding ^slicing.discriminator.type = #value
* section.code.coding ^slicing.discriminator.path = "system"
* section.code.coding ^slicing.rules = #open
* section.code.coding contains semdSection 0..1
* section.code.coding[semdSection].system = $SectionTypes (exactly)
* section.code.coding[semdSection].code 1..1
* section.text 1..1
* section.text ^comment = "Человекочитаемое содержание раздела сохраняется вместе со ссылками на структурированные записи. Наличие раздела IMM само по себе не означает вакцинацию."

Profile: AmbMedicationStatement
Parent: MedicationStatement
Id: semd-amb-medication-statement
Title: "Сведения о лекарственной терапии в консультации"
Description: "Сведения о терапии, сообщённые в протоколе консультации. Не являются автоматически рецептом или подтверждением состоявшегося введения. Для числовой дозы без единицы у узла СМНН требуется текстовое пояснение её смысла."
* ^status = #draft
* subject only Reference($CorePatient)
* medication.concept 1..1
* medication.concept.coding 1..*
* dosage.text ^comment = "Для узла СМНН (НСИ 1.2.643.5.1.13.13.99.2.611) числовая доза без единицы означает количество потребительских единиц выбранного препарата. Текст поясняет это соглашение; unit/system/code не выводятся из display и пересчёт в массу не производится. При явно заданной единице это правило автоматически не применяется."
* obeys amb-smnn-dose-text

Invariant: amb-smnn-dose-text
Description: "Если препарат задан узлом СМНН и доза представлена числом без единицы, Dosage.text поясняет потребительскую единицу препарата."
Severity: #error
Expression: "medication.concept.coding.where(system = 'urn:oid:1.2.643.5.1.13.13.99.2.611').exists() implies dosage.all(doseAndRate.dose.ofType(Quantity).where(value.exists() and unit.empty() and system.empty() and code.empty()).exists() implies text.exists())"

Profile: AmbMedicationAdministration
Parent: MedicationAdministration
Id: semd-amb-medication-administration
Title: "Сообщённое применение невакцинного препарата"
Description: "Факт применения невакцинного препарата, в том числе диагностического аллергена, сообщённый в консультации. Вид ресурса выбирается по подтверждённому виду препарата, а не названию раздела IMM. Вакцинации представляются Immunization."
* ^status = #draft
* subject only Reference($CorePatient)
* medication.concept 1..1
* medication.concept.coding 1..*
* encounter ^comment = "Ссылка на посещение допустима только при наличии такой связи в исходных сведениях. Включение записи в документ через Composition.section.entry не устанавливает связь с Encounter консультации. В комплектном примере Диаскинтест с консультацией не связывается."
* occurence[x] ^comment = "Сохраняется точность исходной даты или времени применения. Неизвестные время суток, доза, путь введения, исполнитель и результат пробы не добавляются."
