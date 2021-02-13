-- Script name: inserts.sql
-- Author:      Bryan Caldera
-- Purpose:     insert sample data to test the integrity of this database system

USE `HealthCareOrgDB` ;

-- Account table inserts
INSERT INTO Account (account_id, MembershipNumber, DateCreated, Email, Password) VALUES (1, '0123', '2020-01-31', 'email1@gmail.com', 'fruitloops'),(null, '01234', '2020-09-20', 'email2@gmail.com', 'frostedflakes'),(null, '012345', '2020-11-01', 'email3@gmail.com', 'trix');

-- HealthRecord table inserts
INSERT INTO HealthRecord (record_id, PrimaryDoctorName, PreviousVisit) VALUES (1, 'Jane Doe', '2020-03-31'), (null, 'John Cena', '2020-10-21'), (null, 'Jane Doe', '2020-11-11');

-- Patient table inserts
INSERT INTO Patient (user_id, DateOfBirth, Name, PhoneNumber, Address, Account, HealthRecord) VALUES (1, '2002-01-21', 'Jose', '14151112222', '321 Fake street, CA', 1, 1), (null, '2000-02-21', 'Amy', '14152223333', '555 Real Ave, CA', 2, 2), (3, '2001-03-21', 'Thomas', '14157778888', '123 Fake way, CA', 3, 3);

-- GeneralAppointment table inserts
INSERT INTO GeneralAppointment (general_id, Reason) VALUES (1, 'My leg'),(null, 'Cold'),(null, 'flu');

-- RoutineAppointment table inserts
INSERT INTO RoutineAppointment (routine_id, DatePreviousVisit) VALUES (1, '2020-03-31'),(null, '2020-10-21'),(null, '2020-11-11');

-- Doctor table inserts
INSERT INTO Doctor (doctor_id, Name, Title) VALUES (1, 'Jane Doe', 'MD'),(null, 'John Cena', 'DO'),(null, 'Heather Smith', 'MD');

-- Appointments table inserts
INSERT INTO Appointments (appointment_id, Location, `Time/Date`, GeneralAppointment, RoutineAppointment, Patient, Doctor) VALUES (1, '999 Hospital St, CA', '2020-12-05 16:00:00', null, 1, 1, 1), (null, '999 Hospital St, CA', '2020-12-10 15:00:00', 1, null, 1, 2), (null, '999 Hospital St, CA', '2020-12-21 12:00:00', 3, null, 3, 1);

-- Medication table inserts
INSERT INTO Medication (medication_id, Count, CountPerDay, DatePrescribed, Name, HealthRecord) VALUES (1, 10, 1, '2020-02-13', 'Advil', 1), (null, 50, 2, '2020-01-20', 'Tylenol', 2), (null, 100, 2, '2019-05-06', 'Advil', 3);

-- Messages table inserts
INSERT INTO Messages (message_id, Message, `Date/Time`, Subject, Patient, Doctor) VALUES (1, 'Hello', '2020-10-05 16:00:00', 'Greetings', 1, 1),(null, 'You are dying', '2020-11-05 12:00:00', 'Sad news', 2, 2),(null, 'Healthy','2020-06-05 11:00:00', 'Results', 1, 1);

-- TestResults table inserts
INSERT INTO TestResults (test_id, Date, Name, Comments, HealthRecord) VALUES (1, '2020-10-05', 'Blood test', 'normal results', 1),(null, '2020-10-06', 'Iron in blood', 'low iron', 2),(null, '2020-10-07', 'Skin test', 'acne', 3);

-- MedicalCondition table inserts
INSERT INTO MedicalCondition (condition_id, Name, Date, HealthRecord) VALUES (1, 'Diabetes', '2020-10-05', 1),(null, 'Anemia', '2020-10-06', 2),(null, 'Acne', '2020-10-07', 3);

-- License table inserts
INSERT INTO License (license_id, Type, DateReceived) VALUES (1, 'Dermatology', '2020-11-05'),(null, 'Cardiology', '2020-09-05'),(null, 'Psychiatry', '2020-09-15');

-- Specialist table inserts
INSERT INTO Specialist (specialist_id, Type, Doctor, License) VALUES (1, 'Dermatologist', 3, 1),(null, 'Cardiologist', 2, 2),(null, 'Psychiatrist', 1, 3);

-- HealthCareOrganization table inserts
INSERT INTO HealthCareOrganization (org_id, Name, Address) VALUES (1, 'Kaiser', '564 3rd St, CA'),(null, 'Saint Jake', '4522 Hospital Way, CA'),(null, 'Saint Mary', '777 21st St, CA');

-- Emergency table inserts
INSERT INTO Emergency (emergency_id, Name, Address, HealthCareOrg) VALUES (1, 'Kaiser emergency', '565 3rd St, CA', 1),(null, 'Saint Jake emergency', '4523 Hospital Way, CA', 2),(null, 'Saint Mary emergency', '778 21st St, CA', 3);

-- EmergencyCareLine table inserts
INSERT INTO EmergencyCareLine (e_line_id, Reason, PriorityLevel, Patient, Department)  VALUES (1, 'Broken leg', 3, 1, 1),(null, 'Broken neck', 5, 2, 2),(null, 'Heart attack', 10, 3, 3);

-- UrgentCare table inserts
INSERT INTO UrgentCare (urgentcare_id, Name, Address, HealthCareOrg) VALUES (1, 'Kaiser urgent care', '566 3rd St, CA', 1),(null, 'Saint Jake urgent care', '4524 Hospital Way, CA', 2),(null, 'Saint Mary urgent care', '779 21st St, CA', 3);

-- UrgentCareLine table inserts
INSERT INTO UrgentCareLine (u_line_id, Reason, DateTimeArrived, Patient, Department) VALUES (1, 'Cough', '2020-12-05 10:00:00', 1, 1),(null, 'Arm hurts', '2020-12-05 11:00:00', 2, 2),(null, 'Nauseous', '2020-12-05 12:00:00', 3, 3);

-- Employee table inserts
INSERT INTO Employee (employee_id, Name, Title, HealthCareOrg) VALUES (1, 'Tim', 'Janitor', 1),(null, 'Jimmy', 'Pharmacist', 2),(null, 'Lisa', 'Nurse', 3);

-- Pharmacy table inserts
INSERT INTO Pharmacy (pharmacy_id, Name, Address, HealthCareOrg) VALUES (1, 'Kaiser pharmacy', '567 3rd St, CA', 1),(null, 'Saint Jake pharmacy', '4525 Hospital Way, CA', 2),(null, 'Saint Mary pharmacy', '780 21st St, CA', 3);

-- Lab table inserts
INSERT INTO Lab (lab_id, Name, Address, HealthCareOrg) VALUES (1, 'Kaiser lab', '568 3rd St, CA', 1),(null, 'Saint Jake lab', '4526 Hospital Way, CA', 2),(null, 'Saint Mary lab', '781 21st St, CA', 3);

