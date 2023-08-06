from .constant import keys, grid
from .helper import cleanstr


def parse_querystring(key, configs):
    if keys.QUERYDICT:
        return cleanstr(configs.request.get(key, '').strip())
    else:
        pass
        # TODO:
        # Implement MultiDict


def parse_column(index, configs, columns, params):

    _f = params.get('field', True)
    _s = params.get('filter', True)
    _o = params.get('order', True)

    _s = _to_list(_s, _f)

    columns.setdefault('filter', {})
    columns.setdefault('orders', {})

    if configs.grid == grid.DATATABLES:
        if configs.keys == keys.QUERYDICT:

            columns['filter'][_f] = {
                'fields': _s,
                'search': cleanstr(configs.request.get('search[value]'.format(index), '').strip()),
                'column': cleanstr(configs.request.get('columns[{}][search][value]'.format(index), '').strip())
            }

            _index = 0
            while _o:
                _order_index = cleanstr(configs.request.get('order[{}][column]'.format(_index), None))
                if not _order_index:
                    break

                if int(_order_index) == index:
                    columns['orders'][_f] = cleanstr(configs.request.get('order[{}][dir]'.format(_index), None).upper())
                    break
                _index += 1

        else:
            pass
            # TODO:
            # Implement MultiDict

    else:
        pass
        # TODO:
        # Implement other grid type


def parse_limit(configs):
    if configs.grid == grid.DATATABLES:
        if configs.keys == keys.QUERYDICT:
            _offset = int(cleanstr(configs.request.get('start', 0)))
            _limit = int(cleanstr(configs.request.get('length', 10)))
        else:
            pass
            # TODO:
            # Implement MultiDict

    else:
        pass
        # TODO:
        # Implement other grid type

    return (_limit, _offset)


def _to_list(_filters, _field):
    if isinstance(_filters, (tuple)):
        _filters = list(_filters)

    elif isinstance(_filters, str):
        _filters = [_filters]

    elif isinstance(_filters, bool):
        _filters = [_field]

    if _field not in _filters:
        _filters.append(_field)

    return _filters
