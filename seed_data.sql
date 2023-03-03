/*************************************
�������ݿ�
*****************************************/
create database Bank1
/**************************************
������
**************************************/

--�����û���
create table userlist(
	name char(10) not null,--����
	gender char(2),--�Ա�
	birthday date,--����
	ID_number char(18),--���֤����
	tel_number char(11),--�绰��
	email char(20),--����
	address char(30),--��ַ
	primary key(ID_number))
--�����˻���
create table accountlist(
	account_number char(6),--�˺�
	cancelflag char(2) check(cancelflag in ('��','��')),--�������
	balance float,--���
	user_ID_number char(18),--�������֤����
	primary key(account_number))
--����������ʷ��¼��
create table trading_record(
	own_account_number char(6),--�˺�
	opposite_account_number char(6),--�Է��˺�
	trade_time datetime,--����ʱ��
	trade_type char(4) check(trade_type in('���','ȡ��','ת��','����','��Ϣ')),
	--����ʱ��
	amount float,--���׽��
	balance_before float,--����֮ǰ�����
	balance_after float check(balance_after>=0),--���׺�����
	primary key(own_account_number,trade_time))
--������Ϣ��ʷ��
create table interest_history(
	account_number char(6),--�˺�
	date_last date,--�ϴμ�Ϣ��
	date_new date,--���μ�Ϣ��
	interest_amount float,--��Ϣ���
	primary key(account_number,date_new))
/******************************
��������
******************************/

insert into userlist values('��һ','��','2000-01-03','000000000000000001','00000000001','000001@163.com','�Ϻ����Ͼ�·');
insert into accountlist values('000001','��',0,'000000000000000001');
insert into trading_record values('000001','000001','2020-01-01 00:00:00','����',0,0,0)

insert into userlist values('����','��','1987-12-22','000000000000000002','00000000002','000002@163.com','�Ͼ����Ϻ�·');
insert into accountlist values('000002','��',3000,'000000000000000002');
insert into accountlist values('000022','��',5000,'000000000000000002');
insert into trading_record values('000002','000002','2013-04-01 00:00:00','����',3000,0,3000)
insert into trading_record values('000022','000022','2013-04-01 00:00:00','����',5000,0,5000)


