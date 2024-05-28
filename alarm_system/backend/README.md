# Flask - MySQL

<br>

## requirements
```bash
pip install flask
pip install pymysql
sudo apt install mysql-server
```

<br>

## Database Setting

1. config.py
  Fall-Prevention-System-Based-on-Deep-Learning/config.py 생성 후 아래 내용 입력

```python
db_config = {
  'user' : [your_user_name],
  'password' : [your_password],
  'db' : [your_database_name],
  'charset' : 'utf8'
}

SECRET_KEY = 'your_secret_key'
```

<br>
2. Database 기본 세팅 ( 최초 1회 실행 )

```python
# mysql 시작 ( wsl 인 경우만 실행 )
sudo service mysql start

# mysql 실행 및 사용자 생성
sudo mysql -u root -p 
# Enter password : (root password 없음, Enter 치면 됨)
mysql > SET GLOBAL validate_password.policy=LOW;
mysql > create user [your_user_name]@localhost identified by '[your_password_name]';
mysql > grant all privileges on *.* to [your_user_name]@localhost;
mysql > exit;
```

<br>
3. 데이터베이스 table 생성 및 샘플 데이터 삽입

```python
sudo mysql -u [your_user_name] -p 
 # Enter password : [your_password_name]
mysql> source alarm_system/backend/sqlfile/create.sql;
mysql> source alarm_system/backend/sqlfile/insert_sample.sql;
mysql> exit;
```

<br>
4. 데이터베이스 초기화

```python
sudo mysql -u [your_user_name] -p
 # Enter password : [your_password_name]
mysql> source alarm_system/backend/sqlfile/delete.sql;
mysql> exit;
```
