from .parser import parse_column, parse_limit, parse_querystring
from .query import build_query, get_scalar, get_object
from .helper import obj
from .config import *


class ARCJsonRender:

    def __init__(self, config={}):
        self.__reset_all()
        self.__configs.update_from_dict(config)

    def __reset_all(self):
        self.__configs = cfg
        self.__queries = {}
        self.__columns = {}
        self.__indexes = 0

    def update_config(self, config={}):
        self.__configs.update_from_dict(config)
        return self

    def set_query(self, query):
        self.__queries['origin'] = " ".join(query.split())
        return self

    def add_column(self, key, **params):

        self.__columns.setdefault('render', {})
        self.__columns['render'][key] = params.get('render', None)

        if params.get('field', None):
            parse_column(
                self.__indexes,
                self.__configs,
                self.__columns,
                params
            )
        self.__indexes += 1
        return self

    def get_json(self, out={}, **kwargs):

        wkeys = kwargs.get('key', True)
        dumps = kwargs.get('dumps', True)

        build_query(
            self.__configs,
            self.__queries,
            self.__columns,
            parse_limit(
                self.__configs
            )
        )

        all_data = get_object(self.__configs, self.__queries['origin'])
        rec_count = get_scalar(self.__configs, self.__queries['crecord'])
        rec_filter = get_scalar(self.__configs, self.__queries['cfilter']) if self.__queries['hfilter'] else rec_count

        result = []
        iterate = int(parse_querystring('start', self.__configs)) + 1
        for data in all_data:
            temp = {} if wkeys else []
            for col, callback in self.__columns['render'].items():
                if col in data.keys() or callback:
                    res = str(data[col]) if not callback else callback(obj(data), iterate)
                else:
                    res = '{} or callback not defined'.format(col)

                if wkeys:
                    temp[col] = res
                else:
                    temp.append(res)

            result.append(temp)
            iterate += 1

        out['draw'] = int(parse_querystring('draw', self.__configs))
        out['recordsTotal'] = rec_count
        out['recordsFiltered'] = rec_filter
        out['data'] = result

        if dumps:
            import json
            out = json.dumps(out)

        self.__reset_all()
        return out
