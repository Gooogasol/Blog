#головний файл який усе зв'язує
from flask import Flask, session, request, render_template, redirect, url_for
from settings import*
from db_File import*

app = Flask(__name__, static_folder = STATIC , template_folder= TEMPLATE)

app.config["SECRET_KEY"] = sec


@app.route('/')
@app.route('/index')
def index():
    try:
        session['login'] = session['login']
    except:
        session['login'] = False
    user = get_info()
    return render_template('Index.html', user = user)

@app.route('/post/<category>', methods =["GET", "POST"])
def post_category(category):
    id_cat = get_id_category(category)
    post = get_post_cat(id_cat)
    error_list = list() 
    if request.method == "POST":
        info = request.form.copy()
        info = dict(info)
        info['id_cat'] = id_cat
        image = request.files['image']
        if image:
            image.save(f'{UPPLOADS}/{image.filename}')
            info["image"] = f'upploads/{image.filename}'
        else:
            info['image'] = None
        if info['post_name']=='':
            error_list.append("Ім'я посту не може бути порожнім.")
        if info['text']=='':
            error_list.append("Текст посту не може бути порожнім.")
        if len(error_list)==0:
            add_post(info)
            return redirect(url_for('post_category', category = category))
        else:
            return render_template('post.html', post = post, error_list = error_list)
    return render_template('post.html', post = post)

@app.route('/post/edit/<post_id>/<category_id>', methods =["GET", "POST"])
def post_edit(post_id,category_id):
    post = get_post(post_id)
    error_list = list()
    if request.method == "POST":
        info = request.form.copy()
        info = dict(info)
        info['id_cat'] = category_id
        image = request.files['image']
        if image:
            image.save(f'{UPPLOADS}/{image.filename}')
            info["image"] = f'upploads/{image.filename}'
        else:
            info['image'] = info['old_image']
        if info['post_name']=='':
            error_list.append("Ім'я посту не може бути порожнім.")
        if info['text']=='':
            error_list.append("Текст посту не може бути порожнім.")
        if len(error_list)==0:
            update_post(post_id,info)
            category = get_name_category(category_id)
            return redirect(url_for('post_category', category = category))
        else:
            return render_template('post_edit.html', post = post, error_list = error_list)
    return render_template('post_edit.html', post = post)

@app.route('/about')
def about():
    user = get_info()
    return render_template('about.html', user = user)

@app.route('/post/del/<post_id>/<category_id>')
def delete_post(post_id,category_id):
    del_post(post_id)
    category = get_name_category(category_id)
    return redirect(url_for('post_category', category = category))

# @app.route("/post/edit/<post_id>", methods = ["GET", "POST"])
# def post_edit(post_id):
#     if request.method == "POST":
#         if request.method.get('back'):
#             id = request.form.get('id')
#             post = get_post(id)
#             category = get_name_category(post['category_id'])
#             return redirect(url_for('post_category', category = category))      
#     post = get_post(id)
#     return render_template('post_edit.html', post = post)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if session['login'] == False:
        if request.method == "POST":
            error_list = list()
            login = request.form.get('login')
            password = request.form.get('password')
            pass_bd = get_pass(login)
            if pass_bd == None:
                error_list.append('Невірний логін')
                return render_template('login', error_list = error_list)
            else:
                if password != pass_bd['password']:
                    error_list.append('Невірний пароль.')
                    return render_template('login', error_list = error_list)
                else:
                    session['login'] = True
                    return redirect(session['back'])
                    
        else:
            session['back'] = request.referrer
            return render_template('login.html')
    else:
        session['login'] = False
        return redirect(request.referrer)
    
@app.route("/post/view/<post_id>")
def post_view(post_id):
    post = get_post(post_id)
    category = get_name_category(post['category_id'])
    return render_template('post_view.html', post = post, category = category)


@app.route("/user/edit", methods = ["POST", "GET"])
def user_edit():
    error_list = list()
    user = get_info()
    if request.method == "POST":
        info = request.form.copy()
        info = dict(info)
        image = request.files['image']
        if image:
            image.save(f'{image.filename}')
            info["image"] = f'{image.filename}'
        else:
            info['image'] = info['old_image']
        avatar = request.files['avatar']
        if avatar:
            avatar.save(f'{avatar.filename}')
            info["avatar"] = f'{avatar.filename}'
        else:
            info['avatar'] = info['old_avatar']
        if info['name']=='':
            error_list.append("Ім'я не може бути порожнім.")
        if info['surname']=='':
            error_list.append("Прізвище не може бути порожнім.")
        if info['login']=='':
            error_list.append("Логін не може бути порожнім.")
        if info['password']=='':
            error_list.append("Пароль не може бути порожнім.")
        else:
            if info['password']!= info['password2']:
                error_list.append("Паролі не співпадають.")
        if len(error_list)==0:
            update_user(info)
            user = get_info()
            return redirect(url_for('about', user = user))
        else:
            return render_template('user_edit.html', user = user, error_list = error_list)
    return render_template('user_edit.html', user = user, error_list = error_list)
if __name__ == "__main__":
    app.run(debug = True)