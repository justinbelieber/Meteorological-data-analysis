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


# cursor.execute("DROP TABLE IF EXISTS test2")
# sql = """CREATE TABLE test2 (
#      level INT(5),
#      add_delete INT(5),
#      change1 INT(5),
#      search1 INT(5),
#      key_change INT(5))"""
#
# cursor.execute(sql)


def Insert3(level, add_delete, change1, search1, key_change, db, cursor):
    sql = """INSERT INTO test2(level, add_delete, change1, search1, key_change) \
          VALUES('%d', '%d', '%d', '%d', '%d')""" % (level, add_delete, change1, search1, key_change)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        print('error')
        db.rollback()


def Update3(level, add_delete, change1, search1, key_change, db, cursor):
    # SQL 更新语句
    sql = "UPDATE test2 SET add_delete = %d WHERE level = %d" % (add_delete, level)
    sql1 = "UPDATE test2 SET change1 = %d  WHERE level = %d" % (change1, level)
    sql2 = "UPDATE test2 SET search1 = %d  WHERE level = %d" % (search1, level)
    sql3 = "UPDATE test2 SET key_change = %d  WHERE level = %d" % (key_change, level)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()

        cursor.execute(sql1)
        # 提交到数据库执行
        db.commit()

        cursor.execute(sql2)
        # 提交到数据库执行
        db.commit()

        cursor.execute(sql3)
        # 提交到数据库执行
        db.commit()

    except:
        # 发生错误时回滚
        print('error')
        db.rollback()


def Show3(cursor):
    sql = "SELECT * FROM test2"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        level = row[0]
        add_delete = row[1]
        change1 = row[2]
        search1 = row[3]
        key_change = row[4]
        # 打印结果
        print("level=%d,add_delete=%d,change1=%d,search1=%d,key_change=%d" % (level, add_delete, change1, search1, key_change))
    return results


def Delete3(level, db, cursor):
    # SQL删除记录语句
    sql = "DELETE FROM test2 WHERE level = %d" % level
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 向数据库提交
        db.commit()
    except:
        # 发生错误时回滚
        print('error')
        db.rollback()


def Find3(level, cursor):
    # SQL查找记录语句
    sql = "SELECT * FROM test2 WHERE level = %d" % level
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 向数据库提交
        results = cursor.fetchall()
        for row in results:
            level = row[0]
            add_delete = row[1]
            change1 = row[2]
            search1 = row[3]
            key_change = row[4]
            # 打印结果
            print("level=%d,add_delete=%d,change1=%d,search1=%d,key_change=%d" % (level, add_delete, change1, search1, key_change))
    except:
        # 发生错误时回滚
        print('error')
        db.rollback()

    return results


# Insert3(0, 1, 1, 1, 1, db, cursor)
# Insert3(1, 0, 0, 0, 0, db, cursor)
# Insert3(2, 0, 0, 1, 1, db, cursor)

# # Update('yby', '111', 0, db, cursor)
# # # Delete('yby')
# Show3(cursor)

db.close()
