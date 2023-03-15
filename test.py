country = {'response':
           {'GeoObjectCollection':
            {'metaDataProperty':
             {'GeocoderResponseMetaData':
              {'request': 'Россия', 'results': '1', 'found': '1'}},
             'featureMember':
                [{'GeoObject':
                    {'metaDataProperty':
                        {'GeocoderMetaData':
                            {'precision': 'other', 'text': 'Россия', 'kind': 'country',
                             'Address':
                                 {'country_code': 'RU', 'formatted': 'Россия',
                                  'Components': [{'kind': 'country', 'name': 'Россия'}]},
                                 'AddressDetails': {'Country': {'AddressLine': 'Россия', 'CountryNameCode': 'RU', 'CountryName': 'Россия'}}}},
                        'name': 'Россия',
                        'boundedBy':
                            {'Envelope':
                                {'lowerCorner': '19.484764 41.185996', 'upperCorner': '191.128012 81.886117'}},
                            'Point': {'pos': '99.505405 61.698657'}}}]}}}
city = {'response':
        {'GeoObjectCollection':
         {'metaDataProperty':
          {'GeocoderResponseMetaData':
           {'boundedBy':
            {'Envelope':
             {'lowerCorner': '37.038186 55.312148', 'upperCorner': '38.2026 56.190802'}},
            'request': 'Москва', 'results': '1', 'found': '1'}},
          'featureMember': [
              {'GeoObject':
               {'metaDataProperty':
                {'GeocoderMetaData':
                 {'precision': 'other', 'text': 'Россия, Москва', 'kind': 'province',
                  'Address':
                  {'country_code': 'RU', 'formatted': 'Россия, Москва',
                   'Components': [{'kind': 'country', 'name': 'Россия'},
                                  {'kind': 'province', 'name': 'Центральный федеральный округ'},
                                  {'kind': 'province', 'name': 'Москва'}]},
                  'AddressDetails': {
                      'Country': {'AddressLine': 'Россия, Москва', 'CountryNameCode': 'RU', 'CountryName': 'Россия',
                                                 'AdministrativeArea': {'AdministrativeAreaName': 'Москва'}}}}},
                'name': 'Москва',
                        'description': 'Россия',
                        'boundedBy': {
                            'Envelope': {
                                'lowerCorner': '36.803268 55.142226', 'upperCorner': '37.967799 56.021286'}},
                        'Point': {'pos': '37.617698 55.755864'}}}]}}}
