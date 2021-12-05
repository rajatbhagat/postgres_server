import pandas as pd
import csv


def add_entry_to_db_repo(dbName, VM, Owner, Status, AccessType):
    df1 = pd.read_csv('db_repository.csv')
    # print(len(df1.index))
    ID = len(df1.index) + 1
    fields = [ID, dbName, VM, Owner, Status, AccessType]
    with open('db_repository.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        # print('write success!!')


def update_active_flag_db_repo(dbName, status):
    df = pd.read_csv('db_repository.csv')
    df.loc[df['dbName'] == dbName, 'Status'] = status
    # print(df)
    df.to_csv('db_repository.csv', index=False)


def check_db_exists(dbName, username):
    df = pd.read_csv('db_repository.csv')
    if ((df['dbName'] == dbName) & (df['Owner'] == username)).any():
        print(df.loc[df['dbName'] == dbName, 'Status'][0])
        if df.loc[df['dbName'] == dbName, 'Status'][0] == 'Active':
            return True
        else:
            return False
    else:
        return False
