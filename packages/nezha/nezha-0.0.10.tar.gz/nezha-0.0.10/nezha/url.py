from typing import Union, Mapping
from urllib import parse


def urljoin(base: str, url: str = '', params: Union[str, Mapping] = '') -> str:
    return '?'.join((parse.urljoin(base, url), parse.urlencode(params))).rstrip('?')


if __name__ == '__main__':
    print(urljoin('http://ww.sx/s/'))
