/*************************************
创建数据库
*****************************************/
create database Bank1
/**************************************
创建表
**************************************/

--创建用户表
create table userlist(
	name char(10) not null,--姓名
	gender char(2),--性别
	birthday date,--生日
	ID_number char(18),--身份证号码
	tel_number char(11),--电话号
	email char(20),--邮箱
	address char(30),--地址
	primary key(ID_number))
--创建账户表
create table accountlist(
	account_number char(6),--账号
	cancelflag char(2) check(cancelflag in ('是','否')),--销户标记
	balance float,--余额
	user_ID_number char(18),--储户身份证号码
	primary key(account_number))
--创建交易历史记录表
create table trading_record(
	own_account_number char(6),--账号
	opposite_account_number char(6),--对方账号
	trade_time datetime,--交易时间
	trade_type char(4) check(trade_type in('存款','取款','转账','开户','计息')),
	--交易时间
	amount float,--交易金额
	balance_before float,--交易之前的余额
	balance_after float check(balance_after>=0),--交易后的余额
	primary key(own_account_number,trade_time))
--创建计息历史表
create table interest_history(
	account_number char(6),--账号
	date_last date,--上次计息日
	date_new date,--本次计息日
	interest_amount float,--计息金额
	primary key(account_number,date_new))
/******************************
插入数据
******************************/

insert into userlist values('张一','男','2000-01-03','000000000000000001','00000000001','000001@163.com','上海市南京路');
insert into accountlist values('000001','否',0,'000000000000000001');
insert into trading_record values('000001','000001','2020-01-01 00:00:00','开户',0,0,0)

insert into userlist values('王二','男','1987-12-22','000000000000000002','00000000002','000002@163.com','南京市上海路');
insert into accountlist values('000002','否',3000,'000000000000000002');
insert into accountlist values('000022','否',5000,'000000000000000002');
insert into trading_record values('000002','000002','2013-04-01 00:00:00','开户',3000,0,3000)
insert into trading_record values('000022','000022','2013-04-01 00:00:00','开户',5000,0,5000)


