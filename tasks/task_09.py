def validate_model(model: dict) -> list[str]:
    problems = []
    scope = model.get('scope')
    systems = model.get('systems', [])
    people = model.get('people', [])
    containers = model.get('containers', [])
    relations = model.get('relations', [])
    
    scope_sys = next((s for s in systems if s.get('id') == scope), None)
    if not scope_sys or scope_sys.get('external', False):
        problems.append(f"Невідомий обсяг: {scope}")
        
    for s in systems:
        if s.get('id') != scope and not s.get('external', False):
            problems.append(f"Система {s.get('id')}: має бути зовнішньою")
            
    if not containers:
        problems.append("У системі немає контейнерів")
        
    seen_ids = set()
    all_ids_ordered = []
    for p in people:
        all_ids_ordered.append(p.get('id'))
    for s in systems:
        all_ids_ordered.append(s.get('id'))
    for c in containers:
        all_ids_ordered.append(c.get('id'))
        
    for cid in all_ids_ordered:
        if cid in seen_ids:
            problems.append(f"Дубль ідентифікатора: {cid}")
        else:
            seen_ids.add(cid)
            
    all_known_ids = set(all_ids_ordered)
    element_kinds = {}
    for p in people:
        element_kinds[p.get('id')] = 'person'
    for s in systems:
        element_kinds[s.get('id')] = 'system'
    for c in containers:
        element_kinds[c.get('id')] = c.get('kind', 'app')
        
    for c in containers:
        cid = c.get('id')
        kind = c.get('kind', 'app')
        if kind not in {'app', 'database'}:
            problems.append(f"Контейнер {cid}: невідомий вид {kind}")
        tech = c.get('technology')
        if not tech or not str(tech).strip():
            problems.append(f"Контейнер {cid}: немає технології")
            
    connected_ids = set()
    for idx, rel in enumerate(relations):
        r_num = idx + 1
        f_id = rel.get('from')
        t_id = rel.get('to')
        desc = rel.get('description')
        tech = rel.get('technology')
        
        f_known = f_id in all_known_ids
        if not f_known:
            problems.append(f"Зв'язок {r_num}: невідомий елемент {f_id}")
        else:
            connected_ids.add(f_id)
            
        t_known = t_id in all_known_ids
        if not t_known:
            problems.append(f"Зв'язок {r_num}: невідомий елемент {t_id}")
        else:
            connected_ids.add(t_id)
            
        if f_known and t_known and f_id == t_id:
            problems.append(f"Зв'язок {r_num}: елемент з'єднано сам із собою")
                
        if not desc or not str(desc).strip():
            problems.append(f"Зв'язок {r_num}: немає опису")
            
        f_is_container = f_id in [c.get('id') for c in containers]
        t_is_container = t_id in [c.get('id') for c in containers]
        if (f_is_container or t_is_container) and (not tech or not str(tech).strip()):
            problems.append(f"Зв'язок {r_num}: немає технології")
            
        if f_known and t_known:
            f_kind = element_kinds.get(f_id)
            t_kind = element_kinds.get(t_id)
            is_f_db = (f_kind == 'database')
            is_t_db = (t_kind == 'database')
            if is_f_db or is_t_db:
                other_id = t_id if is_f_db else f_id
                other_is_app_container = other_id in [c.get('id') for c in containers if c.get('kind', 'app') == 'app']
                if not other_is_app_container:
                    problems.append(f"Зв'язок {r_num}: база даних доступна не лише з контейнерів")
                    
    all_elements_list = []
    for p in people:
        all_elements_list.append(p.get('id'))
    for s in systems:
        if s.get('id') != scope:
            all_elements_list.append(s.get('id'))
    for c in containers:
        all_elements_list.append(c.get('id'))
        
    for eid in all_elements_list:
        if eid not in connected_ids:
            problems.append(f"Елемент {eid}: немає жодного зв'язку")
            
    return problems


def to_mermaid(model: dict) -> str:
    problems = validate_model(model)
    if problems:
        raise ValueError(f"Модель містить помилки: {len(problems)}")
        
    def sanitize(text):
        if not text:
            return ""
        return str(text).replace('"', "'")
        
    lines = ["C4Container"]
    title = model.get('title')
    if title:
        lines.append(f"    title {sanitize(title)}")
        
    people = model.get('people', [])
    for p in people:
        pid = p.get('id')
        name = sanitize(p.get('name', ''))
        desc = p.get('description')
        if desc and str(desc).strip():
            lines.append(f"    Person({pid}, \"{name}\", \"{sanitize(desc)}\")")
        else:
            lines.append(f"    Person({pid}, \"{name}\")")
            
    systems = model.get('systems', [])
    scope = model.get('scope')
    scope_sys = next((s for s in systems if s.get('id') == scope), None)
    
    external_systems = [s for s in systems if s.get('external', False)]
    for s in external_systems:
        sid = s.get('id')
        name = sanitize(s.get('name', ''))
        desc = s.get('description')
        if desc and str(desc).strip():
            lines.append(f"    System_Ext({sid}, \"{name}\", \"{sanitize(desc)}\")")
        else:
            lines.append(f"    System_Ext({sid}, \"{name}\")")
            
    if scope_sys:
        s_name = sanitize(scope_sys.get('name', ''))
        lines.append(f"    System_Boundary({scope}, \"{s_name}\") {{")
        containers = model.get('containers', [])
        for c in containers:
            cid = c.get('id')
            cname = sanitize(c.get('name', ''))
            tech = sanitize(c.get('technology', ''))
            desc = c.get('description')
            kind = c.get('kind', 'app')
            macro = "ContainerDb" if kind == 'database' else "Container"
            if desc and str(desc).strip():
                lines.append(f"        {macro}({cid}, \"{cname}\", \"{tech}\", \"{sanitize(desc)}\")")
            else:
                lines.append(f"        {macro}({cid}, \"{cname}\", \"{tech}\")")
        lines.append("    }")
        
    relations = model.get('relations', [])
    for r in relations:
        f_id = r.get('from')
        t_id = r.get('to')
        desc = sanitize(r.get('description', ''))
        tech = r.get('technology')
        if tech and str(tech).strip():
            lines.append(f"    Rel({f_id}, {t_id}, \"{desc}\", \"{sanitize(tech)}\")")
        else:
            lines.append(f"    Rel({f_id}, {t_id}, \"{desc}\")")
            
    return "\n".join(lines)