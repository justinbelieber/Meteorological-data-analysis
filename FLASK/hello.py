import execjs
from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect
from wmy2 import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

db = pymysql.connect(host="127.0.0.1", port=3306, user="FYEWARD", password="101774939yby", db="log")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()
print("Database version : %s " % data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('request achieve!')
    if request.method == 'GET':
        return render_template('login.html')
    # 获取POST传值

    if "btu" in request.form:
        user = request.form.get('username')
        key = request.form.get('pass')
        user_1 = Find(user, cursor)
        print(user_1)
        print('LOGIN')

        if user_1 and user == 'bbb' and key == 'bbbbbb':
            print('Audit department LOGIN SUCCESS!')
            return redirect('/admin2')

        elif user_1 and user == 'aaa' and key == 'aaaaaa':
            print('Developer LOGIN SUCCESS!')
            return redirect('/admin')

        elif user_1 and user == user_1[0][0] and key == user_1[0][1]:
            print('LOGIN SUCCESS!')
            return redirect('/success')

        else:
            flash("请输入正确的用户名和密码")
            return render_template('login.html')

    # elif "btn" in request.form:
    #     return render_template('register.html')

    elif "btu2" in request.form:
        print("游客登录")
        return redirect('/success3')

    elif "btn" in request.form:
        return redirect('/register')

    elif "btu3" in request.form:
        print("忘记密码")
        return redirect('/forget')

    else:
        return render_template('login.html')
    # 获取GET传值
    # request.args


@app.route('/register', methods=['GET', 'POST'])
def register():
    print('request achieve!')
    if request.method == 'GET':
        return render_template('register.html')
    # 获取POST传值
    user = request.form.get('username')
    pass1 = request.form.get('pass1')
    pass2 = request.form.get('upassword')
    user_1 = Find(user, cursor)
    print(pass1, pass2)
    if "btn" in request.form:
        if pass1 == pass2 and not user_1:
            print("注册成功")
            Insert(user, pass1, db, cursor)
            return redirect('/login')
        else:
            flash("两次密码不一致")

            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/forget', methods=['GET', 'POST'])
def forget():
    print('request achieve!')
    if request.method == 'GET':
        return render_template('forget.html')
    # 获取POST传值
    user = request.form.get('username')
    pass1 = request.form.get('pass2')
    pass2 = request.form.get('pass1')
    pass3 = request.form.get('upassword')
    user_1 = Find(user, cursor)
    print(pass1, pass2)
    if "btn" in request.form:
        print("信息接收成功")
        if user_1 and pass2 == pass3 and user == user_1[0][0] and pass1 == user_1[0][1] :
            print("修改成功")
            Update(user, pass2, db, cursor)
            return redirect('/login')
        else:
            d=1000

            print("修改失败")

            return render_template('forget.html')
    else:
        return render_template('forget.html')


@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')


@app.route('/success3', methods=['GET', 'POST'])
def success3():
    return render_template('success3.html')


@app.route('/admin2', methods=['GET', 'POST'])
def admin2():
    if request.method == 'GET':
        return render_template('admin2.html')
    if "Submit3" in request.form:
        print("刷新用户")
        ft = Show(cursor)
        for x in ft:
            i = x[0]
            j = x[1]
            flash("用户名：%s 密码：%s" % (i, j))
    return render_template('admin2.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html')
    if "Submit3" in request.form:
        print("刷新用户")
        ft = Show(cursor)
        for x in ft:
            i = x[0]
            j = x[1]
            flash("用户名：%s 密码：%s" % (i, j))
    if "Submit" in request.form:
        print("新增用户")
        user = request.form.get('username1')
        pass1 = request.form.get('password')
        user_1 = Find(user, cursor)
        if not user_1 and pass1:
            Insert(user, pass1, db, cursor)
            ft = Show(cursor)
            for x in ft:
                i = x[0]
                j = x[1]
                flash("用户名：%s 密码：%s" % (i, j))
        else:
            flash("用户存在或未设置密码")
    if "Submit2" in request.form:
        print("删除用户")
        user = request.form.get('username1')
        user_1 = Find(user, cursor)
        if user_1 and user == user_1[0][0]:
            Delete(user, db, cursor)
            ft = Show(cursor)
            for x in ft:
                i = x[0]
                j = x[1]
                flash("用户名：%s 密码：%s" % (i, j))
        else:
            flash("找不到用户")
    return render_template('admin.html')


if __name__ == "__main__":
    db.close()
    app.run(port=1112)



