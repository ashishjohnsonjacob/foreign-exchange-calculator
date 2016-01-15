from urllib.request import urlopen
from urllib.error import URLError


def load_page(url: str) -> str:
    """ Returns the content of the web page for a valid url.
        Otherwise it returns the empty string.
    """
    try:
        response = urlopen(url)

        if response.status == 200:
            body_text = str(response.read())
            return body_text
        return ""
    except URLError:
        return ""