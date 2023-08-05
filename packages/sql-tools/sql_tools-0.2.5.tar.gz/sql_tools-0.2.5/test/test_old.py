from sql_tools import sqlite

sqlite.createDatabase("test/test-ok.db")
# sqlite.clearDatabase("test/test-ok.db")
sqlite.connect("test/test-ok.db")
# sqlite.execute("CREATE TABLE IF NOT EXISTS OK (NAME TEXT);", logConsole=True, splitByColumns=True)
# sqlite.execute("INSERT INTO OK VALUES ('YOGESH');", logConsole=True)
# sqlite.execute("INSERT INTO OK VALUES ('PANKAJ');", logConsole=True)
# sqlite.execute("INSERT INTO OK VALUES ('SAKSHI');", logConsole=True)
# print(sqlite.getColumnNames("OK"))
print(sqlite.io.databaseToCSV("ok", databPath=sqlite.constants.__databPath__[0], returnDict=True))
# print(sqlite.getTableNames(databPath="test/test-ok.db"))
