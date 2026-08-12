import os

MYSQL_HOST = os.getenv("MYSQLHOST", "localhost")
MYSQL_USER = os.getenv("MYSQLUSER", "root")
MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD", "")
MYSQL_DB = os.getenv("MYSQLDATABASE", "mineria_choco")
MYSQL_PORT = int(os.getenv("MYSQLPORT", 3306))