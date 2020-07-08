import pymysql
import json
import pandas as pd
from datetime import datetime
from dateutil import parser
import sqlalchemy


# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
db = pymysql.connect(host="192.168.0.104", port=3306, user="test", password="18301108", db="log")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()
print("Database version : %s " % data)

# cursor.execute("DROP TABLE IF EXISTS json")
# sql = """CREATE TABLE IF NOT EXISTS json(
#    city VARCHAR(20) NOT NULL,
#    date VARCHAR(20) NOT NULL,
#    min FLOAT(10) NOT NULL,
#    max FLOAT(10) NOT NULL
# )DEFAULT CHARSET=utf8mb4"""
# cursor.execute(sql)


def DateSave(city, date, min, max):
    sql = 'Insert into json(city, date, min, max) values("%s","%s","%s","%s")' % (city, date, min, max)
    cursor.execute(sql)


def Find(city, date):
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
    except:
        # 发生错误时回滚
        print('error')
        db.rollback()


def Show():
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


# a = open(r"xin_jiang_forecast.json", "r")
# source = a.read()
# source = json.loads(source)
# length = len(source)
# for x in range(0, length):
#     DateSave(source[x]['city'], source[x]['DATE'], source[x]['min'], source[x]['max'])
#     db.commit()

# cursor.execute(sql)
# Show()
Find('xin_jiang', '2020/12/31')
# sql = "SELECT * FROM json WHERE city = '%s' and date = '%s'" % ('xin_jiang', '2020-01-01')
# # 执行SQL语句
# cursor.execute(sql)
# # 向数据库提交
# results = cursor.fetchall()
# for row in results:
#     city = row[0]
#     date = row[1]
#     min = row[2]
#     max = row[3]
#     # 打印结果
#     print("city='%s',data='%s',min='%s',max='%s'" % (city, date, min, max))
db.close()