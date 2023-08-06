import requests
import urllib


def unquote_url(url):
    return urllib.unquote(url).decode('utf8')


def download_file(url, local_filename):
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
