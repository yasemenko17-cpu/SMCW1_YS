def view(elements: list[dict], level: str, scope: str | None = None) -> list[str]:
    valid_levels = {'context', 'container', 'component'}
    if level not in valid_levels:
        raise ValueError(f"Невідомий рівень: {level}")
        
    valid_kinds = {'person', 'system', 'container', 'component'}
    for el in elements:
        kind = el.get('kind')
        if kind not in valid_kinds:
            raise ValueError(f"Невідомий тип елемента: {kind}")
            
    if level == 'context':
        return [el['name'] for el in elements if el['kind'] in {'person', 'system'}]
        
    if scope is None:
        raise ValueError("Невідомий обсяг: None")
        
    scope_el = next((el for el in elements if el['name'] == scope), None)
    
    if level == 'container':
        if not scope_el or scope_el['kind'] != 'system':
            raise ValueError(f"Невідомий обсяг: {scope}")
        result = []
        for el in elements:
            k = el['kind']
            if k == 'person':
                result.append(el['name'])
            elif k == 'system' and el['name'] != scope:
                result.append(el['name'])
            elif k == 'container' and el.get('parent') == scope:
                result.append(el['name'])
        return result
        
    elif level == 'component':
        if not scope_el or scope_el['kind'] != 'container':
            raise ValueError(f"Невідомий обсяг: {scope}")
        result = []
        for el in elements:
            k = el['kind']
            if k in {'person', 'system'}:
                result.append(el['name'])
            elif k == 'container' and el['name'] != scope:
                result.append(el['name'])
            elif k == 'component' and el.get('parent') == scope:
                result.append(el['name'])
        return result
        
    return []