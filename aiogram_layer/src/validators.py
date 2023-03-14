def is_user_input_valid(user_input: str) -> bool:
    """

    :param user_input: user's message

    :return: True if  user's message is valid, else False
    """

    invalid_chars = set('!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~')
    if not user_input or user_input[0].isdigit() or invalid_chars in set(user_input):
        return False

    return True
