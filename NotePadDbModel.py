from cx_Oracle import *
from traceback import *

class Db_Model:

    def __init__(self):
        self.file_dict = {}
        self.db_status = True
        self.conn=None
        self.cur=None
        try:
            self.conn=connect("notepad/notepad@127.0.0.1/xe")
            print("Connected successfully to the DB")
            self.cur=self.conn.cursor()
        except DatabaseError:
            self.db_status=False
            print("DB Error:",format_exc)

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.conn.close()
        if self.conn.close():
                self.conn.close()
        print("Disconnected from db")

    def add_file(self, file_name, file_path, file_owner, file_pwd):
        self.file_dict[file_name]=(file_path, file_owner, file_pwd)
        print("File added successfully:",self.file_dict[file_name])

    def get_file_path(self, file_name):
        return self.file_dict[file_name][0]

    def add_file_to_db(self, file_name, file_path, file_owner,file_pwd):
        next_id=1
        self.cur.execute("select max(file_id) from mysecurefiles")
        last_file_id=self.cur.fetchone()[0]
        if last_file_id is not None:
            next_id=last_file_id+1
        self.cur.execute("insert into mysecurefiles values(:1, :2, :3, :4, :5)",(next_id, file_name, file_path, file_owner, file_pwd))
        self.conn.commit()
        return "File added successfully to DB"

    def load_files_from_db(self):
        self.cur.execute("Select file_name, file_path, file_owner, file_pwd from mysecurefiles")
        file_present=False
        for file_name, file_path, file_owner, file_pwd in self.cur:
            self.file_dict[file_name]=(file_path, file_owner, file_pwd)
            file_present=True
        if file_present:
            return "Files populated from db"
        else:
            return 'No files present in your db'

    def remove_file_from_db(self, file_name):
        self.cur.execute(f"delete from mysecurefiles where file_name='{file_name}'")
        count=self.cur.rowcount
        if count==0:
            return "File not present in your DB"
        else:
            self.file_dict.pop(file_name)
            self.conn.commit()
            return "File deleted from your DB"

    def is_secure_file(self, file_name):
        if file_name in self.file_dict:
           return True
        return False

    def is_secure_file_path(self, file_name, file_path):
        if file_name in self.file_dict:
            if file_path == self.file_dict[file_name][0]:
                return True
        return False

    def get_file_pwd(self, file_name):
        return self.file_dict[file_name][2]

    def get_file_count(self):
        return len(self.file_dict)
