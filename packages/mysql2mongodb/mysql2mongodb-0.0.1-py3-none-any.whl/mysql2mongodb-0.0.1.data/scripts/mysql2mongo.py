from mysql2mongodb.database import DatabaseFactory



db = DatabaseFactory.build('mysql',address="192.168.1.9", user="test", password="Chuckie93@", database_name="mongotest")

print(db.tables())