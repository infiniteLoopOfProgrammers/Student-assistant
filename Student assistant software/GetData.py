import pyodbc


def connectionString() -> str:
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=./Data/Courses_main.accdb;'
    )
    return conn_str


def DataAdapter(query,params):
    cnxn = pyodbc.connect(connectionString())
    cursor = cnxn.cursor()
    cursor.execute(query,params)
    rows = cursor.fetchall()
    cnxn.close()
    return rows

