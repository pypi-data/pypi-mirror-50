from sql_tools import sqlite

sqlite.connect("test/ok.sqlite")
sqlite.createDatabase()
# sqlite.execute("CREATE TABLE STUDENT(NAME TEXT);", commit=False)
sqlite.execute("INSERT INTO STUDENT VALUES('YOGESH')")
sqlite.execute("INSERT INTO STUDENT VALUES('SANDESH')")

print(sqlite.io.tableToCSV("STUDENT", index=False))
