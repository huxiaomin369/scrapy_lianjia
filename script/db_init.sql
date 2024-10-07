-- 检查数据库是否存在，如果不存在则创建
CREATE DATABASE IF NOT EXISTS house
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 检查用户是否存在，如果不存在则创建
CREATE USER IF NOT EXISTS 'mhu'@'172.18.0.1' IDENTIFIED BY '971101';

-- 授予用户对数据库的权限
/* GRANT ALL PRIVILEGES ON house.* TO 'root'@'localhost'; */

GRANT ALL PRIVILEGES ON house.* TO 'mhu'@'172.18.0.1';

-- 应用权限更改
FLUSH PRIVILEGES;