import sqlite3 as sq

con = None
c = None


def start_db_connection(version):
    global con
    global c
    con = sq.connect(version)
    c = con.cursor()


def get_entries_from_table(pkg_str, column_select='*'):
    global c
    c.execute("SELECT " + column_select + " from " + pkg_str)
    rows = c.fetchall()
    return rows


def get_all_tables():
    c.execute("select * from sqlite_master")
    table_list = c.fetchall()
    return [a[1] for a in table_list]


def drop_table(pkg=None):
    global c
    c.execute(f'DROP TABLE IF EXISTS {pkg}')


def drop_cols():
    global c
    # ['Hash', 'FileSizeB', 'FileType', 'RefID', 'RefPKG']
    c.execute('CREATE TABLE IF NOT EXISTS everythingbackup (FileName TEXT, Reference TEXT, FileType TEXT)')
    c.execute(f'INSERT INTO everythingbackup SELECT FileName, Reference, FileType FROM Everything WHERE FileType=="Texture Header"')
    c.execute('DROP TABLE Everything')
    c.execute(f'ALTER TABLE everythingbackup RENAME TO Everything')
    con.commit()
    c.execute('vacuum')