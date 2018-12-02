# Modified from https://realpython.com/python-web-scraping-practical-introduction/
import os
import urllib
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

BASE_HTML='http://www.keyakizaka46.com/s/k46o/artist/'
IMAGE_DST=os.getenv("HOME") + '/images/'

MAX_MEMBER=42
NULL_MEMBERS={16} #Grads

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
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
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def dl_fullsize(imgSrc, name):
    # Fullsize is the actual filename
    dl = imgSrc.replace("/400_320_102400", '')
    nameFile = IMAGE_DST + name + ".jpg"

    ## TO DO: Should have try and catch
    urllib.request.urlretrieve(dl, nameFile)


def process_html(num):
    html_address = BASE_HTML + num
    raw_html = simple_get(html_address)
    html = BeautifulSoup(raw_html, 'html.parser')

    img_box = html.find("div", {"class": "box-profile_img"})
    img_link = img_box.find("img")['src']
    #dl_fullsize(img_link, num)

    profile_box = html.find("div", {"class": "box-profile_text"})
    furigana = profile_box.find("p", {"class": "furigana"}).text
    furigana = furigana.strip()
    name = profile_box.find("p", {"class": "name"}).text
    name = name.strip().replace(" ",'')
    en_name = profile_box.find("span", {"class": "en"}).text

    info_box = profile_box.find("div", {"class": "box-info"})
    all_info = info_box.findAll("dt")
    
    info_arr = []
    for info in all_info:
        info_arr.append(info.text.strip())

    birthday, zodiac, height,birthplace, blood_type = info_arr
    print(blood_type)
    #get the text for all

def main():
    for i in range(1, MAX_MEMBER+1):
        # Only access girls who still in Keyaki
        if i not in NULL_MEMBERS:
            num = str(i)
            if ( len(num) == 1):
                num = '0' + num
            process_html(num)

if __name__ == "__main__":
    main()