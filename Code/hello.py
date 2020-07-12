from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect
from wmy2 import *
from wmy3 import *
#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from JSON_to_SQL import *
from datetime import datetime, timedelta
import datetime as dtt
import operator
from functools import reduce
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="log")
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
        global now

        if user_1 and user_1[0][0] == 'wmy' and user_1[0][1] == '111':
            now = user_1[0][2]
            print('Audit department LOGIN SUCCESS!')
            return redirect('/admin')

        elif user_1 and user_1[0][0] == 'cjz' and user_1[0][1] == '111':
            now = user_1[0][2]
            print('SEE LOGIN SUCCESS!')
            return redirect('/admin')

        elif user_1 and user_1[0][0] == 'yby' and user_1[0][1] == '111':
            now = user_1[0][2]
            print('Developer LOGIN SUCCESS!')
            return redirect('/admin3')

        elif user_1 and key == user_1[0][1] and Find3(user_1[0][2], cursor)[0][3] == 1:
            now = user_1[0][2]
            print('LOGIN SUCCESS!')
            return redirect('/success.html')

        else:
            flash("输入错误或该用户没有此权限")
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
            Insert(user, pass1,2, db, cursor)
            return redirect('/login')
        else:
            flash("用户已存在或两次密码不一致")

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
        if user_1 and pass2 == pass3 and user == user_1[0][0] and pass1 == user_1[0][1] and Find3(user_1[0][2], cursor)[0][4] == 1:
            print("修改成功")
            Update(user, pass2, user_1[0][2], db, cursor)
            return redirect('/login')
        else:
            flash("输入错误或该用户没有此权限")
            print("修改失败")

            return render_template('forget.html')
    else:
        return render_template('forget.html')


@app.route('/success.html')
def success():
    return render_template('success.html',async_mode=socketio.async_mode)


@app.route('/success2.html' )
def succ2():
    return render_template('success2.html', async_mode=socketio.async_mode)

@app.route('/success3' )
def succ3():
    return render_template('success3.html', async_mode=socketio.async_mode)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html')
    if "Submit" in request.form:
        if Find3(now, cursor)[0][1] == 1:
            user = request.form.get('username')
            pass1 = request.form.get('pass1')
            level = request.form.get('department')
            level = int(level)
            user_1 = Find(user, cursor)
            if not user_1:
                Insert(user, pass1, level, db, cursor)
            else:
                Update(user, pass1, level, db, cursor)
        else:
            flash("您没有此权限")
    elif "Submit2" in request.form:
        if Find3(now, cursor)[0][1] == 1:
            user = request.form.get('username')
            user_1 = Find(user, cursor)
            if not user_1:
                flash("用户不存在")
            else:
                Delete(user, db, cursor)
        else:
            flash("您没有此权限")
    else:
        return render_template('admin.html')
    return render_template('admin.html')


@app.route('/admin3', methods=['GET', 'POST'])
def admin3():
    if request.method == 'GET':
        return render_template('admin3.html')


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('choosePlace', namespace='/test')
def test_choosePlace(message):
    global place
    place = str(message)
    print(place + "  is chosen!")

# 3 4 5 6  8 9 10 11 13 14 15 16


@socketio.on('allrights', namespace='/test')
def rights(message):
    x = Show3(cursor)
    print(x)

    Update3(0, message[2], message[3], message[4], message[5], db, cursor)
    Update3(1, message[7], message[8], message[9], message[10], db, cursor)
    Update3(2, message[12], message[13], message[14], message[15], db, cursor)

    y = Show3(cursor)
    print(y)


@socketio.on('search', namespace='/test')
def test_search(message):

    # message是天气情况
    datey =datetime.strptime(message, "%Y-%m-%d").date()
    i = 0
    while i < 7:
        datei = datey + dtt.timedelta(days= i)
        print("today is " + str(datei))
        y, m, d = str(datei).split("-", 2)
        datex = str(int(y)) + "/" + str(int(m)) + "/" + str(int(d))
        print("The date is " + str(datex))
        my_json = json.dumps(Find1(place, datex))
        emit('my_result', my_json)
        print("my_json : " + str(my_json))
        i = i + 1


@socketio.on('to_check', namespace='/test')
def to_check(message):
    x = Show3(cursor)
    y = reduce(operator.add, x)
    y = list(y)
    emit('to_check', y)


@socketio.on('to_fresh', namespace='/test')
def to_fresh(message):
    x = Show(cursor)
    y = reduce(operator.add, x)
    y = list(y)
    emit('to_fresh', y)


if __name__ == "__main__":
    app.run(port=4699, debug=True)
