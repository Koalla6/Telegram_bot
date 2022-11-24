import config
import mysql.connector

def russian_channels():
    mydb = mysql.connector.connect(
        host=config.HOST,
        user=config.USER,
        passwd=config.PASSWORD,
        database=config.DATABASE_NAME
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT link_to_connect FROM russian")
    new_list = []
    for ltc in mycursor:
        ltc = str(ltc).replace("('", "")
        new_list.append(ltc.replace("',)", ""))
    return new_list

def ukrainian_channels():
    mydb = mysql.connector.connect(
        host=config.HOST,
        user=config.USER,
        passwd=config.PASSWORD,
        database=config.DATABASE_NAME
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT link_to_connect FROM ukrainian")
    new_list = []
    for ltc in mycursor:
        ltc = str(ltc).replace("('", "")
        new_list.append(ltc.replace("',)", ""))
    return new_list

def ukrainian_channels_r():
    mydb = mysql.connector.connect(
        host=config.HOST,
        user=config.USER,
        passwd=config.PASSWORD,
        database=config.DATABASE_NAME
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT link_to_connect FROM ukrainian_r")
    new_list = []
    for ltc in mycursor:
        ltc = str(ltc).replace("('", "")
        new_list.append(ltc.replace("',)", ""))
    return new_list

def show_russian_channels():
    mydb = mysql.connector.connect(
        host=config.HOST,
        user=config.USER,
        passwd=config.PASSWORD,
        database=config.DATABASE_NAME
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT channel_name, link FROM russian")
    new_list = []
    for srl in mycursor:
        srl = str(srl).replace("('", "")
        srl = str(srl).replace("', '", " - ")
        new_list.append(srl.replace("')", ""))
    return new_list

def show_ukrainian_channels():
    mydb = mysql.connector.connect(
        host=config.HOST,
        user=config.USER,
        passwd=config.PASSWORD,
        database=config.DATABASE_NAME
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT channel_name, link FROM ukrainian")
    new_list = []
    for srl in mycursor:
        srl = str(srl).replace("('", "")
        srl = str(srl).replace("', '", " - ")
        new_list.append(srl.replace("')", ""))
    mycursor.execute("SELECT channel_name, link FROM ukrainian_r")
    for srl in mycursor:
        srl = str(srl).replace("('", "")
        srl = str(srl).replace("', '", " - ")
        new_list.append(srl.replace("')", ""))
    return new_list

# result = new_list[0].replace("(", "")
#     # new_list2.append(result)
# print(result)

# new_list2 = []
# for i in range(len(new_list)):
#     result = new_list[0].replace("(", "")
#     # new_list2.append(result)
#     print(result)



# mydb = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         passwd='root',
#         database='channels'
#     )
# mycursor = mydb.cursor()
# mycursor.execute("SELECT link_to_connect FROM russian")
# new_list = []
# for ltc in mycursor:
#     ltc = str(ltc).replace("('", "")
#     new_list.append(ltc.replace("',)", ""))
# for i in new_list:
#     print(i)
