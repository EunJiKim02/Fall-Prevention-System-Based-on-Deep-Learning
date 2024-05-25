import pymysql
from config import db_config

# database object
class Mysqldb:
    def __init__(self):
        self.conn = pymysql.connect(**db_config)
        self.cursor = self.conn.cursor()

    # --------- 기본 database 함수 -----------
    
    # select 관련 함수들

    def select1(self, query): # 단일 선택
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def select(self, query, size): # size 개수만큼 row 선택
        self.cursor.execute(query)
        return self.cursor.fetchmany(size)
    
    def selectall(self, query): # 모든 정보 선택
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # --------------------------------------


    # --------- manager 관련 함수 -----------

    # manager signup ( = insert s)
    # info = ('email', 'password', 'name')
    def signup(self, info): 
        def isiddup(email): # duplicate check
            query = f"SELECT COUNT(*) FROM MANAGER WHERE email ='{email}'"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result[0] == 0
    
        def insert(info): #signup
            try:
                self.conn.begin() 
                query = f"INSERT INTO MANAGER VALUES( 0, '{info[0]}','{info[1]}', '{info[2]}')"
                self.cursor.execute(query)
                self.conn.commit() 
                return True
            except Exception as e: #transaction rollback
                self.conn.rollback()
                print(f"Error during insert: {e}")
                return False
            
        if isiddup(info[0]):
            return insert(info)
        else:
            print('duplicate id')    
        return False


    # manager get info
    def get_manager_info(self, email):
        query = f"SELECT * FROM MANAGER WHERE email = '{email}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result
    
    # signin
    def authenticate_manager(self, email, pw):
        query = f"SELECT count(*) FROM MANAGER WHERE email ='{email}' AND password='{pw}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] > 0

    
