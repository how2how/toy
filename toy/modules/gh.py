# -*- encoding: utf-8 -*-
from json import loads, dumps
# from urllib2 import Request, urlopen
try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request
import logging
fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt)


def _request(method='GET', uri=None, data=None, headers=None):
    url = 'https://api.github.com'
    url = uri if url in uri else (url + uri)
    req = Request(url)
    req.headers = {'User-Agent': 'github-api',
                   'Accept': 'application/vnd.github.v3+json'}
    if headers:
        req.headers.update(headers)
    req.get_method = lambda: method
    if data:
        data = dumps(data, ensure_ascii=False)
    try:
        logging.info('Start to request: %s' % url)
        logging.debug('Request data: %s' % data)
        rsp = urlopen(req, data)
    except Exception as e:
        logging.exception(e)
        rsp = None
    return rsp


def auth_reqest(user, password, method='GET', uri=None,
                data=None, headers=None):
    auth_hash = ':'.join((user, password)).encode('base64').strip()
    headers = headers or {}
    headers.update({'Authorization': 'Basic ' + auth_hash})
    return _request(method=method, uri=uri, data=data, headers=headers)


def token_request(token, method='GET', uri=None, data=None, headers=None):
    headers = headers or {}
    headers.update({'Authorization': 'token ' + token})
    return _request(method=method, uri=uri, data=data, headers=headers)


def request(upot, method='GET', uri=None, data=None, headers=None):
    if ':' in upot:
        user, password = upot.split(':', 1)
        return auth_reqest(user, password, method, uri, data, headers)
    return token_request(upot, method, uri, data, headers)


def put(owner, token, repo, path, content, msg='new file'):
    """
    PUT /repos/:owner/:repo/contents/:path
    """
    uri = '/repos/%s/%s/contents/%s' % (owner, repo, path)
    data = {'message': msg, 'content': content.encode('base64')}
    return request(token, 'PUT', uri, data)


def get(owner, token, repo, path):
    """
    GET /repos/:owner/:repo/contents/:path
    """
    uri = '/repos/%s/%s/contents/%s' % (owner, repo, path)
    rsp = request(token, uri=uri)
    content = loads(rsp.read().strip()) if rsp else {}
    return content.get('content', '').decode('base64'), content


def update(owner, token, repo, path, content, sha, msg='update file'):
    """
    PUT /repos/:owner/:repo/contents/:path
    """
    uri = '/repos/%s/%s/contents/%s' % (owner, repo, path)
    data = {'message': msg, 'content': content.encode('base64'), 'sha': sha}
    return request(token, 'PUT', uri, data)


def delete(owner, token, repo, path, sha, msg='delete file'):
    """
    DELETE /repos/:owner/:repo/contents/:path
    """
    uri = '/repos/%s/%s/contents/%s' % (owner, repo, path)
    data = {'message': msg, 'sha': sha}
    return request(token, 'DELETE', uri, data)


def get_raw(path, owner=None, repo=None, branch='master'):
    if path.startswith('http'):
        url = path
    else:
        raw_url = 'https://raw.githubusercontent.com'
        uri = '/%s/%s/%s/%s' % (owner, repo, branch, path)
        url = raw_url + uri
    try:
        rsp = urlopen(url).read()
    except Exception as e:
        logging.exception(e)
        rsp = ''
    return rsp
