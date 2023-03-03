1.	编译环境
（1）	anaconda spyder python 3.7
（2）	SQL Server Management Studio 15.0

2.	运行方法
（1）	运行seed_data.sql,建立数据库并插入数据;
（2）	运行system.py,返回网址http://127.0.0.1:5000/
（3）	在网页上进行增删改查等操作。

3.	简要使用说明
	打开网址http://127.0.0.1:5000/，在homepage页面选择作为普通用户或者系统管理员登录（seed_data中已插入ID为000000000000000001和000000000000000002的用户,对应账户分别为000001和000002、000022），对已有账户进行操作或创建新用户。
	详细功能见设计文档。
	注意：若要使用新的account number和ID number，必须先进行创建新用户和开户操作。

4.	文件目录
（1）	account_transfer.html
（2）	administrator.html
（3）	balance_inquiry.html
（4）	create_new_user.html
（5）	destroy_account.html
（6）	draw_money.html
（7）	handle_the_business.html
（8）	homepage.html
（9）	open_account.html
（10）	save_money.html
（11）	seed_data.sql
（12）	system.py
