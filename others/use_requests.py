import requests
from lxml import etree #必须这么用，import lxml用不了etree
from io import BytesIO



url = 'https://ky9oss.top'
data = {'user': 'lalalal', 'passwd': '12345'}
parser = etree.HTMLParser()


def get():
    # GET
    response = requests.get(url)
    content = response.content
    return content

def post():
    # POST
    response = requests.post(url, data=data)
    content = response.content
    return content

def main():
    content = get()
    content = etree.parse(BytesIO(content), parser=parser)
    
    for link in content.findall('//a'):
        print(f'{link.get("href")} --> {link.text}')

if __name__ == '__main__':
    main()
