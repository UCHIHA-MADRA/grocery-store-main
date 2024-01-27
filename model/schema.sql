CREATE TABLE Users (
    UserID INTEGER,
    Name VARCHAR(100) NOT NULL,
    Username VARCHAR(100) NOT NULL,
    Password VARCHAR(100) NOT NULL,
    AccountType INT(1) DEFAULT 0,
    UNIQUE (Username),
    PRIMARY KEY (UserID)
);

CREATE TABLE Categories (
    CategoryID  INTEGER,
    Name        VARCHAR(100),
    PRIMARY KEY (CategoryID)
);

CREATE TABLE Products (
    ProductID   INTEGER,
    Name        VARCHAR(100),
    Quantity    INTEGER,
    CategoryID  INTEGER,
    PRIMARY KEY (ProductID),
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
);

CREATE TABLE Orders (
	OrderID	    INTEGER,
	UserID 	    INTEGER NOT NULL,
	Quantity	INTEGER NOT NULL,
	Date	    TEXT NOT NULL,
	ProductID	INTEGER NOT NULL,
	Status	    INTEGER NOT NULL,
	PRIMARY KEY(OrderID)
);