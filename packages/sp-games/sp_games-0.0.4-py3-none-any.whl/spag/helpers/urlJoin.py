try:
    import urlparse
    from urllib import urlencode
except:
    import urllib.parse as urlparse
    from urllib.parse import urlencode


def join_url(base_url, extension, url_parameters):
    url = base_url + extension
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(url_parameters)

    url_parts[4] = urlencode(query)
    url = urlparse.urlunparse(url_parts)

    return url
