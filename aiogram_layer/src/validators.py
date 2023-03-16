def is_user_input_valid(user_input: str) -> bool:
    """
    Validates user input

    :param user_input: user's message

    :return: True if  user's message is not empty, start with char and contain only valid chars, else False
    """

    invalid_chars = set('!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~;№|')
    if not user_input or user_input[0].isdigit() or any(filter(lambda x: x in invalid_chars, set(user_input))):
        return False

    return True
