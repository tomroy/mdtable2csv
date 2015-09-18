#!/usr/bin/python
#coding:utf-8
import io
import requests
from flask import abort, json

# filename = "mdtable.md"
# api_url = 'https://api.github.com'

def _read_file_or_404(filename, read_as_text=True):
    """
    Reads the contents of the specified file, or raise 404.
    """
    mode = 'rt' if read_as_text else 'rb'
    encoding = 'utf-8' if read_as_text else None
    try:
        with io.open(filename, mode, encoding=encoding) as f:
            return f.read()
    except IOError as ex:
        if ex.errno != errno.ENOENT:
            raise
        abort(404)

# render_text = _read_file_or_404(filename)
# print render_text

def render_content(text, api_url, gfm=False, context=None,
                   username=None, password=None):
    """
    Renders the specified markup using the GitHub API.
    """
    if gfm:
        url = '{}/markdown'.format(api_url)
        data = {'text': text, 'mode': 'gfm'}
        if context:
            data['context'] = context
        data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        headers = {'content-type': 'application/json; charset=UTF-8'}
    else:
        url = '{}/markdown/raw'.format(api_url)
        data = text.encode('utf-8')
        headers = {'content-type': 'text/x-markdown; charset=UTF-8'}

    auth = (username, password) if username or password else None
    r = requests.post(url, headers=headers, data=data, auth=auth)

    # Relay HTTP errors
    if r.status_code != 200:
        try:
            message = r.json()['message']
        except Exception:
            message = r.text
        abort(r.status_code, message)

    return r.text

# html_table = render_content(render_text, api_url, True, None, None, None)
# print html_table