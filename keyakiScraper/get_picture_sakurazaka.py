import os
import re
import json
import urllib
import argparse
import collections
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

MAIN_SRC='https://sakurazaka46.com/s/s46/search/artist'
BASE_SRC='https://sakurazaka46.com'

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

def get_members_link():
    members_links = set()
    raw_html = simple_get(MAIN_SRC)
    html = BeautifulSoup(raw_html, 'html.parser')
    for li in html.findAll('li', {"class": "box"}):
        for a in li.findAll("a"):
            curr_profile_link = a['href']
            curr_profile_link = re.sub(r'\?ima=[0-9]*', '', curr_profile_link)
            if curr_profile_link not in members_links:
                members_links.add(curr_profile_link)
    return sorted(members_links)

def get_image(member_link_bs_html, num):
    """Get the image link and download fullsize
    @params:
        members_link: BeautifulSoup object that contain tags from profile link
    """
    img_box = member_link_bs_html.find("p", {"class": "ph"})
    img_link = BASE_SRC + img_box.find("img")['src']
    print(img_link)

    name_file = IMAGE_DST + num + ".jpg"
    try:
        urllib.request.urlretrieve(img_link, name_file)
    except URLError:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))    

def download_images_and_profiles(members_links):
    # Initialization and declaration
    data = collections.OrderedDict()

    # Create directory if image path does not exist
    if not os.path.exists(IMAGE_DST):
        os.makedirs(IMAGE_DST)

    # Go through each members profile link
    for member_link in members_links:
        num = member_link.split('/')[4]

        member_link_raw_html = simple_get(BASE_SRC + member_link)
        member_link_bs_html = BeautifulSoup(member_link_raw_html, 'html.parser')

        get_image(member_link_bs_html, num)
        data[num] = get_profile(member_link_bs_html)
    
    # Save the profile
    with open(JSON_DST, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

    # Change to how many profiles been saved
    print("All members' profile have been saved")
    print("Images are saved in:", IMAGE_DST)
    print("Profiles are saved in:", JSON_DST)
    


def get_profile(html):
    """Get the image link and gather the profile details
    @params:
        object html:BeautifulSoup object that contain tags from profile link
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


def process_html():
    """Read the profile links, download profile image,
    get profile data and dumps into json
    """
    print("Gathering members' profile")
    members_links = get_members_link()
    download_images_and_profiles(members_links)

def main():
    global IMAGE_DST
    global JSON_DST
    parser = argparse.ArgumentParser(description='Get Keyakizaka46 data profile and pictures')
    parser.add_argument('-i', '--image',
                    help='specify the path to save the image')
    parser.add_argument('-d', '--data',
                    help='specify the path to save the profile data')
    args = parser.parse_args()
    if args.image:
        if args.image[len(args.image)-1] != '/':
            args.image += '/'
        IMAGE_DST = args.image
    if args.data:
        if args.data[len(args.data)-1] != '/':
            args.data += '/'        
        JSON_DST = args.data + JSON_DST
    process_html()

if __name__ == "__main__":
    main()
