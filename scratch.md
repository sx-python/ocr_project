### 介绍
ocr图片识别，筛选带字母的图片

### 部署
* 创建数据库
  ```

    create database User charset=utf8;
    create database ImageData charset=utf8;
  ```

* 创建虚拟环境
  ```shell
    mkvirtualenv -p python3 ocr_vir
    cd /home/python/Desktop/ocr_project
    pip install -r requirements.txt
  ```

* 迁移数据库-使用模型类生成表
  ```shell
  # 初始化
    python main.py db init
  # 生成迁移脚本
    python main.py db migrate
  # 执行迁移脚本
    python main.py db upgrade
  ```

 * 执行代码
 ```
    python main.py runserver -h 192.168.192.130 -p 5000
   ```
 * 查看所有路由
```
  http://192.168.192.130:5000/
  ```
* 测试


