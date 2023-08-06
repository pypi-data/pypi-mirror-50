from urllib.request import urlopen
import re

class UrlError(Exception):
    pass

def webcompile(url):
    web = re.compile('http(s)?://\w+.\w+')
    web = web.search(url)
    if web != None:
        code = urlopen(url).read().decode()
        code = compile(code, 'sumstring', 'exec')
        exec(code)
    else:
        raise UrlError('Url is invalid, the correct structure is https://url.extension')
