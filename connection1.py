
import pymysql

host="very.long.endpoint.definition.amazonaws.com"
port=3306
dbname="arrzi"
user="admin"
password="adminmysql"

conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)