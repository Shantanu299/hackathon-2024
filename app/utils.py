def find_by_key(data, target):
    for key, value in data.items():
        if key == target:
            return value
        elif isinstance(value, list):
            for obj in value:
                if isinstance(obj, dict):
                    target_value = find_by_key(obj, target)
                    if target_value:
                        return target_value
        elif isinstance(value, dict):
            target_value = find_by_key(value, target)
            if target_value:
                return target_value
