import sqlite3
from sqlite3 import Error
from constants_3P import DATABASE_NAME,TEXT_NAME,METER_ID,READ_DAY,DEMANT_TIME,COSTUMER_NAME


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def get_labels(conn, table):
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}');")
    return [label[0] for label in cursor.fetchall()]


def tableKeysContact():
    keysTable = [
        "d000",
        "d080",
        "d091",
        "d092",
        "d095",
        "d180",
        "d181",
        "d182",
        "d183",
        "d1801",
        "d1811",
        "d1821",
        "d1831",
        "d1841",
        "d580",
        "d5801",
        "d880",
        "d8801",
        "d160",
        "d3170",
        "d5170",
        "d7170",
        "d3270",
        "d5270",
        "d7270",
        "d9661",
        "d9670",
        "d9671",
    ]
    keysTableResult = ""
    for item in keysTable:
        keysTableResult = keysTableResult + item + ","

    return keysTableResult[0:-1]


def insertData():
    try:
        sqliteConnection = sqlite3.connect(DATABASE_NAME)
        cursor = sqliteConnection.cursor()
        print("VTYS bağlantısı başarılı...")

        if (
            SqlDataCount(METER_ID) == 0
        ):  # Sayaç ID kontrolü burada yapılıyor. Bu sayaç yoksa kayıt ekleme işlemine geöilmiyor.
            print("Elektrik sayacı bulunmuyor...")
            return

        sqlite_insert_query = (
            "INSERT INTO data ("
            + tableKeysContact()
            + ") VALUES ("
            + getDatas(TEXT_NAME)
            + ")"
        )

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Kayıtlar SqLite veritabanına başarıyla eklendi.", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print(getDatas(TEXT_NAME))
        print("SqLite veritabanına tabloya veri ekleme hatası!")
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("SQLite VTYS bağlantısı kapatıldı.")


def insertMeterData():
    try:
        sqliteConnection = sqlite3.connect(DATABASE_NAME)
        cursor = sqliteConnection.cursor()
        print("VTYS bağlantısı başarılı...")

        sqlite_insert_query = """INSERT INTO elcMeter (d000,readDay,demandTime,costumerName) VALUES (?,?,?,?)"""

        executeDatas = [METER_ID, READ_DAY, DEMANT_TIME, COSTUMER_NAME]
        count = cursor.execute(sqlite_insert_query, executeDatas)
        sqliteConnection.commit()
        print("Kayıtlar SqLite veritabanına başarıyla eklendi. ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        pass
        print("SqLite veritabanına veri ekleme hatası!", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("SQLite VTYS bağlantısı kapatıldı.")


def SqlDataCount(elcMeterName):
    sqliteConnection = sqlite3.connect(DATABASE_NAME)
    cursor = sqliteConnection.cursor()

    cursor.execute("SELECT * FROM elcMeter WHERE d000='" + elcMeterName + "'")
    sqliteConnection.commit()

    # Close the connection

    count = len(cursor.fetchall())
    sqliteConnection.close()
    return count


def getDatas(fileName):
    keys = [
        "0.0.0",
        "0.8.0",
        "0.9.1",
        "0.9.2",
        "0.9.5",
        "1.8.0",
        "1.8.1",
        "1.8.2",
        "1.8.3",
        "1.8.0*1",
        "1.8.1*1",
        "1.8.2*1",
        "1.8.3*1",
        "1.8.4*1",
        "5.8.0",
        "5.8.0*1",
        "8.8.0",
        "8.8.0*1",
        "1.6.0",
        "31.7.0",
        "51.7.0",
        "71.7.0",
        "32.7.0",
        "52.7.0",
        "72.7.0",
        "96.6.1",
        "96.70",
        "96.71",
    ]
    i = 0
    finalResults = ""

    f = open(fileName)

    for line in f:
        i = i + 1
        getindexc = line.find("(")
        getindexcl = line.find(")")
        sCount = line.count("*")

        if getindexc < 0:
            continue

        keys_value = line[0:getindexc]

        if not keys_value in keys:
            continue

        if sCount == 1:
            if line.find("*") < getindexc:
                getKeyValue = line[getindexc + 1 : getindexcl]
            else:
                getindexs = line.find("*")
                getKeyValue = line[getindexc + 1 : getindexs]
        elif sCount == 2:
            getindexs = line[getindexc + 1 :].find("*")
            getKeyValue = line[getindexc + 2 : getindexs]
        elif sCount == 0:
            getKeyValue = line[getindexc + 1 : getindexcl]

        if keys_value in ["0.0.0", "0.9.1", "0.9.2", "96.70", "96.71"]:
            getKeyValue = "'" + getKeyValue + "'"
        else:
            getKeyValue = float(getKeyValue)

        finalResult = str(getKeyValue)
        finalResults = finalResults + finalResult + ","

    finalResults = finalResults[0:-1]
    return str(finalResults)


def mainDB():
    database = DATABASE_NAME

    sql_create_data_table = """CREATE TABLE IF NOT EXISTS data (
                                    d000 TEXT FOREING KEY REFERENCES elcMeter(d000),
                                    d080 REAL,
                                    d091 TEXT,
                                    d092 TEXT,
                                    d095 REAL,
                                    d180 REAL,
                                    d181 REAL,
                                    d182 REAL,
                                    d183 REAL,
                                    d1801 REAL,
                                    d1811 REAL,
                                    d1821 REAL,
                                    d1831 REAL,
                                    d1841 REAL,
                                    d580 REAL,
                                    d5801 REAL,
                                    d880 REAL,
                                    d8801 REAL,
                                    d160 REAL,
                                    d3170 REAL,
                                    d5170 REAL,
                                    d7170 REAL,
                                    d3270 REAL,
                                    d5270 REAL,
                                    d7270 REAL,
                                    d9661 REAL,
                                    d9670 TEXT,
                                    d9671 TEXT
                                );"""

    sql_create_elcMeter_table = """CREATE TABLE IF NOT EXISTS elcMeter (
                                    d000 text NOT NULL UNIQUE,
                                    readDay INT,
                                    demandTime INT,
                                    costumerName TEXT,
                                    PRIMARY KEY(d000) 
                                );"""
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_elcMeter_table)
        create_table(conn, sql_create_data_table)

    else:
        print("Hata! Veritabanı tablo oluşturulmadı.")

    # MAİN METOT


def writeDB():
    mainDB()  # Tablo oluşturma için
    insertMeterData()  # Sayaç bilgilerini  ekleme için
    insertData()  # İlgili sayaçla ilgili değerleri eklemek için.
