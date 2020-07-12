import pymysql
import json

# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="log")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()
print("Database version : %s " % data)


# cursor.execute("DROP TABLE IF EXISTS json")# 删除json表

#建名为json的表 执行完一次后请注释
# sql = """CREATE TABLE IF NOT EXISTS json(
#    city VARCHAR(20) NOT NULL,
#    date VARCHAR(20) NOT NULL,
#    min FLOAT(10) NOT NULL,
#    max FLOAT(10) NOT NULL
# )DEFAULT CHARSET=utf8mb4"""
# cursor.execute(sql)


# 保存到数据库
def DateSave(city, date, min, max):
    # 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
    db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="log")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = 'Insert into json(city, date, min, max) values("%s","%s","%s","%s")' % (city, date, min, max)
    cursor.execute(sql)  # 执行命令
    db.commit()  # 提交到数据库
    db.close()


# 根据城市与时间查找数据
def Find1(city, date):
    # 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
    db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="log")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL查找记录语句
    sql = "SELECT * FROM json WHERE city = '%s' and date = '%s'" % (city, date)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 向数据库提交
        results = cursor.fetchall()
        for row in results:
            city = row[0]
            date = row[1]
            min = row[2]
            max = row[3]
            # 打印结果
            print("city='%s',date='%s',min='%s',max='%s'" % (city, date, min, max))
        return results[0]
    except:
        # 发生错误时回滚
        print('error')
        db.rollback()
    db.close()

# 展示json表中所有数据
def Show1():
    # 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
    db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="log")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "SELECT * FROM json"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        city = row[0]
        date = row[1]
        min = row[2]
        max = row[3]
        # 打印结果
        print("city='%s',date='%s',min='%s',max='%s'" % (city, date, min, max))
    db.close()
# 读取json文件并存入数据库，执行一次后请注释
a = open(r"zhe_jiang_forecast.json", "r")
source = a.read()
source = json.loads(source)
length = len(source)
for x in range(0, length):
    DateSave(source[x]['city'], source[x]['DATE'], source[x]['min'], source[x]['max'])
Show1()