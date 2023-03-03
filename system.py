# -*- coding: utf-8 -*-
"""
Created on Sat May 30 20:17:39 2020

@author: qingming
"""

from flask import request
from datetime import datetime
from flask import Flask
from flask import send_file
import pyodbc
import numpy as np
import io
import  matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Response

app = Flask(__name__)

server = 'localhost'
database = 'Bank1'#数据库名
username = 'sa'#用户名
password = 'rootroot'#密码
#连接数据库
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password +';CHARSET=GBK')
cursor = cnxn.cursor()
#初始页面

@app.route("/")
def homepage():
    return send_file("homepage.html")

@app.route("/open_account_input")
def open_account_input():
    return send_file("open_account.html")

@app.route("/handle_the_business")
def handle_the_business():
    return send_file("handle_the_business.html")


@app.route("/create_new_user_input")
def create_new_user_input():
    return send_file("create_new_user.html")

@app.route("/account_transfer_input")
def account_transfer_input():
    return send_file("account_transfer.html")

@app.route("/balance_inquiry_input")
def balance_inquiry_input():
    return send_file("balance_inquiry.html")

@app.route("/destroy_account_input")
def destroy_account_input():
    return send_file("destroy_account.html")

@app.route("/draw_money_input")
def draw_money_input():
    return send_file("draw_money.html")

@app.route("/save_money_input")
def save_money_input():
    return send_file("save_money.html")

@app.route("/administrator")
def administrator():
    return send_file("administrator.html")

@app.route('/general_information')
def general_information():
    tsql="""select user_ID_number,count(account_number),sum(balance)
        from accountlist
        group by user_ID_number"""
    s='<div align="center" style="font-size:30px;position:relative;top:150px">'
    s=s+"the general information is as follows:"
    s = s+'<table border="1">'+'<tr>'
    s = s+'<th>ID number</th>'+'<th>account amont</th>'+'<th>total balance</th>'
    with cursor.execute(tsql):
        row = cursor.fetchone()
        while row:
            s = s + "<tr>"
            s = s + "<td>" + str(row[0]) + "</td>"
            s = s + "<td>" + str(row[1]) + "</td>"
            s = s + "<td>" + str(row[2]) + "</td>"
            row = cursor.fetchone()
            s = s +  "</tr><br/><br/>"
    s = s + "</table>"
    tsql="""select sum(balance) from accountlist;"""
    cursor.execute(tsql)
    total_money=cursor.fetchone()[0]
    s=s+"the total money in the bank is "+str(total_money)+'<br/>'
    s=s+'<a href="http://127.0.0.1:5000/general_information_plot" title="Plot" target="_self">the plot</a><br/>'
    s=s+'<a href="http://127.0.0.1:5000/administrator" title="Plot" target="_self">go back</a><br/>'
    s = "</div> <html><body>" + s + "</body></html>"
    return s

@app.route('/general_information_plot')
def general_information_plot():
    tsql="""select user_ID_number,count(account_number),sum(balance)
        from accountlist
        group by user_ID_number"""
    ID_list=[]
    balance_list=[]
    with cursor.execute(tsql):
        row = cursor.fetchone()
        while row:
            ID_list.append(row[0])
            balance_list.append(row[2])
            row = cursor.fetchone()
    
    myfont = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    objects = ID_list
    xx_pos = np.arange(len(objects))
    performance = balance_list
    axis.bar(xx_pos, performance, align='center', alpha=0.5)
    axis.set_xticks(np.arange(len(ID_list)))
    axis.set_xticklabels(ID_list, fontproperties = myfont)
    axis.set_ylabel('balance')
    axis.set_title('total balance and ID of users')

    output = io.BytesIO()
    FigureCanvas(fig).print_jpg(output)
    return Response(output.getvalue(), mimetype='image/png')
    
#开户
@app.route('/open_account', methods = ['POST'])
def open_account():
    account_number= request.form['account_number']
    cancelflag='否'
    balance= request.form['balance']
    user_ID_number= request.form['user_ID_number']
    trade_time=datetime.now()

    tsql = "insert into accountlist values("
    tsql=tsql+"'"+account_number+"',"
    tsql=tsql+"'"+cancelflag+"',"
    tsql=tsql+balance+","
    tsql=tsql+"'"+user_ID_number+"');\n"
    tsql=tsql+"insert into trading_record values("
    tsql=tsql+"'"+account_number+"',"
    tsql=tsql+"'"+account_number+"',"
    tsql=tsql+"'"+str(trade_time)[:-3]+"',"
    tsql=tsql+"'"+"开户"+"',"
    tsql=tsql+balance+","
    tsql=tsql+"0"+","
    tsql=tsql+balance+");\n"
    with cursor.execute(tsql):
        s='<div align="center" style="font-size:30px;position:relative;top:150px">'
        s=s+"open successfully!<br/>"
    tsql="""select distinct account_number,balance,trade_time
            from accountlist,trading_record
            where accountlist.user_ID_number="""
    tsql=tsql+user_ID_number+ """and accountlist.account_number=trading_record.own_account_number
			and trading_record.trade_type='开户'
			order by trade_time"""
    with cursor.execute(tsql):
        s=s+'your account information is as follows:<br/>'
        s =s+ '<table border="1">'+'<tr>'
        s = s+'<th>account number</th>'+'<th>balance</th>'+'<th>open time</th>'+'</tr>'
        row = cursor.fetchone()
        while row:
            s = s + "<tr>"
            s = s + "<td>" + str(row[0]) + "</td>"
            s = s + "<td>" + str(row[1]) + "</td>"
            s = s + "<td>" + str(row[2]) + "</td>"
            row = cursor.fetchone()
            s = s +  "</tr>"
        s = s + "</table>"
        s=s+'<a href="http://127.0.0.1:5000/handle_the_business" title="click here to handle the business" target="_self">handle other business</a><br />'
        s = "</div> <html><body>" + s + "</body></html>"
    return s


#创建新用户
@app.route('/create_new_user', methods = ['POST'])
def create_new_user():
    name= request.form['name']
    gender= request.form['gender']
    birthday= request.form['birthday']
    ID_number= request.form['ID_number']
    tel_number= request.form['tel_number']
    email= request.form['email']
    address= request.form['address']

    tsql = "insert into userlist values("
    tsql=tsql+"'"+name+"',"
    tsql=tsql+"'"+gender+"',"
    tsql=tsql+"'"+birthday+"',"
    tsql=tsql+"'"+ID_number+"',"
    tsql=tsql+"'"+tel_number+"',"
    tsql=tsql+"'"+email+"',"
    tsql=tsql+"'"+address+"');"
    with cursor.execute(tsql):
        s='<div align="center" style="font-size:30px;position:relative;top:150px">'
        s=s+'create successfully!<br/>'
        s=s+'<a href="http://127.0.0.1:5000/handle_the_business" title="click here to handle the business" target="_self">handle other business</a><br />'
        s = "</div><html><body>" + s + "</body></html>"
    return s
#转账
@app.route('/account_transfer', methods = ['POST'])
def account_transfer():
    my_account_number= request.form['my_account_number']
    opposite_account_number= request.form['opposite_account_number']
    trans_amount= request.form['trans_amount']
    trade_time=datetime.now()
    
    tsql="select cancelflag from accountlist where account_number="+my_account_number
    tsql=tsql+" or account_number="+opposite_account_number
    cursor.execute(tsql);
    if cursor.fetchone()[0]=='否' and cursor.fetchone()[0]=='否':
        tsql="select accountlist.balance from accountlist where accountlist.account_number="+my_account_number
        cursor.execute(tsql)
        my_balance_before=float(cursor.fetchone()[0])#查询当前余额
        tsql="select accountlist.balance from accountlist where accountlist.account_number="+opposite_account_number
        cursor.execute(tsql);
        opposite_balance_before=float(cursor.fetchone()[0])
        if my_balance_before>=float(trans_amount):#有足够的钱转账
            tsql="update accountlist set balance =balance-"
            tsql=tsql+trans_amount
            tsql=tsql+" where account_number="+my_account_number+";\n"
            tsql=tsql+"update accountlist set balance =balance+"
            tsql=tsql+trans_amount
            tsql=tsql+" where account_number="+opposite_account_number+";\n"#更新账户数据
            
            tsql=tsql+"insert into trading_record values("
            tsql=tsql+"'"+my_account_number+"',"
            tsql=tsql+"'"+opposite_account_number+"',"
            tsql=tsql+"'"+str(trade_time)[:-3]+"',"
            tsql=tsql+"'"+"转账"+"',"
            tsql=tsql+trans_amount+","
            tsql=tsql+str(my_balance_before)+","
            tsql=tsql+str(my_balance_before-float(trans_amount))+");\n" 
            tsql=tsql+"insert into trading_record values("
            tsql=tsql+"'"+opposite_account_number+"',"
            tsql=tsql+"'"+my_account_number+"',"
            tsql=tsql+"'"+str(trade_time)[:-3]+"',"
            tsql=tsql+"'"+"转账"+"',"
            tsql=tsql+trans_amount+","
            tsql=tsql+str(opposite_balance_before)+","
            tsql=tsql+str(opposite_balance_before+float(trans_amount))+");"#更新交易记录 
            with cursor.execute(tsql):
                s='<div align="center" style="font-size:30px;position:relative;top:150px">'
                s=s+'transfer successfully!<br/>'
                s=s+'your balance now is '
                s=s+str(my_balance_before-float(trans_amount))+'!'
        else:
             s='<div align="center" style="font-size:30px;position:relative;top:150px">'
             s="sorry, your balance is insufficient!<br/>" 
             s=s+'there is only '+str(my_balance_before)+'in your account<br/>'
    else:
        s='<div align="center" style="font-size:30px;position:relative;top:150px">'
        s=s+'sorry, your account or opposite account has been destroyed, please input again!<br/>'
    s=s+'<a href="http://127.0.0.1:5000/handle_the_business" title="click here to handle the business" target="_self">handle other business</a><br />'
    s = "</div><html><body>" + s + "</body></html>"
    return s
#查询余额
@app.route('/balance_inquiry', methods = ['POST'])
def record_inquiry():
    my_account_number = request.form['my_account_number']
    tsql="select cancelflag from accountlist where account_number="+my_account_number
    cursor.execute(tsql)
    if cursor.fetchone()[0]=='否':
        tsql = """select * from trading_record
    			where own_account_number='"""
        tsql = tsql+my_account_number
        tsql = tsql +"'\n"
        tsql=tsql+'order by trade_time'
        s='<div align="center" style="font-size:30px;position:relative;top:150px">'
        s=s+"your trading_record are as follows:<br/>"
        s = s+'<table border="1">'+'<tr>'
        s = s+'<th>my account number</th>'+'<th>opposite account number</th>'+'<th>trade time</th>'
        s=s+'<th>trade type</th>'+'<th>amont</th>'+'<th>blance before</th>'+'<th>blance after</th>'+'</tr>'
        with cursor.execute(tsql):
            row = cursor.fetchone()
            while row:
                s = s + "<tr>"
                s = s + "<td>" + str(row[0]) + "</td>"
                s = s + "<td>" + str(row[1]) + "</td>"
                s = s + "<td>" + str(row[2]) + "</td>"
                s = s + "<td>" + str(row[3]) + "</td>"
                s = s + "<td>" + str(row[4]) + "</td>"
                s = s + "<td>" + str(row[5]) + "</td>"
                s = s + "<td>" + str(row[6]) + "</td>"
                row = cursor.fetchone()
                s = s +  "</tr>"
        s = s + "</table>"
    else:
        s='<div align="center" style="font-size:30px;position:relative;top:150px">'
        s=s+'sorry, your account has been destroyed, please input again!<br/>'
    s=s+'<a href="http://127.0.0.1:5000/handle_the_business" title="click here to handle the business" target="_self">handle other business</a><br/>'
    s = "</div><html><body>" + s + "</body></html>"
    return s
#取钱
@app.route('/draw_money', methods = ['POST'])
def draw_money():
    account_number= request.form['account_number']
    draw_amount= request.form['draw_amount']
    trade_time=datetime.now()
    tsql="select cancelflag from accountlist where account_number="+account_number
    cursor.execute(tsql)
    if cursor.fetchone()[0]=='否':

        tsql="select accountlist.balance from accountlist where accountlist.account_number="+account_number+";\n"
        cursor.execute(tsql);
        balance_before=float(cursor.fetchone()[0])#查询当前余额
        if(balance_before>=float(draw_amount)):
            tsql="update accountlist set balance =balance-"
            tsql=tsql+draw_amount
            tsql=tsql+" where account_number="+account_number+";\n"#更新账户数据
            
            tsql=tsql+"insert into trading_record values("
            tsql=tsql+"'"+account_number+"',"
            tsql=tsql+"'"+account_number+"',"
            tsql=tsql+"'"+str(trade_time)[:-3]+"',"
            tsql=tsql+"'"+"取款"+"',"
            tsql=tsql+draw_amount+","
            tsql=tsql+str(balance_before)+","
            tsql=tsql+str(balance_before-float(draw_amount))+");"#更新交易记录    
            with cursor.execute(tsql):
                s='<div align="center" style="font-size:30px;position:relative;top:150px">'
                s=s+'draw successfully!'
                s=s+'your balance before is '
                s=s+str(balance_before)+'!<br/>'
                s=s+'and your balance now is '
                s=s+str(balance_before-float(draw_amount))+'!'
                s = "</div><html><body>" + s + "</body></html>"
                
        else:
            s='<div align="center" style="font-size:30px;position:relative;top:150px">'
            s=s+"sorry, your balance is insufficient!"   
            s=s+'there is only '+str(balance_before)+'in your account<br/>'
    else:
        s='<div align="center" style="font-size:30px;position:relative;top:150px">'
        s=s+'sorry, your account has been destroyed, please input again!<br/>'
    s=s+'<a href="http://127.0.0.1:5000/handle_the_business" title="click here to handle the business" target="_self">handle other business</a><br />'
    s = "</div><html><body>" + s + "</body></html>"
    return s
#存钱
@app.route('/save_money', methods = ['POST'])
def save_money():
    account_number= request.form['account_number']
    save_amount= request.form['save_amount']
    trade_time=datetime.now()
    tsql="select cancelflag from accountlist where account_number="+account_number
    cursor.execute(tsql)
    if cursor.fetchone()[0]=='否':
        tsql="select accountlist.balance from accountlist where accountlist.account_number="+account_number+";\n"
        cursor.execute(tsql);
        balance_before=float(cursor.fetchone()[0])#查询当前余额
        
        tsql="update accountlist set balance =balance+"
        tsql=tsql+save_amount
        tsql=tsql+" where account_number="+account_number+";\n"#更新存款
        
        tsql=tsql+"insert into trading_record values("
        tsql=tsql+"'"+account_number+"',"
        tsql=tsql+"'"+account_number+"',"
        tsql=tsql+"'"+str(trade_time)[:-3]+"',"
        tsql=tsql+"'"+"存款"+"',"
        tsql=tsql+save_amount+","
        tsql=tsql+str(balance_before)+","
        tsql=tsql+str(balance_before+float(save_amount))+");"
        
        with cursor.execute(tsql):
            s='<div align="center" style="font-size:30px;position:relative;top:150px">'
            s=s+'save successfully!<br/>'
            s=s+'your balance before is '
            s=s+str(balance_before)+'!<br/>'
            s=s+'and your balance now is '
            s=s+str(balance_before+float(save_amount))+'!'
            s = "</div><html><body>" + s + "</body></html>"
    else:
        s='<div align="center" style="font-size:30px;position:relative;top:150px">'
        s=s+'sorry, your account has been destroyed, please input again!<br/>'
    s=s+'<a href="http://127.0.0.1:5000/handle_the_business" title="click here to handle the business" target="_self">handle other business</a><br />'
    s = "</div><html><body>" + s + "</body></html>"
    return s
#销户
@app.route('/destroy_account', methods = ['POST'])
def destroy_account():
    account_number= request.form['account_number']
    tsql="select cancelflag from accountlist where account_number="+account_number
    cursor.execute(tsql)
    if cursor.fetchone()[0]=='否':
        tsql="update accountlist set cancelflag ='是'"
        tsql=tsql+" where account_number="+account_number+";\n"
     
        with cursor.execute(tsql):
            s='<div align="center" style="font-size:30px;position:relative;top:150px">'
            s=s+'destroy successfully!'
            s = "<html><body>" + s + "</body></html>"
    else:
        s='<div align="center" style="font-size:30px;position:relative;top:150px">'
        s=s+'sorry, your account has been destroyed already!<br/>'
    s=s+'<a href="http://127.0.0.1:5000/handle_the_business" title="click here to handle the business" target="_self">handle other business</a><br />'
    s = "</div><html><body>" + s + "</body></html>"
    return s

if __name__ == "__main__":
    app.run()