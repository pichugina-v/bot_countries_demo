def add_prefix(key_list: list[str]) -> list[str]:
    """
    Function adds prefix 'country_' for keys.
    """
    for indx, key_ in enumerate(key_list):
        key_list[indx] = f'country_{key_}'
    return key_list
