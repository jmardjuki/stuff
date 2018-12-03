import os
import json
import urllib
import collections
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

BASE_HTML='http://www.keyakizaka46.com/s/k46o/artist/'

MAX_MEMBER=42
NULL_MEMBERS={16} #Add Grads

IMAGE_DST='images/'
JSON_DST='keyaki.json'

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


def process_image(html, num):
    """Get the image link and download fullsize
    @params:
        object html: BeautifulSoup object that contain tags from profile link
        string num: member's number; image would be named after
    """
    if not os.path.exists(IMAGE_DST):
        os.makedirs(IMAGE_DST)
    img_box = html.find("div", {"class": "box-profile_img"})
    img_link = img_box.find("img")['src']

    dl = imgSrc.replace("/400_320_102400", '')
    nameFile = IMAGE_DST + name + ".jpg"
    try:
        urllib.request.urlretrieve(dl, nameFile)
    except URLError:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))


def get_profile(html):
    """Get the image link and gather the profile details
    @params:
        object html: object html: BeautifulSoup object that contain tags from profile link
    @return:
        object: a dictionary that contains all the profile data
    """
    profile_dict = collections.OrderedDict()
    profile_box = html.find("div", {"class": "box-profile_text"})
    name = profile_box.find("p", {"class": "name"}).text
    profile_dict['name'] = name.strip().replace(" ",'')
    profile_dict['furigana'] = profile_box.find("p",
            {"class": "furigana"}).text.strip()
    profile_dict['en_name'] = profile_box.find("span",
            {"class": "en"}).text.replace("\u3000", " ")

    info_box = profile_box.find("div", {"class": "box-info"})
    all_info = info_box.findAll("dt")

    info_arr = []
    for info in all_info:
        info_arr.append(info.text.strip())

    # TO DO: Improve this as it's more than 80 char
    profile_dict['birthday'], profile_dict['horoscope'], profile_dict['height'], profile_dict['birthplace'], profile_dict['blood_type'] = info_arr
    return profile_dict


def process_html(num):
    """Read the profile link, download profile image, and get profile data
    @params:
        string num: member's number, the profile link is based on this
    @return:
        object: a dictionary that contains all the profile detail
    """
    html_address = BASE_HTML + num
    raw_html = simple_get(html_address)
    html = BeautifulSoup(raw_html, 'html.parser')

    process_image(html, num)
    return get_profile(html)


def main():
    data = collections.OrderedDict()
    for i in range(1, MAX_MEMBER+1):
        if i not in NULL_MEMBERS:
            num = str(i)
            if ( len(num) == 1):
                num = '0' + num
            data[num] = process_html(num)
    with open(JSON_DST, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
