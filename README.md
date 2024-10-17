# scrapy_lianjia
scrapy爬虫 爬取nc链家房价数据

## 项目描述
本项目基于scrapy框架开发，包含两个爬虫
### 1、代理服务器爬虫
爬取几个免费代理网站的服务器，验证有效性并存入redis数据库
### 2、房价爬虫
读取redis缓存的代，使用代理进行爬取，爬取过程中会自动删除redis数据库中的无效代理，并将爬取到的房价数据存入MySQL数据库

## 使用
docker 一键部署 (2024 new)
``` sh
cd docker
docker-compose up -d

# 初始化mysql
## 进入mysql 容器
docker exec -it mysql /bin/bash
## 初始化数据库
bash initmysql.sh
```

## tips 
lianjia已有反爬虫机制，需要登录验证，且登录加密，目前只能手动指定cookie中的token才能爬取

```sh
# chrome 驱动
https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
wget https://chromedriver.storage.googleapis.com/130.0.6723.58/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo cp ./chromedriver-linux64/chromedriver /usr/bin/chromedriver

#安装PhantomJS
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2

# 设置环境变量OPENSSL_CONF来禁用OpenSSL 3的配置加载
export OPENSSL_CONF=/etc/ssl/

# 访问mysql数据库
docker exec -it mysql mysql -uroot -p

# 安装依赖
pip install -r requirements.txt

# 查看本机ip
hostname -I
```

```sql
# 创建数据库
CREATE DATABASE IF NOT EXISTS house
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

# 修改root 用户密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
```

