"""Readable, escaped XHTML derived solely from example resource facts."""
from html import escape

TITLES = {
    'Composition': 'Протокол консультации', 'Patient': 'Пациент',
    'Organization': 'Организация', 'Practitioner': 'Медицинский работник',
    'PractitionerRole': 'Роль медицинского работника', 'Encounter': 'Посещение',
    'Coverage': 'Страховое обеспечение', 'Procedure': 'Медицинская услуга',
    'Condition': 'Диагноз', 'Observation': 'Наблюдение',
    'AllergyIntolerance': 'Сведения об аллергии',
    'MedicationAdministration': 'Применение препарата',
    'MedicationStatement': 'Сведения о приёме препарата', 'Medication': 'Препарат',
    'CarePlan': 'Рекомендации', 'DocumentReference': 'Связанный документ',
    'Immunization': 'Вакцинация',
}
LABELS = {
    'status': 'Статус', 'clinicalStatus': 'Клинический статус', 'intent': 'Намерение',
    'subject': 'Пациент', 'patient': 'Пациент', 'beneficiary': 'Застрахованный',
    'name': 'Имя / наименование', 'identifier': 'Идентификатор', 'type': 'Тип',
    'code': 'Код / содержание', 'category': 'Категория', 'description': 'Описание',
    'birthDate': 'Дата рождения', 'gender': 'Пол', 'address': 'Адрес',
    'telecom': 'Контакт', 'contact': 'Контактные сведения', 'period': 'Период',
    'start': 'Начало', 'end': 'Окончание', 'date': 'Дата', 'recordedDate': 'Дата записи',
    'effectiveDateTime': 'Дата / время', 'effectivePeriod': 'Период',
    'occurrenceDateTime': 'Дата / время выполнения', 'occurrencePeriod': 'Период выполнения',
    'occurenceDateTime': 'Дата / время применения', 'occurencePeriod': 'Период применения',
    'actualPeriod': 'Период посещения', 'encounter': 'Посещение', 'partOf': 'Часть / карта',
    'medication': 'Препарат', 'dosage': 'Дозировка', 'doseAndRate': 'Разовая доза',
    'doseQuantity': 'Количество', 'doseForm': 'Лекарственная форма', 'timing': 'Расписание',
    'repeat': 'Повторение', 'frequency': 'Число приёмов', 'periodUnit': 'Единица интервала',
    'route': 'Путь введения', 'patientInstruction': 'Условия приёма',
    'reaction': 'Реакция', 'manifestation': 'Проявление', 'onset': 'Начало реакции',
    'valueQuantity': 'Значение', 'valueString': 'Значение', 'valueCodeableConcept': 'Значение',
    'valueBoolean': 'Значение', 'valueInteger': 'Значение', 'valueRange': 'Диапазон',
    'valuePeriod': 'Значение / период', 'dataAbsentReason': 'Причина отсутствия значения',
    'performer': 'Исполнитель', 'recorder': 'Автор записи', 'author': 'Автор',
    'custodian': 'Хранитель', 'attester': 'Заверение', 'party': 'Участник', 'mode': 'Способ',
    'organization': 'Организация', 'practitioner': 'Медицинский работник',
    'serviceProvider': 'Организация посещения', 'serviceType': 'Вид помощи',
    'class': 'Условия оказания помощи', 'priority': 'Срочность', 'diagnosis': 'Диагноз',
    'condition': 'Состояние', 'use': 'Роль / назначение', 'focus': 'Относится к',
    'hasMember': 'Связанные наблюдения', 'derivedFrom': 'Основано на',
    'content': 'Содержимое', 'attachment': 'Вложение', 'title': 'Название',
    'creation': 'Дата создания', 'contentType': 'Формат', 'language': 'Язык',
    'insurer': 'Страховая организация', 'kind': 'Вид', 'qualification': 'Квалификация / лицензия',
    'version': 'Версия', 'extension': 'Дополнительные сведения',
}
STATUS = {
    'unknown': 'неизвестен', 'completed': 'выполнено', 'recorded': 'записано',
    'draft': 'черновик', 'current': 'актуальная запись', 'proposal': 'предложение',
    'male': 'мужской', 'female': 'женский', 'food': 'пищевая', 'insurance': 'страхование',
}


def _code(value):
    """Label a Coding without inventing terminology beyond its display/code."""
    label = value.get('display') or value.get('code') or value.get('system', '')
    return str(label)


def _brief(resource):
    result = TITLES.get(resource.get('resourceType'), resource.get('resourceType', 'Ресурс'))
    for key in ('name', 'code', 'title', 'description'):
        if resource.get(key):
            result += ': ' + human_value(resource[key])
            break
    return result


def human_value(value, references=None):
    """Plain-text rendering. Callers MUST escape before placing in XHTML."""
    references = references or {}
    if value is None:
        return ''
    if isinstance(value, bool):
        return 'да' if value else 'нет'
    if isinstance(value, (str, int, float)):
        return str(value)
    if isinstance(value, list):
        return '; '.join(filter(None, (human_value(item, references) for item in value)))
    if not isinstance(value, dict):
        return str(value)
    if 'reference' in value and isinstance(value['reference'], str):
        target = references.get(value['reference'])
        return value.get('display') or (_brief(target) if target else value['reference'])
    if 'coding' in value:
        codings = list(dict.fromkeys(_code(coding) for coding in value['coding']))
        return '; '.join(filter(None, [value.get('text', ''), *codings]))
    if 'system' in value and 'code' in value and 'value' not in value:
        return _code(value)
    if 'family' in value or 'given' in value:
        return ' '.join(filter(None, [*value.get('prefix', []), value.get('family', ''),
                                     *value.get('given', []), *value.get('suffix', [])]))
    if 'value' in value:
        unit = value.get('unit') or value.get('code') or ''
        label = str(value['value']) + (' ' + unit if unit else '')
        if value.get('type'):
            label = human_value(value['type'], references) + ': ' + label
        if value.get('system') and 'code' not in value:
            label += ' [' + str(value['system']) + ']'
        return label
    fields = []
    for key, item in value.items():
        if key in ('resourceType', 'id', 'meta', 'div', 'data'):
            continue
        if key == 'url' and 'extension' in value:
            fields.append(str(item))
            continue
        text = human_value(item, references)
        if not text:
            continue
        fields.append(LABELS.get(key, key) + ': ' + text)
    if 'data' in value:
        fields.append('Содержимое вложения включено в ресурс')
    return '; '.join(fields)


def enrich_narratives(bundle):
    """Mutate resource.text only; preserve Composition.section narratives verbatim."""
    references = {entry['fullUrl']: entry['resource'] for entry in bundle.get('entry', [])
                  if entry.get('fullUrl') and entry.get('resource')}
    for entry in bundle.get('entry', []):
        resource = entry.get('resource', {})
        resource_type = resource.get('resourceType', '')
        title = TITLES.get(resource_type, resource_type)
        rows = []
        for key, value in resource.items():
            if key in ('resourceType', 'id', 'meta', 'text'):
                continue
            if resource_type == 'Composition' and key == 'section':
                names = [human_value(s.get('code', s.get('title', '')), references) for s in value]
                text = '; '.join(names)
                label = 'Разделы документа (исходный текст сохранён в каждом разделе)'
            else:
                text = human_value(value, references)
                if key in ('status', 'intent', 'gender', 'kind') and isinstance(value, str):
                    text = STATUS.get(value, value)
                label = LABELS.get(key, key)
            if text:
                rows.append('<tr><td>' + escape(label) + '</td><td>' + escape(text) + '</td></tr>')
        resource['text'] = {
            'status': 'generated',
            'div': '<div xmlns="http://www.w3.org/1999/xhtml" lang="ru" xml:lang="ru"><h2>' + escape(title)
                   + '</h2><table><tbody>' + ''.join(rows) + '</tbody></table></div>',
        }
    return bundle
