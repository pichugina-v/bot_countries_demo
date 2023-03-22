is_city_name_valid_cases = [
    ('Москва', True), ('Нижний Новгород', True), ('London', True), ('сИвастопл', True), ('Комсомольск-на-Амуре', True),
    ('\'s-Hertogenbosch', True), ('Артемовск13', True), ('', False), ('234city', False), ('Вологда&', False),
    ('^*&', False)
]
is_country_name_valid_cases = [
    ('Россия', True), ('USA', True), ('Доминиканская Республика', True), ('кОзахстн', True), ('Коста-Рика', True),
    ('Кот д\'Ивуар', True), ('Уругвай56', False), ('', False), ('234country', False), ('Италия&', False), ('^*(', False)
]
