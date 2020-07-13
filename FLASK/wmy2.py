import pymysql

# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）

db = pymysql.connect(host="127.0.0.1", port=3306, user="FYEWARD", password="101774939yby", db="log")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()
print("Database version : %s " % data)


#cursor.execute("DROP TABLE IF EXISTS test")
# sql = """CREATE TABLE test (
#      name CHAR(20) NOT NULL PRIMARY KEY,
#      pwd CHAR(20))DEFAULT CHARSET = utf8mb4"""
# cursor.execute(sql)


def Insert(name, pwd, db, cursor):
    sql = """INSERT INTO test(name, pwd) \
          VALUES('%s', '%s')""" % (name, pwd)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        print('error')
        db.rollback()


def Update(name, pwd, db, cursor):
    # SQL 更新语句
    sql = "UPDATE test SET pwd = '%s' WHERE name = '%s'" % (pwd, name)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        print('error')
        db.rollback()


def Show(cursor):
    sql = "SELECT * FROM test"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        pwd = row[1]
        name = row[0]
        # 打印结果
        print("pwd=%s,name=%s" % (pwd, name))
    return results


def Delete(name, db, cursor):
    # SQL删除记录语句
    sql = "DELETE FROM test WHERE name = '%s'" % name
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 向数据库提交
        db.commit()
    except:
        # 发生错误时回滚
        print('error')
        db.rollback()


def Find(name, cursor):
    # SQL查找记录语句
    sql = "SELECT * FROM test WHERE name = '%s'" % name
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 向数据库提交
        results = cursor.fetchall()
        for row in results:
            name = row[0]
            pwd = row[1]
            # 打印结果
            print("name='%s',pwd='%s'" % (name, pwd))
    except:
        # 发生错误时回滚
        print('error')
        db.rollback()

    return results


Insert("yby", "18301114", db, cursor)
Insert("mac", "18301114", db, cursor)
x = Find('yby', cursor)
Update('yby', '111', db, cursor)
# Delete('yby')
# Show()
print(x[0])
db.close()
