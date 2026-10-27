CodeSystem: AmbContextRoles
Id: semd-amb-context-roles
Title: "Роли контекстных разделов документа"
Description: "Служебные роли контекста FHIR-документа; не являются кодами разделов СЭМД или новыми клиническими утверждениями."
* ^status = #draft
* ^caseSensitive = true
* ^content = #complete
* #document-event "Документируемое событие"
* #recipient "Получатель документа"
* #payment "Источник оплаты"
* #referrer "Направившее лицо"
* #referral "Документ направления"

ValueSet: AmbContextRoleVS
Id: semd-amb-context-role-vs
Title: "Роли контекстных разделов"
Description: "Допустимые роли служебных разделов контекста консультации."
* ^status = #draft
* include codes from system AmbContextRoles

Extension: AmbContextRole
Id: semd-amb-context-role
Title: "Роль раздела контекста"
Description: "Явная роль служебного подраздела Composition без присвоения вымышленного кода секции НСИ. Включённые ресурсы имеют указанную роль в документе."
Context: Composition.section
* value[x] only code
* valueCode 1..1 MS
* valueCode from AmbContextRoleVS (required)

Invariant: amb-document-context
Description: "У1-15 и У1-20: документ содержит получателя и документируемое событие с явным обозначением контекстной роли."
Severity: #error
Expression: "section.section.where(extension.where(url = 'https://fhir.ru/ig/semd/amb/StructureDefinition/semd-amb-context-role').value = 'recipient').entry.exists() and section.section.where(extension.where(url = 'https://fhir.ru/ig/semd/amb/StructureDefinition/semd-amb-context-role').value = 'document-event').entry.exists()"
