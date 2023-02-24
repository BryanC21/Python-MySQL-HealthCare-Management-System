# Python-MySQL-Health Care Management System

The application is a health management system that would be used by a health care provider. The application is using Python for the interface, and MySQL for the database. The database includes patients, doctors, appointments, health records, medications, messaging and more. The interface allows you to view, update, delete, insert database contents. The program can detect if any DB tables are missing and uses a change log to recover missing data.

![alt text](https://i.imgur.com/RIIEkl3.png)

#### Sample run:

Setting up the database......  

Missing 21 tables...rebuilding  
Created database HealthCareOrgDB  
51 Executed queries from databasemodel.sql   
22 Executed queries from insert.sql  
1 Executed queries from transactions.sql  
Set up process finished  
User Menu  
1. Create Account   
2. Login  
3. Search  
4. Insert  
5. Update  
6. Delete  
7. Exit    
Select one option from the menu: 1   
Email: bryan@gmail.com  
Password: 123  
Account successfully created  

User Menu  
1. Create Account  
2. Login  
3. Search  
4. Insert  
5. Update  
6. Delete  
7. Exit  
Select one option from the menu: 3  
Tables: Account Appointments Messages HealthRecord  
Select a table to search: Messages    
Search by (i.e name)? message_id   
Enter the value: 1  
(('Hello', 'Greetings', 'Jose', 'Jane Doe'),)   
Results from: Messages  
Message: ['Hello']  
Subject: ['Greetings']  
Patient: ['Jose']   
Doctor: ['Jane Doe']    

User Menu  
1. Create Account   
2. Login  
3. Search  
4. Insert  
5. Update  
6. Delete   
7. Exit  
Select one option from the menu: 4  
Tables: Account Appointments Messages HealthRecord  
Enter a table to insert data: Messages  
Enter the name attribute/s separated by comma? Subject,Message   
Enter the values separated by comma: subject, message  
Data successfully inserted into Messages  

User Menu  
1. Create Account   
2. Login  
3. Search   
4. Insert     
5. Update   
6. Delete   
7. Exit  
Select one option from the menu: 5  
Tables: Account Appointments Messages HealthRecord  
Enter a table to update data: Account  
Enter the name of the attribute: Email  
What is the current value?: Bryan@gmail.com   
Enter the new value: bryan2@yahoo.com   
Data successfully updated into Account  

User Menu  
1. Create Account   
2. Login  
3. Search  
4. Insert  
5. Update  
6. Delete  
7. Exit  
Select one option from the menu: 6  
Tables: Account Appointments Messages HealthRecord  
Enter a table to delete data: HealthRecord  
Enter the name attribute: record_id  
What is the current value of the attribute?: 2     
Data successfully deleted from HealthRecord    

User Menu  
1. Create Account   
2. Login  
3. Search  
4. Insert  
5. Update  
6. Delete  
7. Exit  
Select one option from the menu: 7  

**Running app again**  

Set up process finished  
User Menu  
1. Create Account   
2. Login  
3. Search  
4. Insert  
5. Update  
6. Delete  
7. Exit  
Select one option from the menu: 2   
Email: bryan2@yahoo.com   
Password: 123  
Logged in as, bryan2@yahoo.com  
