import pymysql

# 连接到 MySQL 数据库
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='971101',
                             database='house',
                             charset='utf8mb4')

try:
    # 创建游标
    with connection.cursor() as cursor:
        # 执行查询语句
        sql = "SHOW TABLES;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
finally:
    # 关闭游标和连接
    connection.close()