import handler
from jinja2 import Template, Environment, FileSystemLoader
import sqlite3
from urllib import parse

urls = {}

def url_for(link):
    if link in urls:
        return urls[link][9:]
    return 'null'

def https_handle(link, urlfor):
    def deco(func):
        def inner(*args, **kwargs):
            res = func(*args, **kwagrs)
            return res
        urls[urlfor] = link
        handler.template_dict[link] = func
        return inner
    return deco

def get_template(content):
    template = Environment(loader=FileSystemLoader('static/')).from_string(content)
    template.globals['url_for'] = url_for
    return template

@https_handle('./static/index.html', 'index')
def index(content, query, method):
    if (method != 'GET'):
        return '405 method not allowed', 405

    template = get_template(content)
    result = template.render()
    return result, 200

@https_handle('./static/board.html', 'board')
def board(content, query, method):
    if (method != 'GET'):
        return '405 method not allowed', 405

    if 'board' not in query:
        query['board'] = 'notice'

    conn = sqlite3.connect("./blog.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            f'select `id`, `title`, `author`, `time` from {query["board"]}')
    except Exception as e:
        return str(e), 503

    rows = cursor.fetchall()

    template = get_template(content)
    result = template.render(rows=rows, board_title=query['board'])
    return result, 200

@https_handle('./static/board_view.html', 'board_view')
def board_view(content, param, method):
    if (method != 'GET'):
        return '405 method not allowed', 405

    if 'id' not in param or not param['id'].isdecimal():
        return 'invalid parameter', 400
    

    id = int(param['id'])

    conn = sqlite3.connect("./blog.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            'select `title`, `content`, `author`, `time`'
            f'from {param["board"]} where id = {id}')

    except Exception as e:
        return str(e), 503

    row = cursor.fetchone()
    row = list(row)

    if row is None:
        return 'post not exist', 404

    post_name = row[1]
    path = f'./static/posts/{post_name}'

    import os.path
    if not os.path.exists(path):
        return f'internal server error. post name: {post_name}', 500

    with open(path, 'r', encoding='utf8') as f:
        row[1] = f.read()

    template = get_template(content)
    result = template.render(row=row, board_title=param["board"])

    return result, 200

@https_handle('./static/board_write.html', 'board_write')
def board_write(content, query, method):
    if (method != 'GET'):
        return '405 method not allowed', 405

    if query['board'] != 'free':
        return f"<script>alert('You do not have permission.');location.href='./board.html?board={query['board']}'</script>", 200

    template = get_template(content)
    result = template.render(board_title=query['board'])
    return result, 200

@https_handle('./static/write.html', 'write')
def write(content, query, method):
    if (method != 'POST'):
        return '405 method not allowed', 405

    conn = sqlite3.connect("./blog.db")
    cursor = conn.cursor()

    if query['board_title'] != 'free':
        return f"<script>alert('You do not have permission.');location.href='./board.html?board={query['board_title']}'</script>", 400

    if len(query['title']) == 0 or len(query['content']) == 0 or len(query['author']) == 0:
        return f"<script>alert('invalid title, content, or author');location.href='./board.html?board={query['board_title']}'</script>", 400
    
    try:
        cursor.execute(f"select count(*) from `{query['board_title']}`")
        num = cursor.fetchone()[0]
    except Exception as e:
        return str(e), 503

    filename = f"{query['board_title']}{num}.html"
    with open(f'./static/posts/{filename}', "w", encoding='utf-8') as f:
        f.write(parse.unquote_plus(query['content']))
    
    try:
        import time
        now = time.localtime()
        cursor.execute(f"select count(*) from `{query['board_title']}`")
        sql = f"insert into `{parse.unquote_plus(query['board_title'])}` (`title`, `content`, `author`, `time`) values ('{parse.unquote_plus(query['title'])}', '{filename}', '{parse.unquote_plus(query['author'])}', '{now.tm_year}/{now.tm_mon}/{now.tm_mday}')"
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        return str(e), 503

    return f"<script>location.href='./board_view.html?board={query['board_title']}&id={num + 1}'</script>", 200


def main():
    handler.start_server()
    
if __name__ =="__main__":
    main()
