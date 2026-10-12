def utility_tree(scenarios: list[dict]) -> str:
    valid_levels = {'high', 'medium', 'low'}
    
    seen_ids = set()
    for sc in scenarios:
        sid = sc['id']
        if sid in seen_ids:
            raise ValueError(f"Дубль ідентифікатора: {sid}")
        seen_ids.add(sid)
        
        for field in ['importance', 'difficulty']:
            val = sc.get(field)
            if val not in valid_levels:
                raise ValueError(f"Некоректне значення поля {field}: {val}")
                
    class_order = {'драйвер': 0, 'реалізувати': 1, 'за потреби': 2, 'відкласти': 3}
    imp_diff_weight = {'high': 3, 'medium': 2, 'low': 1}
    trans_map = {'high': 'висока', 'medium': 'середня', 'low': 'низька'}
    
    processed = []
    drivers = []
    
    for idx, sc in enumerate(scenarios):
        imp = sc['importance']
        diff = sc['difficulty']
        
        if imp == 'high' and diff in {'high', 'medium'}:
            sc_class = 'драйвер'
            drivers.append((sc, idx))
        elif imp == 'high' and diff == 'low':
            sc_class = 'реалізувати'
        elif imp == 'low' and diff == 'high':
            sc_class = 'відкласти'
        else:
            sc_class = 'за потреби'
            
        processed.append({
            'id': sc['id'],
            'attribute': sc['attribute'],
            'refinement': sc['refinement'],
            'importance': imp,
            'difficulty': diff,
            'class': sc_class,
            'orig_index': idx
        })
        
    drivers.sort(key=lambda x: (-imp_diff_weight[x[0]['difficulty']], x[1]))
    driver_ids = [d[0]['id'] for d in drivers]
    
    attributes = []
    attr_seen = set()
    for sc in processed:
        attr = sc['attribute']
        if attr not in attr_seen:
            attr_seen.add(attr)
            attributes.append(attr)
            
    lines = ["Корисність системи"]
    
    for attr in attributes:
        lines.append(f"  {attr}")
        attr_scenarios = [s for s in processed if s['attribute'] == attr]
        
        refinements = []
        ref_seen = set()
        for sc in attr_scenarios:
            ref = sc['refinement']
            if ref not in ref_seen:
                ref_seen.add(ref)
                refinements.append(ref)
                
        for ref in refinements:
            lines.append(f"    {ref}")
            ref_scs = [s for s in attr_scenarios if s['refinement'] == ref]
            
            ref_scs.sort(key=lambda s: (
                class_order[s['class']],
                -imp_diff_weight[s['importance']],
                -imp_diff_weight[s['difficulty']],
                s['orig_index']
            ))
            
            for sc in ref_scs:
                imp_ru = trans_map[sc['importance']]
                diff_ru = trans_map[sc['difficulty']]
                line = f"      {sc['id']} (важливість: {imp_ru}, складність: {diff_ru}) — {sc['class']}"
                lines.append(line)
                
    if driver_ids:
        lines.append(f"Драйвери: {', '.join(driver_ids)}")
    else:
        lines.append("Драйвери: немає")
        
    return "\n".join(lines)