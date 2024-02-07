import sqlite3

name = "blog.db"

conn = None

cursor = None

def open():
    global conn , cursor
    conn = sqlite3.connect(name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()


def close():
    cursor.close()
    conn.close()

def get_info():
    open()
    cursor.execute("SELECT* FROM user")
    res = cursor.fetchone()
    res = dict(res)
    close()
    return res

def get_id_category(category_name):
    open()
    cursor.execute('SELECT id FROM category WHERE category_name ==(?)', [category_name])
    res = cursor.fetchone()
    res = dict(res)
    close()
    return res['id']

def get_post_cat(id_cat):
    open()
    cursor.execute('SELECT* FROM post WHERE category_id ==(?)', [id_cat])
    res = cursor.fetchall()
    close()
    return res

def add_post(new_post):
    open()
    cursor.execute('INSERT INTO post (category_id, post_name, text, image) VALUES (?, ?, ?, ?)', [new_post["id_cat"], new_post["post_name"], new_post["text"], new_post["image"]])
    conn.commit()
    close()

def del_post(id):
    open()
    cursor.execute('DELETE FROM post WHERE id==(?)', [id])
    conn.commit()
    close()

def get_name_category(category_id):
    open()
    cursor.execute('SELECT category_name FROM category WHERE id ==(?)', [category_id])
    res = cursor.fetchone()
    res = dict(res)
    close()
    return res['category_name']

def get_post(id):
    open()
    cursor.execute('SELECT* FROM post WHERE id ==(?)', [id])
    res = cursor.fetchone()
    close()
    return res

def update_post(id, new_data):
    open()
    cursor.execute('UPDATE post SET post_name=(?), text=(?), image=(?) WHERE id==(?)', [new_data['post_name'],new_data['text'],new_data['image'],id])
    conn.commit()
    close()

def get_pass(login):
    open()
    cursor.execute('SELECT password FROM user WHERE login==(?)', [login])
    res = cursor.fetchone()
    res = dict(res)
    close()
    return res

def update_user(info):
    open()
    cursor.execute('UPDATE user SET name=(?), surname=(?), login=(?), password=(?), image=(?), avatar=(?), about_me_short=(?), about_me=(?) ', [info['name'], info['surname'], info['login'], info['password'], info['image'], info['avatar'], info['about_me_short'], info['about_me']])
    conn.commit()
    close()

if __name__ == "__main__":
    print(get_pass())