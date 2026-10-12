def check_history(history: list[str]) -> str:
    if not history:
        return "Помилка: історія порожня"
        
    valid_states = {'запропоновано', 'прийнято', 'відхилено', 'застаріло', 'замінено'}
    terminal_states = {'відхилено', 'застаріло', 'замінено'}
    allowed_transitions = {
        ('запропоновано', 'запропоновано'),
        ('запропоновано', 'прийнято'),
        ('запропоновано', 'відхилено'),
        ('прийнято', 'застаріло'),
        ('прийнято', 'замінено')
    }
    
    for i, state in enumerate(history):
        step_num = i + 1
        if state not in valid_states:
            return f"Помилка: невідомий стан «{state}» на кроці {step_num}"
        if i == 0:
            if state != 'запропоновано':
                return "Помилка: початковий стан має бути «запропоновано»"
        else:
            prev_state = history[i - 1]
            if (prev_state, state) not in allowed_transitions:
                return f"Помилка: крок {step_num}: перехід {prev_state} -> {state} заборонений"
                
    last_state = history[-1]
    result = f"Історія коректна, поточний стан: {last_state}"
    if last_state in terminal_states:
        result += " (кінцевий)"
    return result