# Auto-generated SQL queries

car_1 = '''CREATE TABLE car_makers (
    Id        INTEGER,
    PRIMARY KEY (Id),
    Maker     TEXT,
    FullName  TEXT,
    Country   TEXT,
    FOREIGN KEY (Country) REFERENCES countries (CountryId)
);
CREATE TABLE car_names (
    MakeId  INTEGER,
    PRIMARY KEY (MakeId),
    Model   TEXT,
    Make    TEXT,
    FOREIGN KEY (Model) REFERENCES model_list (Model)
);
CREATE TABLE cars_data (
    Id          INTEGER,
    PRIMARY KEY (Id),
    MPG         TEXT,
    Cylinders   INTEGER,
    Edispl      REAL,
    Horsepower  TEXT,
    Weight      INTEGER,
    Accelerate  REAL,
    Year        INTEGER,
    FOREIGN KEY (Id) REFERENCES car_names (MakeId)
);
CREATE TABLE continents (
    ContId     INTEGER,
    PRIMARY KEY (ContId),
    Continent  TEXT   
);
CREATE TABLE countries (
    CountryId    INTEGER,
    PRIMARY KEY (CountryId),
    CountryName  TEXT,
    Continent    INTEGER,
    FOREIGN KEY (Continent) REFERENCES continents (ContId)
);
CREATE TABLE model_list (
    ModelId  INTEGER UNIQUE,
    PRIMARY KEY (ModelId),
    Maker    INTEGER,
    Model    TEXT,
    FOREIGN KEY (Maker) REFERENCES car_makers (Id)
);'''

concert_singer = '''CREATE TABLE concert (
    concert_ID    INT,
    PRIMARY KEY (concert_ID),
    concert_Name  TEXT,
    Theme         TEXT,
    Stadium_ID    TEXT,
    Year          TEXT,
    CONSTRAINT sqlite_autoindex_concert_1 UNIQUE (concert_ID),
    FOREIGN KEY (Stadium_ID) REFERENCES stadium (Stadium_ID)
);
CREATE TABLE singer (
    Singer_ID          INT,
    PRIMARY KEY (Singer_ID),
    Name               TEXT,
    Country            TEXT,
    Song_Name          TEXT,
    Song_release_year  TEXT,
    Age                INT,
    Is_male            bool,
    CONSTRAINT sqlite_autoindex_singer_1 UNIQUE (Singer_ID)
);
CREATE TABLE singer_in_concert (
    concert_ID  INT,
    Singer_ID   TEXT,
    CONSTRAINT sqlite_autoindex_singer_in_concert_1 UNIQUE (concert_ID, Singer_ID),
    FOREIGN KEY (Singer_ID) REFERENCES singer (Singer_ID),
    FOREIGN KEY (concert_ID) REFERENCES concert (concert_ID),
    PRIMARY KEY (concert_ID, Singer_ID)
);
CREATE TABLE stadium (
    Stadium_ID  INT,
    PRIMARY KEY (Stadium_ID),
    Location    TEXT,
    Name        TEXT,
    Capacity    INT,
    Highest     INT,
    Lowest      INT,
    Average     INT,
    CONSTRAINT sqlite_autoindex_stadium_1 UNIQUE (Stadium_ID)
);'''

employee_hire_evaluation = '''CREATE TABLE employee (
    Employee_ID  INT,
    PRIMARY KEY (Employee_ID),
    Name         TEXT,
    Age          INT,
    City         TEXT,
    CONSTRAINT sqlite_autoindex_employee_1 UNIQUE (Employee_ID)
);
CREATE TABLE evaluation (
    Employee_ID   TEXT,
    Year_awarded  TEXT,
    Bonus         REAL,
    CONSTRAINT sqlite_autoindex_evaluation_1 UNIQUE (Employee_ID, Year_awarded),
    FOREIGN KEY (Employee_ID) REFERENCES employee (Employee_ID),
    PRIMARY KEY (Employee_ID, Year_awarded)
);
CREATE TABLE hiring (
    Shop_ID       INT,
    Employee_ID   INT,
    PRIMARY KEY (Employee_ID),
    Start_from    TEXT,
    Is_full_time  bool,
    CONSTRAINT sqlite_autoindex_hiring_1 UNIQUE (Employee_ID),
    FOREIGN KEY (Employee_ID) REFERENCES employee (Employee_ID),
    FOREIGN KEY (Shop_ID) REFERENCES shop (Shop_ID)
);
CREATE TABLE shop (
    Shop_ID          INT,
    PRIMARY KEY (Shop_ID),
    Name             TEXT,
    Location         TEXT,
    District         TEXT,
    Number_products  INT,
    Manager_name     TEXT,
    CONSTRAINT sqlite_autoindex_shop_1 UNIQUE (Shop_ID)
);'''

flight_2 = '''CREATE TABLE airlines (
    uid           INTEGER,
    PRIMARY KEY (uid),
    Airline       TEXT,
    Abbreviation  TEXT,
    Country       TEXT   
);
CREATE TABLE airports (
    City           TEXT,
    AirportCode    TEXT,
    PRIMARY KEY (AirportCode),
    AirportName    TEXT,
    Country        TEXT,
    CountryAbbrev  TEXT,
    CONSTRAINT sqlite_autoindex_airports_1 UNIQUE (AirportCode)
);
CREATE TABLE flights (
    Airline        INTEGER,
    FlightNo       INTEGER,
    SourceAirport  TEXT,
    DestAirport    TEXT,
    CONSTRAINT sqlite_autoindex_flights_1 UNIQUE (Airline, FlightNo),
    FOREIGN KEY (DestAirport) REFERENCES airports (AirportCode),
    FOREIGN KEY (SourceAirport) REFERENCES airports (AirportCode),
    PRIMARY KEY (Airline, FlightNo)
);'''

pets_1 = '''CREATE TABLE Has_Pet (
    StuID  INTEGER,
    PetID  INTEGER,
    FOREIGN KEY (StuID) REFERENCES Student (StuID),
    FOREIGN KEY (PetID) REFERENCES Pets (PetID)
);
CREATE TABLE Pets (
    PetID    INTEGER,
    PRIMARY KEY (PetID),
    PetType  VARCHAR(20),
    pet_age  INTEGER,
    weight   REAL       
);
CREATE TABLE Student (
    StuID      INTEGER,
    PRIMARY KEY (StuID),
    LName      VARCHAR(12),
    Fname      VARCHAR(12),
    Age        INTEGER,
    Sex        VARCHAR(1),
    Major      INTEGER,
    Advisor    INTEGER,
    city_code  VARCHAR(3) 
);'''

