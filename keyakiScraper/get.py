# Modified from https://realpython.com/python-web-scraping-practical-introduction/
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

HTML_SOURCE='http://www.keyakizaka46.com/s/k46o/search/artist?ima=0000'

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


def main():
    raw_html = simple_get(HTML_SOURCE)
    html = BeautifulSoup(raw_html, 'html.parser')
    images = html.findAll('img')
    for image in images:
        print(image['src'])
    raw_html = simple_get("http://cdn.keyakizaka46.com/images/14/eeb/23f672b0c99925d3d9495c67306f0/400_320_102400.jpg")
    



if __name__ == "__main__":
    main()
