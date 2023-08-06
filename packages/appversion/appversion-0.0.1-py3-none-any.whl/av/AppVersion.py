import json
import re
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup


def appstore(bundleId):
    link = 'http://itunes.apple.com/lookup?bundleId=' + bundleId

    response = requests.get(link)
    j = json.loads(response.text)

    if j['resultCount'] < 1:
        return None

    appStoreVersion = j['results'][0]['version']
    return appStoreVersion


def playstore(packageName):
    link = 'https://play.google.com/store/apps/details?id=' + packageName
    html = urlopen(link)

    bs = BeautifulSoup(html, 'html.parser')

    version = bs.find_all(class_='htlgb')
    p = re.compile('^[0-9]{1}.[0-9]{1}.[0-9]{1}$')

    for element in version:
        text = element.get_text()

        if bool(p.match(text)):
            return text

    return None


def maxv(version1, version2):
    return version1 if compare(version1, version2) else version2


def minv(version1, version2):
    return version2 if compare(version1, version2) else version1


def _get_number_list(version1, version2):
    numbers1 = version1.split('.')
    numbers2 = version2.split('.')

    len1 = len(numbers1)
    len2 = len(numbers2)

    maxLen = max(len1, len2)

    _numbers1 = [0 for _ in range(maxLen)]
    _numbers2 = [0 for _ in range(maxLen)]

    cnt = 0
    for number in numbers1:
        _numbers1[cnt] = number
        cnt += 1

    cnt = 0
    for number in numbers2:
        _numbers2[cnt] = number
        cnt += 1

    _numbers1 = list(map(str, _numbers1))
    _numbers2 = list(map(str, _numbers2))

    return _numbers1, _numbers2


def equals(version1, version2):
    numbers1, numbers2 = _get_number_list(version1, version2)
    return numbers1 == numbers2


def compare(version1, version2):
    numbers1, numbers2 = _get_number_list(version1, version2)
    length = len(numbers1)

    for i in range(length):
        number1 = numbers1[i]
        number2 = numbers2[i]

        if number1.isdigit() and number2.isdigit():
            number1 = int(number1)
            number2 = int(number2)

        if number1 > number2:
            return True

    return False
