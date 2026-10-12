import re

def check_scenario(scenario: dict) -> list[str]:
    fields = ['source', 'stimulus', 'environment', 'artifact', 'response', 'measure']
    problems = []
    
    # 1. Перевірка полів на відсутність, не-рядок або порожній рядок
    for field in fields:
        val = scenario.get(field)
        if not isinstance(val, str) or not val.strip():
            problems.append(f"Порожнє поле: {field}")
            
    # 2. Перевірка міри на наявність числа з одиницею виміру
    measure = scenario.get('measure')
    if isinstance(measure, str) and measure.strip():
        unit_pattern = r'\d+(?:[.,]\d+)?\s*(мс|с|хв|год|дн|%|запитів/с|МБ|ГБ|людино-дні|людино-днів)\b'
        if not re.search(unit_pattern, measure):
            problems.append("Міра без числа й одиниці")
            
    # 3. Перевірка невимірних слів у response та measure
    resp_val = scenario.get('response', '')
    meas_val = scenario.get('measure', '')
    text_parts = []
    if isinstance(resp_val, str):
        text_parts.append(resp_val)
    if isinstance(meas_val, str):
        text_parts.append(meas_val)
    combined_text = " ".join(text_parts).lower()
    
    immeasurable_words = ['швидко', 'зручно', 'надійно', 'безпечно', 'добре']
    for word in immeasurable_words:
        if word in combined_text:
            problems.append(f"Невимірне слово: {word}")
            
    return problems