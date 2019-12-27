from urllib.request import urlopen
from string import ascii_letters
import re

from bs4 import BeautifulSoup

from .data import Word


def importer(url:str, wordSize:int=4):
    
    print("url importer started")
    httpObj = urlopen(url)
    html = httpObj.read().decode('utf8')
    httpObj.close()

    wordList = []
    for tag in BeautifulSoup(html, 'html.parser').select('p'):
        for word in tag.text.split():
            
            if len(word) < wordSize:
                continue

            if word in wordList:
                continue

            if word[0] not in ascii_letters:
                continue

            if word[-1] not in ascii_letters:
                word = wordList[:-1]

            if isinstance(word, str) == False:
                continue
            
            try:
                Word().insert(word)
            except Warning as err:
                print(str(err))

    print("url importer finished")
    return True

def isURLValid(url:str):
    
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, url) is not None:
        return True
    return False


