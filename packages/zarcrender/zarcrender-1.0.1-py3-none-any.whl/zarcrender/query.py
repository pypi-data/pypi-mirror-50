from .constant import dbms


def get_scalar(configs, query):
    configs.cursor.execute(query)
    return configs.cursor.fetchone()[0]


def get_object(configs, query):
    configs.cursor.execute(query)
    columns = [col[0] for col in configs.cursor.description]
    return [
        dict(zip(columns, row))
        for row in configs.cursor.fetchall()
    ]


def build_query(configs, queries, columns, limit_offset):

    origin = queries['origin']

    crecord = clean_from(origin, ('limit_offset', 'order', 'and_order', 'order_and', 'where', 'and_where'))
    cfilter = clean_from(origin, ('limit_offset', 'order', 'and_order', 'order_and'))

    _filter = ''
    _filter_exists = False
    for k, column in columns['filter'].items():
        for c in column['fields']:
            if column['search'] != '':
                _filter_exists = True
                if configs.dbms == dbms.SQL:
                    _filter += "CAST({} as Text) LIKE '%{}%' OR ".format(c, column['search'])
                else:
                    pass
                    # TODO:
                    # Implement NOSQL

            if column['column'] != '':
                _filter_exists = True
                if configs.dbms == dbms.SQL:
                    _filter += "CAST({} as Text) LIKE '%{}%' OR ".format(c, column['column'])
                else:
                    pass
                    # TODO:
                    # Implement NOSQL

    _orders = ''
    _order_exists = len(columns['orders']) != 0
    for col, direction in columns['orders'].items():
        if configs.dbms == dbms.SQL:
            _orders += "{} {}, ".format(col, direction)
        else:
            pass
            # TODO:
            # Implement NOSQL

    _filter = _filter[:-3].strip()
    _orders = _orders[:-2].strip()
    _limit, _offset = limit_offset

    if configs.dbms == dbms.SQL:
        queries['origin'] = replace_with(origin, {
            'where': "WHERE {}".format(_filter) if _filter_exists else '',
            'and_where': "AND {}".format(_filter) if _filter_exists else '',

            'order': "ORDER BY {}".format(_orders) if _order_exists else '',
            'and_order': ", {}".format(_orders) if _order_exists else '',
            'order_and': "ORDER BY {}, ".format(_orders) if _order_exists else 'ORDER BY',

            'limit_offset': "LIMIT {} OFFSET {}".format(_limit, _offset)
        })

        queries['crecord'] = "SELECT COUNT(*) FROM ({}) as count_all_records".format(crecord)
        queries['cfilter'] = "SELECT COUNT(*) FROM ({}) as count_with_filter".format(
            replace_with(cfilter, {
                'where': "WHERE {}".format(_filter) if _filter_exists else '',
                'and_where': "AND {}".format(_filter) if _filter_exists else '',
            })
        )
        queries['hfilter'] = _filter_exists

    else:
        pass
        # TODO:
        # Implement NOSQL


def clean_from(origin, keys):
    for k in keys:
        origin = origin.replace('__{}__'.format(k), '')

    return origin.strip()


def replace_with(origin, filters):
    for _k, _q in filters.items():
        origin = origin.replace('__{}__'.format(_k), _q)

    return origin
