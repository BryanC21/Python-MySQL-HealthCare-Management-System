isLoggedIn = False #gives user access to edit tables

def show_menu():
    """
    Prints in console the main menu
    :return: VOID
    """
    print("User Menu \n"
          "1. Create Account \n"
          "2. Login \n"
          "3. Search \n"
          "4. Insert \n"
          "5. Update \n"
          "6. Delete \n"
          "7. Exit \n")


def show_table_names(tables):
    """
    Show all the tables names
    :param tables: a list with the tables names.
                   You can get it by calling the method
                   get_table_names() from DB object
    :return: VOID
    """
    index = 1
    print("\nTables:")
    for table in tables:
        print(table)  # print tables names
        index += 1

#make account
def option1(db_object):
    try:
        # get user input for insert
        email = input("Email: ")
        password = input("Password: ")

        attributes = ['account_id', 'MembershipNumber', 'DateCreated', 'Email', 'Password']
        values = ['4', '675', '2020-12-20', email, password]

        db_object.insert(table="Account", attributes=attributes, values=values)

        print('Account successfully created')
        global isLoggedIn
        isLoggedIn = True

    except: # data was not inserted, then handle error
        print("Error in account insert. Can only make one account in this demo")

#login account
def option2(db_object):
    try:

        email = input("Email: ")
        password = input("Password: ")

        # build queries with the user input
        query = """SELECT * FROM Account WHERE Email = %s AND Password = %s"""

        value = tuple([email, password])

        # get the results from the above query
        rows = db_object.select(query=query, values=value)

        if(rows):
            print('Logged in as, ',email)
            global isLoggedIn
            isLoggedIn = True
        else:
            print('Did not find account.')

    except Exception as err:  # handle error
        print("The account requested couldn't be found\n")

#search
def option3(db_object, tables):
    """
    Search option
    :param db_object: database object
    :param tables: the name of the tables in the database
    :return: VOID
    """
    try:
        # shows that tables names in menu
        show_table_names(tables)

        # get user input
        table_selected = input("\nSelect a table to search: ")
        attribute_selected = input("Search by (i.e name)? ")
        value_selected = input("Enter the value: ")

        columns = db_object.get_column_names(table_selected)  # get columns names for the table selected

        # build queries with the user input
        query = """SELECT * FROM {} WHERE {} = %s""".format(table_selected, attribute_selected)

        if table_selected == "Appointments": 
            print('got into if')
            query = """SELECT Patient.Name, Doctor.Name, Appointments.Location FROM Appointments 
                           JOIN Patient ON user_id = Appointments.Patient
                           JOIN Doctor ON doctor_id = Appointments.Doctor
                           WHERE Appointments.{} = %s""".format(attribute_selected)
            columns = ["Patient", "Doctor", "Address"]

        elif table_selected == "Messages":  
            query = """SELECT Messages.Message, Messages.Subject, Patient.Name, Doctor.Name FROM Messages 
                           JOIN Patient ON user_id = Messages.Patient
                           JOIN Doctor ON doctor_id = Messages.Doctor
                           WHERE Messages.{} = %s""".format(attribute_selected)
            columns = ["Message", "Subject", "Patient", "Doctor"]

        elif table_selected == "HealthRecord":  
            query = """SELECT x.PrimaryDoctorName, y.Name, z.Name, c.Name, c.Comments FROM HealthRecord x
                           JOIN Medication y ON y.HealthRecord = x.record_id
                           JOIN MedicalCondition z ON z.HealthRecord = x.record_id
                           JOIN TestResults c ON c.HealthRecord = x.record_id
                           WHERE x.{} = %s""".format(attribute_selected)
            columns = ["Primary Doctor", "Medications", "Medical Conditions", "Tests", "Test Results"]

        elif table_selected == "Account":
            columns = ["Account id", "Membership Number", "Created", "Email", "Password"]
        
        value = value_selected
        # get the results from the above query
        results = db_object.select(query=query, values=value)
        column_index = 0

        if not all(results):
            print('Not found')
            return

        # print results
        print("\n")
        print(results)
        print("Results from: " + table_selected)
        for column in columns:
            values = []
            for result in results:
                values.append(result[column_index])
            print("{}: {}".format(column, values) ) # print attribute: value
            column_index+= 1
        print("\n")

    except Exception as err:  # handle error
        print("The data requested couldn't be found\n")



# option 4 when user selects insert
def option4(db_object, tables):
    try:
        # show tables names
        show_table_names(tables)

        # get user input for insert
        table = input("\nEnter a table to insert data: ")
        if(table not in tables):
            print("Dont have access to that table.")
            return
        attributes_str = input("Enter the name attribute/s separated by comma? ")
        values_str = input("Enter the values separated by comma: ")

        # from string to list of attributes and values
        if "," in attributes_str:  # multiple attributes
            attributes = attributes_str.split(",")
            values = values_str.split(",")
        else:  # one attribute
            attributes = [attributes_str]
            values = [values_str]

        if db_object.insert(table=table, attributes=attributes, values=values):
            print("Data successfully inserted into {} \n".format(table))

    except: # data was not inserted, then handle error
        print("Error:", values_str, "failed to be inserted in ", table, "\n")


# option 5 when user selects update
def option5(db_object, tables):
    try:
        # show tables names
        show_table_names(tables)

        # get user input for insert
        table = input("\nEnter a table to update data: ")
        if(table not in tables):
            print("Dont have access to that table.")
            return
        attributes_str = input("Enter the name of the attribute: ")
        to_delete_str = input("What is the current value?: ")
        values_str = input("Enter the new value: ")

        # from string to list of attributes and values
        if "," in attributes_str:  # multiple attributes
            values = values_str.split(",")
        else:  # one attribute
            values = [values_str]

        query = """UPDATE {} SET {} = %s 
                        WHERE {} = \"{}\"""".format(table, attributes_str, attributes_str, to_delete_str)

        if db_object.update(query=query, values=values):
            #write transaction
            file = open("transactions.sql", "a")
            temp = """UPDATE {} SET {} = \"{}\" WHERE {} = \"{}\"""".format(table, attributes_str, values_str,attributes_str, to_delete_str)
            file.write("\n{};\n".format(temp))
            file.close
            print("Data successfully updated into {} \n".format(table))

    except: # data was not inserted, then handle error
        print("Error:", values_str, "failed to update in ", table, "\n")


# option 6 when user selects delete
def option6(db_object, tables):
    try:
        # show tables names
        show_table_names(tables)

        # get user input for insert
        table = input("\nEnter a table to delete data: ")
        if(table not in tables):
            print("Dont have access to that table.")
            return
        attributes_str = input("Enter the name attribute: ")
        to_delete_str = input("What is the current value of the attribute?: ")

        query = """DELETE FROM {} WHERE {} = %s""".format(table, attributes_str)
  
        if db_object.delete(query=query, values=to_delete_str):
            #write transaction
            file = open("transactions.sql", "a")
            temp = """DELETE FROM {} WHERE {} = \"{}\"""".format(table, attributes_str, to_delete_str)
            file.write("\n{};\n".format(temp))
            file.close
            print("Data successfully deleted from {} \n".format(table))

    except: # data was not inserted, then handle error
        print("Error: failed delete\n")


##### Driver execution.....
from database import DB

print("Setting up the database......\n")

# DB API object
db = DB(config_file="sqlconfig.conf")

# create a database (must be the same as the one is in your config file)
database = 'HealthCareOrgDB'
tempQuery = """SELECT count(*) AS TOTALNUMBEROFTABLES FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = \"{}\"""".format(database)
tablesFound = 0
try:
    myresult = db.select(tempQuery, "")
    tablesFound = myresult[0][0]
except:
    pass

if(tablesFound != 21):
    missing = 21 - tablesFound
    print("Missing {} tables...rebuilding".format(missing))
    if db.create_database(database=database, drop_database_first=True):
        print("Created database {}".format(database))
    else:
        print("An error occurred while creating database {} ".format(database))
    # create all the tables from databasemodel.sql
    db.run_sql_file("databasemodel.sql")
    # insert sample data from insert.sql
    db.run_sql_file("insert.sql")
    # run transactions.sql
    db.run_sql_file("transactions.sql")

print("\nSet up process finished\n")

#tables = db.get_table_names()

tables = ['Account', 'Appointments', 'Messages', 'HealthRecord']

show_menu()
option = int(input("Select one option from the menu: "))
while option != 7:
    if option == 1:
        option1(db)  # create your account
    elif option == 2:
        option2(db)  # login
    elif option == 3:
        if(isLoggedIn):
            option3(db, tables)
        else:
            print('Please login first')
    elif option == 4:
        if(isLoggedIn):
            option4(db, tables)
        else:
            print('Please login first')
    elif option == 5:
        if(isLoggedIn):
            option5(db, tables)
        else:
            print('Please login first')
    elif option == 6:
        if(isLoggedIn):
            option6(db, tables)
        else:
            print('Please login first')
    show_menu()
    option = int(input("Select one option from the menu: "))
# Example output for insert and search

"""
Setting up the database......

Created database musicsampledb
8 Executed queries from databasemodel.sql
29 Executed queries from insert.sql

Set up process finished

User Menu 
1. Create Account 
2. Login 
3. Search 
4. Insert 
5. Update 
6. Delete 
7. Exit 

Select one option from the menu: 4

Tables:
Album
Artist
Genre
Track

Enter a table to insert data: artist
Enter the name attribute/s separated by comma? id, name
Enter the values separated by comma: 7, Nina
Data successfully inserted into artist 

User Menu 
1. Create Account 
2. Login 
3. Search 
4. Insert 
5. Update 
6. Delete 
7. Exit 

Select one option from the menu: 4

Tables:
Album
Artist
Genre
Track

Enter a table to insert data: genre
Enter the name attribute/s separated by comma? description
Enter the values separated by comma: Hip Hop
Data successfully inserted into genre 

User Menu 
1. Create Account 
2. Login 
3. Search 
4. Insert 
5. Update 
6. Delete 
7. Exit 

Select one option from the menu: 3

Tables:
Album
Artist
Genre
Track

Select a table to search: artist
Search by (i.e name)? name
Enter the value: Nina


Results from: artist
id: [7]
name: ['Nina']


User Menu 
1. Create Account 
2. Login 
3. Search 
4. Insert 
5. Update 
6. Delete 
7. Exit 

Select one option from the menu: 3

Tables:
Album
Artist
Genre
Track

Select a table to search: genre
Search by (i.e name)? description
Enter the value: Hip Hop


Results from: genre
id: [6]
description: ['Hip Hop']


User Menu 
1. Create Account 
2. Login 
3. Search 
4. Insert 
5. Update 
6. Delete 
7. Exit 

Select one option from the menu: 
"""