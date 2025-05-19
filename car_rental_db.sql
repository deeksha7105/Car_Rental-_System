create database car_rental_db;
use car_rental_db;
-- CUSTOMER TABLE
CREATE TABLE CUSTOMER (
    CustID INT PRIMARY KEY AUTO_INCREMENT,
    cust_name VARCHAR(100),
    cust_address TEXT,
    cust_contact VARCHAR(20),
    cust_licence VARCHAR(50)
);
select * from customer;

-- EMPLOYEE TABLE
CREATE TABLE EMPLOYEE (
    EmpID INT PRIMARY KEY AUTO_INCREMENT,
    emp_name VARCHAR(100),
    salary DECIMAL(10,2),
    emp_contact VARCHAR(20),
    emp_address TEXT
);

-- VEHICLE TABLE
CREATE TABLE VEHICLE (
    PlateNo VARCHAR(20) PRIMARY KEY,
    model VARCHAR(100),
    price DECIMAL(10,2),
    mileage INT,
    EmpID INT,
    FOREIGN KEY (EmpID) REFERENCES EMPLOYEE(EmpID)
);

-- RESERVATION TABLE
CREATE TABLE RESERVATION (
    ReserveID INT PRIMARY KEY AUTO_INCREMENT,
    reserve_date DATE,
    return_date DATE,
    pickup_location VARCHAR(255),
    no_of_days INT,
    CustID INT,
    PlateNo VARCHAR(20),
    FOREIGN KEY (CustID) REFERENCES CUSTOMER(CustID),
    FOREIGN KEY (PlateNo) REFERENCES VEHICLE(PlateNo)
);

-- RENT TABLE
CREATE TABLE RENT (
    RentID INT PRIMARY KEY AUTO_INCREMENT,
    total_cost DECIMAL(10,2),
    payment_method VARCHAR(50),
    ReserveID INT,
    FOREIGN KEY (ReserveID) REFERENCES RESERVATION(ReserveID)
);

-- CLIENT TABLE
CREATE TABLE CLIENT (
    ClientID INT PRIMARY KEY AUTO_INCREMENT,
    client_name VARCHAR(100),
    client_contact VARCHAR(20),
    client_address TEXT,
    PlateNo VARCHAR(20),
    id_proof VARCHAR(100),
    FOREIGN KEY (PlateNo) REFERENCES VEHICLE(PlateNo)
);

-- CLIENT COMMISSION TABLE
CREATE TABLE CLIENT_COMMISSION (
    CommissionID INT PRIMARY KEY AUTO_INCREMENT,
    ClientID INT,
    PlateNo VARCHAR(20),
    RentID INT,
    amount DECIMAL(10,2),
    payment_date DATE,
    FOREIGN KEY (ClientID) REFERENCES CLIENT(ClientID),
    FOREIGN KEY (PlateNo) REFERENCES VEHICLE(PlateNo),
    FOREIGN KEY (RentID) REFERENCES RENT(RentID)
);

-- USERS TABLE
CREATE TABLE USERS (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role ENUM('admin', 'customer', 'employee', 'client') NOT NULL,
    RefID INT -- links to CustID, EmpID, ClientID, etc. based on Role
);


