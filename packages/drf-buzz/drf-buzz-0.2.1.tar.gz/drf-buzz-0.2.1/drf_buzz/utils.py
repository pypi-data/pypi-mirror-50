def is_pretty(data):
    if 'description' in data and 'code' in data and isinstance(data, dict) \
            and isinstance(data.get('fields', []), list):
        return True
    return False
