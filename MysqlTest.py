import pymysql

db = pymysql.connect('localhost', 'root', 'root', 'jason_sogou')
# 这里建立游标的时候已经默认开启了一个隐形的数据库事务
cursor = db.cursor()

# 创建表结构
# sql = '''
#     create table python_test(
#         id int not null auto_increment,
#         name varchar(20) not null,
#         age int not null,
#         primary key(id)
#     )engine=innodb;
# '''
# cursor.execute(sql)

# 插入操作
# sql = 'insert into python_test(name, age) values("linjie", 20)'
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()

# 查询操作
sql = 'select * from python_test'
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    # 这里查到的每个结果是一个元组
    for row in result:
        print(row)
except:
    print('error: unable to fetch data')

# 更新操作
# sql = 'update python_test set age=100 where name="linjie"'
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()
#     print('udpate fail')

# 删除操作
sql = 'delete from python_test where name="linjie"'
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    print('delete fail')

# 关闭链接
db.close()
