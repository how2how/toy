# -*- encoding: utf-8 -*-
from json import loads, dumps
from urllib import urlencode
from urllib2 import Request, urlopen

GH_API = 'https://api.github.com/'


def request(method='GET', url='https://api.github.com',
            data=None, headers=None):
    if data:
        data = urlencode(data)
    if method is 'GET' and data is not None:
        url += '?' + data
        data = None
    req = Request(url)
    req.headers = {'User-Agent': 'github-api',
                   'Accept': 'application/vnd.github.v3+json'}
    if headers:
        req.headers.update(headers)
    req.get_method = lambda: method
    data = dumps(data, ensure_ascii=False)
    print data
    try:
        print 'start to request'
        rsp = urlopen(req, data)
    except Exception as e:
        print e
        rsp = None
    return rsp


def auth_reqest(user, password, method='GET',
                url='https://api.github.com',
                data=None, headers=None):
    auth_hash = ':'.join((user, password)).encode('base64').strip()
    headers = headers or {}
    headers.update({'Authorization': 'Basic ' + auth_hash})
    return request(method=method, url=url, data=data, headers=headers)


def token_request(token, method='GET', url='https://api.github.com',
                  data=None, headers=None):
    headers = headers or {}
    headers.update({'Authorization': 'token ' + token})
    return request(method=method, url=url, data=data, headers=headers)


def put(token, content, path, repo, owner, msg='new file'):
    """
    PUT /repos/:owner/:repo/contents/:path
    """
    url = 'https://api.github.com/repos/%s/%s/contents/%s' % (owner, repo, path)
    data = {'message': msg, 'content': content.encode('base64')}
    return token_request(token, 'PUT', url, data)


def get(token, path, repo, owner):
    """
    GET /repos/:owner/:repo/contents/:path
    """
    url = 'https://api.github.com/repos/%s/%s/contents/%s' % (owner, repo, path)
    rsp = token_request(token, url=url)
    content = loads(rsp.read().strip()) if rsp else {}
    return content.get('content', '').decode('base64'), content


def update(token, content, path, sha, repo, owner, msg='update file'):
    """
    PUT /repos/:owner/:repo/contents/:path
    """
    url = 'https://api.github.com/repos/%s/%s/contents/%s' % (owner, repo, path)
    data = {'message': msg, 'content': content.encode('base64'), 'sha': sha}
    return token_request(token, 'PUT', url, data)


def delete(token, path, sha, repo, owner, msg='delete file'):
    """
    DELETE /repos/:owner/:repo/contents/:path
    """
    url = 'https://api.github.com/repos/%s/%s/contents/%s' % (owner, repo, path)
    data = {'message': msg, 'sha': sha}
    return token_request(token, 'DELETE', url, data)
