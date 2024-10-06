#!/bin/bash

# 数据库配置
DB_USER="root"
DB_PASSWORD="971101"
DB_HOST="localhost"
DB_NAME="house"

# MySQL客户端路径
MYSQL=/usr/bin/mysql

# 检查MySQL客户端是否存在
if [ ! -f "$MYSQL" ]; then
    echo "MySQL客户端未找到"
    exit 1
fi

# 初始化库
$MYSQL -u"$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" < db_init.sql
# 检查脚本执行结果
if [ $? -eq 0 ]; then
    echo "house db 创建成功"
else
    echo "house db 创建失败"
fi

# 创建nc表
$MYSQL -u"$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" "$DB_NAME" < house_lianjia_nc_create.sql
if [ $? -eq 0 ]; then
    echo "nc_表创建成功"
else
    echo "nc_表创建失败"
fi

# 创建nc_new表
$MYSQL -u"$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" "$DB_NAME" < house_new_table.sql
if [ $? -eq 0 ]; then
    echo "nc_new表创建成功"
else
    echo "nc_new表创建失败"
fi