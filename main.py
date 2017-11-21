# -*- coding: utf-8 -*-

from collections import OrderedDict
from pyexcel_xlsx import get_data
from pyexcel_xlsx import save_data
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
# database
DB_USER_NAME = 'xulei2'
DB_PASSWORD = '2048'
URI = 'localhost'
DATABASE = 'myBasketball'
URL = ''.join(['postgresql://', DB_USER_NAME, ':', DB_PASSWORD, '@', URI, '/', DATABASE])
app.config['SQLALCHEMY_DATABASE_URI']= URL
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)



class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.INTEGER(),nullable=False,primary_key=True)
    name = db.Column(db.String(64))
    stu_number = db.Column(db.String(64))
    identify_number = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' % self.name


def readDataFile(file):
    db.create_all()
    excel = get_data(file)
    print "get data type:",type(excel)
    for sheet in excel.keys():
        stuList = excel[sheet]
        #去除第一行的中文
        del stuList[0]
        for row in stuList:


            #使用json模块将原列表格式转换成json字符串输出,并设置编码格式
            # row = json.dumps(row,ensure_ascii=False,encoding="utf-8")
            # print  row,'-',len(row),'-',type(row)
            tmpData = Student(name=transToUTF(row[1]),stu_number=transToUTF(row[2]),identify_number=row[3])

            # tmpData = Student(id=row[0],name=row[1],stu_number=row[2],identify_number=row[3])
            db.session.add(tmpData)
            db.session.commit()

def transToUTF(str):
    return json.dumps(str,ensure_ascii=False,encoding="utf-8")

def delDataFile():
    users = Student.query.all()
    for u in users:
        db.session.delete(u)
    db.session.commit()

def findUserByID(id):
    user = Student.query.filter_by(id = id).all()
    print user






#
# if __name__ == '__main__':
#     read_xlsx_file("/Users/xulei2/Desktop/cs14.xlsx")

if __name__ == '__main__':

    readDataFile('/Users/xulei2/Desktop/cs14.xlsx')
    # delDataFile()
    # findUserByID("140")
