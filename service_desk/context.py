def build_context(messages, safety):
    result = []
    remaining = 2400
    for message in reversed(messages[-6:]):
        if message['role'] not in ('user', 'assistant'):
            continue
        safe = safety.inspect(message['content'])
        if safe.flags:
            continue
        text = safe.text[:min(600, remaining)]
        if text:
            result.append({'role': message['role'], 'content': text})
            remaining -= len(text)
        if remaining <= 0:
            break
    return list(reversed(result))
