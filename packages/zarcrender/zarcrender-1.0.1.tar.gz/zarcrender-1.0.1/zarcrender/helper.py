import re


class obj(object):
    def __init__(self, d):
        self.d = d
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)

    def __repr__(self):
        return str(self.d)


def cleanstr(text):
    if not isinstance(text, str):
        return text

    text = re.sub(r"(<.*?>)", '', text, 0, re.MULTILINE)
    text = re.sub(r"([^\w\s.-])", '', text, 0, re.MULTILINE)
    return text
