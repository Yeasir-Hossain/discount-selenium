import requests
import sys
from urllib.parse import urlparse


def req(url, method='get', json=None):
    headers = {"content-type": "application/json"}
    sessionUrl = parseSessionId(url)

    try:
        if method.lower() == 'get':
            response = requests.get(url, headers=headers)
        elif method.lower() == 'post':
            response = requests.post(url, json=json, headers=headers)
        elif method.lower() == 'delete':
            response = requests.delete(url, json=json, headers=headers)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        print(e.response.text)
        req(sessionUrl, method='delete')
        sys.exit(1)
    except Exception as e:
        print(e)
        req(sessionUrl, method='delete')
        sys.exit(1)


def parseSessionId(url):
    parsedUrl = urlparse(url)
    pathComponents = parsedUrl.path.split('/')

    # Find the index of 'session' in the path
    sessionIndex = pathComponents.index(
        'session') + 1 if 'session' in pathComponents else -1

    # Check if there is a subsequent component after 'session'
    if sessionIndex < len(pathComponents):
        # Construct the URL up to the session ID
        url_up_to_session_id = parsedUrl.scheme + '://' + \
            parsedUrl.netloc + '/'.join(pathComponents[:sessionIndex + 1])
        return url_up_to_session_id
    else:
        return None
