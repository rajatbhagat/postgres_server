import pandas as pd
import csv


def add_entry_to_db_repo(dbName, VM, Owner, Status, AccessType):
    df1 = pd.read_csv('./db_repository.csv')
    # print(len(df1.index))
    ID = len(df1.index) + 1
    fields = [ID, dbName, VM, Owner, Status, AccessType]
    with open('db_repository.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        # print('write success!!')


def update_active_flag_db_repo(dbName, status):
    df = pd.read_csv('./db_repository.csv')
    df.loc[df['dbName'] == dbName, 'Status'] = status
    # print(df)
    df.to_csv('db_repository.csv', index=False)


def check_db_exists(dbName, username):
    df = pd.read_csv('./db_repository.csv')
    if ((df['dbName'] == dbName) & (df['Owner'] == username)).any():
        # print(df.loc[df['dbName'] == dbName, 'Status'][0])
        if df.loc[df['dbName'] == dbName, 'Status'][0] == 'Active':
            return True
        else:
            return False
    else:
        return False


def get_vm_details(dbName):
    df = pd.read_csv('./db_repository.csv')
    if dbName in df['dbName'].values.tolist():
        return df.loc[df['dbName'] == dbName, 'VM'][0]
    else:
        return None


# TODO returns the first IP - needs to return according to the available space
def check_available_space():
    df = pd.read_csv('./central_repository.csv')
    # print(df['IsAlive'][0])
    # print((df.loc[df['ID'] == 1, 'ID'][0]))
    # print(((df.loc[df['ID'] == 1, 'ID'][0]) == 1))
    # print(df[df['ID'] == 1])
    # if df['IsAlive'][0] is True:
    return df.loc[df['ID'] == 1, 'VM'][0]


def update_type(VM, type):
    df = pd.read_csv('./central_repository.csv')
    df.loc[df['VM'] == VM, 'Type'] = type
    df.to_csv('./central_repository.csv', index=False)


# update_type('10.0.0.17', 'master')
