import sys
import io
import errno
import requests  # type: ignore
from flask import abort, json
from bs4 import BeautifulSoup, Tag
from typing import cast, Optional


def _read_file_or_404(filename: str, read_as_text: bool = True):
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


def render_content(
    text: str,
    api_url: str,
    gfm: bool = False,
    context: str | None = None,
    username: str | None = None,
    password: str | None = None,
):
    """
    Renders the specified markup using the GitHub API.
    """
    if gfm:
        url = '{}/markdown'.format(api_url)
        data_dict = {'text': text, 'mode': 'gfm'}
        if context:
            data_dict['context'] = context
        body_bytes = json.dumps(data_dict, ensure_ascii=False).encode('utf-8')
        headers = {'content-type': 'application/json; charset=UTF-8'}
    else:
        url = '{}/markdown/raw'.format(api_url)
        body_bytes = text.encode('utf-8')
        headers = {'content-type': 'text/x-markdown; charset=UTF-8'}
    auth = (username, password) if username or password else None
    r = requests.post(url, headers=headers, data=body_bytes, auth=auth)
    if r.status_code != 200:
        try:
            message = r.json()['message']
        except Exception:
            message = r.text
        abort(r.status_code, message)
    return r.text


def mdtable2csv(input_path: str, output_path: Optional[str] = None) -> str:
    if not input_path.endswith('.md'):
        raise ValueError("the file format should be *.md")

    render_text = _read_file_or_404(input_path)
    api_url = 'https://api.github.com'
    html_table = render_content(render_text, api_url, True, None, None, None)

    soup = BeautifulSoup(html_table, "html.parser")
    table = soup.table
    if table is None:
        raise RuntimeError("no <table> element found in rendered HTML")
    table_tag = cast(Tag, table)

    out_path = output_path or (input_path[0:input_path.find('.')] + '.csv')
    f = open(out_path, 'w')

    rows = table_tag.find_all('tr')
    if not rows:
        raise RuntimeError("no table rows found")

    first_row = cast(Tag, rows[0])
    ths = first_row.find_all('th')

    write_th_to_file = ''
    for th in ths:
        th_tag = cast(Tag, th)
        if th_tag.string is not None:
            write_th_to_file += (th_tag.string + ',')
        else:
            write_th_to_file += (' ' + ',')
    write_th_to_file = write_th_to_file[:-1]

    f.write(write_th_to_file)
    f.write('\n')

    for row in rows[1:]:
        write_td_to_file = ''
        row_tag = cast(Tag, row)
        tds = row_tag.find_all('td')
        for td in tds:
            td_tag = cast(Tag, td)
            if td_tag.string is not None:
                write_td_to_file += (td_tag.string + ',')
            else:
                write_td_to_file += (' ' + ',')
        write_td_to_file = write_td_to_file[:-1]
        f.write(write_td_to_file)
        f.write('\n')

    f.close()
    return out_path


def main() -> int:
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        print("please put sys.argv[1] as filename !!")
        return 1
    try:
        _ = mdtable2csv(filename)
    except Exception as ex:
        print(str(ex))
        return 1
    print("convertion successfully done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


