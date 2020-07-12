import pymysql

# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）

db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="log")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()
print("Database version : %s " % data)


# cursor.execute("DROP TABLE IF EXISTS test")
# sql = """CREATE TABLE test (
#      name CHAR(20) NOT NULL PRIMARY KEY,
#      pwd CHAR(20),
#      level INT(5))DEFAULT CHARSET = utf8mb4"""
#
# cursor.execute(sql)


def Insert(name, pwd, level, db, cursor):
    sql = """INSERT INTO test(name, pwd, level) \
          VALUES('%s', '%s', '%d')""" % (name, pwd, level)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        print('error')
        db.rollback()


def Update(name, pwd, level, db, cursor):
    # SQL 更新语句
    sql = "UPDATE test SET pwd = '%s' WHERE name = '%s'" % (pwd, name)
    sql1 = "UPDATE test SET level = %d  WHERE name = '%s'" % (level, name)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()

        cursor.execute(sql1)
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
        level = row[2]
        # 打印结果
        print("pwd=%s,name=%s,level=%d" % (pwd, name, level))
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
            level = row[2]
            # 打印结果
            print("name='%s',pwd='%s',level=%d" % (name, pwd, level))
    except:
        # 发生错误时回滚
        print('error')
        db.rollback()

    return results


# Insert("cjz", "111", 0, db, cursor)
# Insert("wmy", "111", 1, db, cursor)
# Insert('yby', '111', 0, db, cursor)
# # Delete('yby')
# Show(cursor)

db.close()
