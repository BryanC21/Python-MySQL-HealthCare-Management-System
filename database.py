"""
This file is a portable API to be used by python programs that must connect to any database system
"""
import pymysql
import configparser


class DB:

    # SQL Operations
    DROP_DATABASE = 0
    DROP_TABLE = 1
    CREATE_DATABASE = 2
    CREATE_TABLE = 3
    INSERT = 4
    SELECT = 5
    UPDATE = 6
    DELETE = 7
    RUN_SCRIPT = 8

    # Most common default queries
    DROP_DATABASE_QUERY = """DROP DATABASE IF EXISTS """
    DROP_TABLE_QUERY = """DROP TABLE IF EXISTS """
    CREATE_DATABASE_QUERY = """CREATE DATABASE IF NOT EXISTS """

    def __init__(self, host=None, username=None, password=None, database=None, config_file=None, dbms="mysql"):
        """
        Class constractor
        :param host:
        :param username:
        :param password:
        :param database:
        """
        self._host = host
        self._username = username
        self._password = password
        self._database = database
        self._run_transaction = None
        if config_file:
            self.get_mysql_credentials(config_file, dbms)

    def get_mysql_credentials(self, configfile, dbms):
        """
        Retrieve credentials from configuration file
        :param configfile: path to
        :param dbms: default is mysql
        :return: VOID
        """
        try:
            if configfile:
                config = configparser.ConfigParser()
                config.read(configfile)
                self._host = config[dbms]['host']
                self._username = config[dbms]['username']
                self._password = config[dbms]['password']
                self._database = config[dbms]['database']
                self._run_transaction = config[dbms]['transactions']
        except:
            print("Error: couldn't read config file")

    def connect(self, database=None):
        """
        Connect to a existing database
        :param database: name
        :return: the connection handler
        """
        try:
            if database: # if is not Null
                self._database = database
            connection = pymysql.connect(self._host, self._username, self._password, self._database)
            return connection
        except pymysql.InternalError as error:
            print(error.args[1])

    def _drop(self, connection, query):
        """
        Helper function that with base implementation for drop database and drop table functions
        :param connection: database connection
        :param query:
        :return: True if the drop is successful. Otherwise, print the error.
        """
        try:
            connection.cursor().execute(query)
            connection.commit()
            return True
        except pymysql.InternalError as error:
            print(error.args[1])

    def drop_database(self, database=None):
        """
        Drops an existing database.
        Note that if the database is not in the system it will thrown a warning
        :param database: database name
        :return: True if the drop is successful. Otherwise, print the error.
        """
        connection = pymysql.connect(self._host, self._username, self._password)
        if database: # database if not null
            self._database = database
        query = self.DROP_DATABASE_QUERY + self._database # see self.DROP_DATABASE_QUERY at the beginning of the class
        return self._drop(connection, query)

    def drop_table(self, table):
        """
        Drops a table.
        :param table: cannot be None
        :return: True if the drop is successful. Otherwise, print the error.
        """
        connection = self.connect()
        query = self.DROP_TABLE_QUERY + table
        return self._drop(connection, query)

    def create_database(self, database=None, drop_database_first=True):
        """
        Database creation
        :param database:
        :param drop_database_first: drops table
        :return: True if the drop is successful. Otherwise, print the error.
        """
        connection = pymysql.connect(self._host, self._username, self._password)
        try:
          if not database:
              database = self._database
          if drop_database_first: # will drop the database if exists
              self.drop_database(database)
          query = self.CREATE_DATABASE_QUERY + database
          connection.cursor().execute(query)
          connection.commit() # permanent save to thendatabase
          connection.select_db(database)
          return True
        except pymysql.InternalError as error:
            print(error.args[1])

    def _execute_query(self, query, values, action=None):
        """
        Helper method to split responsibilities for create, insert, delete, select and update
        :param query: The sql query. if values, then it must be in this form:
                      "INSERT INTO X WHERE y=%s"
        :param values: If set, avoid sql injections. When more than one value it can be passed as a primitive type.
                       However, when there are more than 1 values they must be pass as tuple:
                       tuple = (value1, value2.....value_n)
        :param action: the context of the query
        :return: True if the query is successful. Return results if the query is SELECT. Otherwise, print the error
        """
        connection = self.connect()
        try:
           cursor = connection.cursor()
           if values:
               cursor.execute(query, values) # query will have wildcards as values
           else:
               cursor.execute(query)
           connection.commit() # important
           if action == self.SELECT:
               return cursor.fetchall()
           return True
        except pymysql.InternalError as error:
            print(error.args[1])


    def get_queries_from(self, sql_file, delimiter=";"):
        """
        Read queries from a sql file
        :param sql_file:
        :param delimiter: default is semicolon
        :return: a list of queries
        """
        with open(sql_file, "r") as file:
            # Split by delimiter
            queries = file.read().split(delimiter)
            # pop the empty line at the end of the file
            queries.pop()
        return queries

    def run_sql_file(self, sqlfile):
        """
        Execute queries from sqlfile
        Note that you must create the database with the method create_database()
        :param sqlfile: sql file
        :return: VOID
        """
        try:
           queries = self.get_queries_from(sqlfile)
           queries_executed = 0
           for query in queries:
               if self._execute_query(query, values=None): # execute each query
                   queries_executed += 1
           print("{} Executed queries from {}".format(queries_executed, sqlfile))
        except pymysql.InternalError as error:
            print(error.args[1])

    def create_table(self, query, values=None):
        return self._execute_query(query, values, action=self.CREATE_TABLE)

    def insert(self, query=None, table=None, attributes=None, values=None):
        if not query:
            wildcards = self.wildcars(len(values))
            attributes_to_str = ", ".join(attributes)
            query = """INSERT INTO {} ( {} ) VALUES ( {} )""".format(table, attributes_to_str, wildcards)

            #save to transaction
            file = open("transactions.sql", "a")
            temp2 = tuple(values)
            if(len(values) == 1):
                temp2 = "(\"{}\")".format(values[0])
            temp = """INSERT INTO {} ( {} ) VALUES {} """.format(table, attributes_to_str, temp2)
            file.write("\n{};\n".format(temp))
            file.close

            values = [x.strip(' ') for x in values]
            values = tuple(values)
        return self._execute_query(query, values, action=self.INSERT)

    def update(self, query, values=None):
        return self._execute_query(query, values, action=self.UPDATE)

    def delete(self, query, values=None):
        return self._execute_query(query, values, action=self.DELETE)

    def select(self, query, values=None):
        rows = self._execute_query(query, values, action=self.SELECT)
        return rows

    def get_table_names(self):
        query = """SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE 
                   TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA=%s"""
        tables = self.select(query, self._database)
        return tables

    def get_column_names(self, table):
        query = """SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE 
                   TABLE_SCHEMA = %s AND TABLE_NAME = %s"""
        values = (self._database, table)
        columns = self.select(query, values)
        return columns

    def wildcars(self, num_wildcards):
        list_wildcards = []
        for i in range(num_wildcards):
            list_wildcards.append('%s')
        return ", ".join(list_wildcards)