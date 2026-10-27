// MustSupport applies to receiving systems; see support.html.
RuleSet: AmbSupport
* ^purpose = "MustSupport (S) устанавливает обязанность получателя обрабатывать данные по support.html. Для отправителя обязательность определяется кратностями и условными ограничениями, а не отметкой S."
* text MS
* extension MS

Profile: AmbObservation
Parent: Observation
Id: semd-amb-observation
Title: "Клиническое утверждение амбулаторной консультации"
Description: "Общий профиль наблюдений, результатов и уточняющих сведений редакции 7. Конкретные требования определяются профилем вида записи; связанные уточнения сохраняются отдельными Observation."
* insert AmbSupport
* status MS
* code MS
* code.coding MS
* code.coding.system 1..1 MS
* code.coding.code 1..1 MS
* code.coding.display 1..1 MS
* code.coding.version 1..1 MS
* code.text MS
* subject 1..1 MS
* subject only Reference(AmbPatient)
* encounter MS
* focus MS
* effective[x] MS
* effectivePeriod.start MS
* effectivePeriod.end MS
* performer MS
* performer only Reference(AmbPractitionerRole or AmbPractitioner or AmbOrganization)
* performer.extension contains AmbParticipantRole named sourceRole 0..1 MS
* value[x] MS
* valueCodeableConcept.coding MS
* valueCodeableConcept.coding.system 1..1 MS
* valueCodeableConcept.coding.code 1..1 MS
* valueCodeableConcept.coding.display MS
* valueCodeableConcept.coding.version MS
* valueCodeableConcept.text MS
* valueQuantity.value MS
* valueQuantity.unit MS
* valueQuantity.system MS
* valueQuantity.code MS
* valueRange MS
* valueRange.low MS
* valueRange.high MS
* valueRange.low.extension contains AmbBoundaryInclusive named inclusive 0..1 MS
* valueRange.high.extension contains AmbBoundaryInclusive named inclusive 0..1 MS
* valueRatio MS
* valueBoolean MS
* valueInteger MS
* valueString MS
* valueDateTime MS
* valueTime MS
* valuePeriod MS
* valueQuantity.comparator MS
* valueQuantity.extension contains AmbSourceUnit named sourceUnit 0..1 MS
* dataAbsentReason MS
* note MS
* bodySite MS
* referenceRange MS
* referenceRange.low MS
* referenceRange.high MS
* referenceRange.text MS
* hasMember MS
* hasMember only Reference(AmbObservation)
* hasMember.extension contains AmbClinicalLinkType named sourceLinkType 0..1 MS
* derivedFrom.extension contains AmbClinicalLinkType named sourceLinkType 0..1 MS
* derivedFrom MS
* component MS
* component.code MS
* component.value[x] MS
* component.dataAbsentReason MS
* obeys amb-oth-code-text and amb-oth-value-text and amb-other-reason-text

Profile: AmbPatient
Parent: https://fhir.ru/ig/core/StructureDefinition/core-patient|0.26.0
Id: semd-amb-patient
Title: "Пациент амбулаторной консультации"
Description: "Пациент, идентификаторы МИС, СНИЛС, удостоверяющие документы, полис, адреса, контакты и представительство (У1-12). Расширения RuCore сохраняют тип адреса, регион и ФИАС."
* ^baseDefinition = "https://fhir.ru/ig/core/StructureDefinition/core-patient|0.26.0"
* insert AmbSupport
* identifier 1..* MS
* identifier.extension contains AmbIdentifierSeries named series 0..1 MS
* identifier.type MS
* identifier.system MS
* identifier.value MS
* identifier.assigner MS
* identifier.period MS
* identifier[misPatient] 1..1 MS
* identifier[snils] 1..1 MS
* identifier[identityDocument] 1..* MS
* identifier[omsPolicy] 1..1 MS
* name 1..* MS
* name.family 1..1 MS
* name.given 1..* MS
* gender 1..1 MS
* birthDate 1..1 MS
* address 1..* MS
* address.text MS
* address.postalCode MS
* address.extension MS
* telecom MS
* contact MS
* contact.relationship MS
* contact.name MS
* contact.telecom MS
* contact.address MS
* contact.organization MS
* managingOrganization MS
* link MS

Profile: AmbOrganization
Parent: https://fhir.ru/ig/core/StructureDefinition/core-organization|0.26.0
Id: semd-amb-organization
Title: "Организация в амбулаторном документе"
Description: "Организации и подразделения: идентификаторы ФРМО, лицензия, ОГРН/ОГРНИП, ОКПО, ОКАТО, наименование, адреса и контакты; У1-12–У1-21. Обязательность реквизитов зависит от роли организации."
* ^baseDefinition = "https://fhir.ru/ig/core/StructureDefinition/core-organization|0.26.0"
* insert AmbSupport
* identifier MS
* identifier.extension contains AmbIdentifierSeries named series 0..1 MS
* identifier.type MS
* identifier.system MS
* identifier.value MS
* name 1..1 MS
* partOf MS
* contact MS
* contact.telecom MS
* contact.address MS
* contact.address.text MS
* contact.address.postalCode MS
* contact.address.extension MS

Profile: AmbPractitioner
Parent: https://fhir.ru/ig/core/StructureDefinition/core-practitioner|0.26.0
Id: semd-amb-practitioner
Title: "Медицинский работник в амбулаторном документе"
Description: "ФИО, СНИЛС, адреса и контакты работника. Идентификатор роли в МИС передаётся отдельно в PractitionerRole."
* ^baseDefinition = "https://fhir.ru/ig/core/StructureDefinition/core-practitioner|0.26.0"
* insert AmbSupport
* identifier MS
* identifier.system MS
* identifier.value MS
* name MS
* name.family MS
* name.given MS
* address MS
* address.extension MS
* telecom MS

Profile: AmbPractitionerRole
Parent: https://fhir.ru/ig/core/StructureDefinition/core-practitionerrole|0.26.0
Id: semd-amb-practitioner-role
Title: "Роль медицинского работника в амбулаторном документе"
Description: "Идентификатор персонала в МИС, должность, лицо, организация и рабочие контакты. Обязательность зависит от роли автора, заверителя, направившего лица или участника события."
* ^baseDefinition = "https://fhir.ru/ig/core/StructureDefinition/core-practitionerrole|0.26.0"
* insert AmbSupport
* identifier MS
* identifier.system MS
* identifier.value MS
* practitioner MS
* practitioner only Reference(AmbPractitioner)
* organization MS
* organization only Reference(AmbOrganization)
* code MS
* code.coding MS
* code.coding.version MS
* code.coding.display MS
* contact MS
* contact.telecom MS
* contact.address MS

Profile: AmbEncounter
Parent: https://fhir.ru/ig/core/StructureDefinition/core-encounter|0.26.0
Id: semd-amb-encounter
Title: "Случай оказания помощи в консультации"
Description: "У1-21: случай, период, вид, форма и условия помощи, медицинская карта и диагнозы."
* ^baseDefinition = "https://fhir.ru/ig/core/StructureDefinition/core-encounter|0.26.0"
* insert AmbSupport
* identifier 1..* MS
* identifier.system MS
* identifier.value MS
* subject 1..1 MS
* subject only Reference(AmbPatient)
* actualPeriod MS
* actualPeriod.start 1..1 MS
* actualPeriod.end MS
* class MS
* priority MS
* serviceType MS
* serviceProvider 1..1 MS
* partOf 1..1 MS
* partOf.identifier MS
* partOf.identifier.type MS
* partOf.identifier.value MS
* diagnosis MS
* diagnosis.condition MS
* diagnosis.use MS

Profile: AmbCoverage
Parent: https://fhir.ru/ig/core/StructureDefinition/core-coverage|0.26.0
Id: semd-amb-coverage
Title: "Источник оплаты и страховое обеспечение"
Description: "У1-17: вид оплаты, реквизиты полиса/договора, период, страховая организация и застрахованный."
* ^baseDefinition = "https://fhir.ru/ig/core/StructureDefinition/core-coverage|0.26.0"
* insert AmbSupport
* beneficiary MS
* beneficiary only Reference(AmbPatient)
* type 1..1 MS
* identifier MS
* identifier.extension contains AmbIdentifierSeries named series 0..1 MS
* identifier.type MS
* identifier.value MS
* period MS
* period.start MS
* period.end MS
* insurer MS
* insurer ^type[0].targetProfile[0] = Canonical(AmbOrganization)
* paymentBy MS
* paymentBy.party MS

Profile: AmbCondition
Parent: Condition
Id: semd-amb-condition
Title: "Диагноз амбулаторной консультации"
Description: "У3-38: отдельная нозологическая единица, код МКБ-10, формулировка и дата; дополнительные характеристики — связанные Observation. Роль и обоснованность диагноза сохраняются в Encounter.diagnosis.use."
* insert AmbSupport
* subject 1..1 MS
* subject only Reference(AmbPatient)
* encounter MS
* code 1..1 MS
* code.coding 1..* MS
* code.text MS
* recordedDate 1..1 MS
* onset[x] MS
* evidence MS
* note MS
* clinicalStatus MS
* verificationStatus MS

Profile: AmbAllergyIntolerance
Parent: AllergyIntolerance
Id: semd-amb-allergy-intolerance
Title: "Аллергии и непереносимость"
Description: "У3-22: агент, тип патологической реакции, дата, клинические проявления и комментарии; текстовое указание аллергии У3-21 — Observation."
* insert AmbSupport
* patient MS
* patient only Reference(AmbPatient)
* encounter MS
* code 1..1 MS
* code.coding MS
* code.text MS
* type MS
* category MS
* onset[x] MS
* reaction 1..* MS
* reaction.manifestation MS
* reaction.description MS
* reaction.onset 1..1 MS
* note MS
* obeys amb-oth-code-text and amb-allergy-other-manifestation

Profile: AmbProcedure
Parent: Procedure
Id: semd-amb-procedure
Title: "Оказанная медицинская услуга"
Description: "У3-40 и документируемое событие У1-20: код, дата, примечания и участники услуги. Запись о результате вмешательства в SUR передаётся отдельным профилем Observation."
* insert AmbSupport
* subject MS
* code 1..1 MS
* occurrence[x] 1..1 MS
* encounter MS
* recorder MS
* performer MS
* performer.function MS
* performer.actor MS
* note MS
* report MS
* supportingInfo MS

Profile: AmbCarePlan
Parent: CarePlan
Id: semd-amb-care-plan
Title: "Режим и рекомендации"
Description: "У3-39: исходный текст рекомендаций без выведения новых назначений из свободного текста."
* insert AmbSupport
* subject MS
* encounter MS
* description 1..1 MS

Profile: AmbDocumentReference
Parent: DocumentReference
Id: semd-amb-document-reference
Title: "Связанный документ консультации"
Description: "У3-41: вид, дата формирования, идентификаторы МИС/РЭМД, серия, номер, форма и комментарии; файл необязателен. Также используется для вложения исходного учебного XML."
* insert AmbSupport
* subject MS
* identifier MS
* identifier.system MS
* identifier.value MS
* type MS
* description MS
* content MS
* content.attachment.creation MS
* content.attachment.title MS
* content.attachment.url MS
* content.attachment.data MS
* content.attachment.extension MS
* relatesTo MS

Profile: AmbMedication
Parent: Medication
Id: semd-amb-medication
Title: "Лекарственный препарат консультации"
Description: "У3-34: исходный код препарата, действующее вещество, торговое наименование и лекарственная форма."
* insert AmbSupport
* code MS
* code.coding MS
* code.coding.system MS
* code.coding.code MS
* code.coding.display MS
* code.coding.version MS
* code.text MS
* doseForm MS
* ingredient MS
* ingredient.item MS
* extension contains AmbTradeName named tradeName 0..1 MS
* obeys amb-medication-unknown-code

Profile: AmbImmunization
Parent: Immunization
Id: semd-amb-immunization
Title: "Сообщённая вакцинация"
Description: "У3-33: применяется только к подтверждённым вакцинам; невакцинные препараты передаются MedicationAdministration. Дата применения обязательна; отсутствующие доза и исполнитель не выдумываются."
* insert AmbSupport
* patient MS
* patient only Reference(AmbPatient)
* vaccineCode MS
* occurrence[x] MS
* note MS
* supportingInformation MS

Profile: AmbRelatedPerson
Parent: RelatedPerson
Id: semd-amb-related-person
Title: "Представитель пациента"
Description: "У1-12.1.7.4: представитель, связь с пациентом, СНИЛС, документы, полномочия, ФИО, адрес и контакты. Представитель-организация указывается через Patient.contact.organization."
* insert AmbSupport
* patient MS
* patient only Reference(AmbPatient)
* identifier MS
* identifier.extension contains AmbIdentifierSeries named series 0..1 MS
* identifier.type MS
* identifier.value MS
* identifier.assigner MS
* identifier.period MS
* relationship MS
* name MS
* telecom MS
* address MS
* address.extension MS

Profile: AmbServiceRequest
Parent: ServiceRequest
Id: semd-amb-service-request
Title: "Направление на консультацию"
Description: "У1-18–У1-19: направление, идентификатор, дата, направившие работник и организация."
* insert AmbSupport
* identifier MS
* identifier.system MS
* identifier.value MS
* subject MS
* authoredOn MS
* requester MS
* code MS
* code ^binding.description = "Коды запрошенных услуг или исследований; исходное кодирование направления сохраняется."
* supportingInfo MS

Profile: AmbAuthorPractitioner
Parent: AmbPractitioner
Id: semd-amb-author-practitioner
Title: "Автор документа как медицинский работник"
Description: "У1-13: ФИО и СНИЛС автора обязательны."
* identifier[snils] 1..1 MS
* identifier[snils].value 1..1 MS
* name 1..* MS
* name.family 1..1 MS
* name.given 1..* MS

Profile: AmbAuthorRole
Parent: AmbPractitionerRole
Id: semd-amb-author-role
Title: "Роль автора документа"
Description: "У1-13: обязательны идентификатор персонала в МИС, должность и ссылка на лицо со СНИЛС и ФИО."
* identifier[misPractitionerRole] 1..1 MS
* code 1..* MS
* practitioner 1..1 MS
* practitioner only Reference(AmbAuthorPractitioner)

Profile: AmbLinkedDocument
Parent: AmbDocumentReference
Id: semd-amb-linked-document
Title: "Реквизиты связанного документа LINKDOCS"
Description: "У3-41: обязательны вид документа, дата формирования и идентификаторы либо предусмотренные руководством явные причины отсутствия идентификаторов. Файл не требуется."
* type 1..1 MS
* identifier 1..* MS
* content.attachment.creation 1..1 MS
