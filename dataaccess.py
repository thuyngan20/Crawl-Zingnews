import collections
from typing import List
from pymongo import MongoClient
from pymongo.database import Database
from datetime import datetime



class DataAccess():
    def __init__(self, MONGO_URI: str, MONGO_DB: str):
        '''
            maxIdleTimeMS (tùy chọn): Số mili giây tối đa mà kết nối có thể duy trì ở trạng thái 
                không hoạt động trong nhóm trước khi bị xóa và thay thế. Mặc định là Không (không giới hạn).

            socketTimeoutMS: (số nguyên hoặc Không có) Kiểm soát thời gian (tính bằng mili giây) 
                trình điều khiển sẽ đợi phản hồi sau khi gửi hoạt động cơ sở dữ liệu thông thường (không giám sát) 
                trước khi kết luận rằng đã xảy ra lỗi mạng. 0 hoặc Không có nghĩa là không có thời gian chờ.
                Mặc định là Không (không có thời gian chờ)
        '''
        self.mongo_uri = MONGO_URI
        self.mongo_db = MONGO_DB
        self.client: MongoClient = MongoClient(self.mongo_uri,
                                               maxIdleTimeMS=30000,
                                               socketTimeoutMS=60000
                                               )
        self.db = self.client[self.mongo_db]

    def connect_db(self) -> Database:
        """ connect MongoDB """
        self.client = MongoClient(self.mongo_uri,
                                  maxIdleTimeMS=30000,
                                  socketTimeoutMS=60000
                                  )
        self.db = self.client[self.mongo_db]

    def disconnect_db(self) -> bool:
        ''' discount MongoDB'''
        try:
            self.client.close()
            return True
        except Exception as exc:
            print("Error in disconnect db: %s" % str(exc))
        return False
        
    def get_info(self):
        """ get category info """
        try:
            if self.db is None:
                self.db = self.connect_db()
            projection = {'_id':0, 'content':1, 'link': 1}
            collection = self.db['zing']
            results  = collection.find({}, projection)
            return list(results)
        except Exception as exc:
            print(f"data_access.get_category_info: {exc}")
            return None
        
    def get_item(self, content):
        """ get category info """
        try:
            if self.db is None:
                self.db = self.connect_db()
            projection = {'_id':0, 'content':1, 'link': 1}
            collection = self.db['zing']
            results  = collection.find({"content": content}, projection)
            return list(results)
        except Exception as exc:
            print(f"data_access.get_category_info: {exc}")
            return None
        
    def update_link(self, content: str, link: str):
        """ update status """
        try:
            if self.db is None:
                self.db = self.connect_db()
            myquery = { "content": content }
            newvalues = { "$set": { "link": link } }
            collection = self.db['zing']
            collection.update_one(myquery, newvalues)
            return True
        except Exception as exc:
            print(f"data_access.update_category_info: {exc}")
            return False
        
    def insert_content(self,content: str):
        try:
            if self.db is None:
                self.db = self.connect_db()
            mylist = {"content":content}
            collection = self.db['zing']
            collection.insert_one(mylist)
            return True
        except Exception as exc:
            print(f"data_access.update_category_info: {exc}")
            return False
    
    def get_link(self):
        try:
            if self.db is None:
                self.db = self.connect_db()
            projection = {'link':1}
            collection = self.db['zing']
            results = collection.find({},projection)
            return list(results)
        except Exception as exc:
            print(f"data_access.get_category_info: {exc}")
            return None
    def update_body(self, link: str, title: str, body: str):
        """ update title and body of links """
        try:
            if self.db is None:
                self.db = self.connect_db()
            myquery = { "link": link }
            newvalues = { "$set": { "title": title, "body": body } }
            collection = self.db['zing']
            collection.update_one(myquery, newvalues)
            return True
        except Exception as exc:
            print(f"data_access.update_category_info: {exc}")
            return False
            