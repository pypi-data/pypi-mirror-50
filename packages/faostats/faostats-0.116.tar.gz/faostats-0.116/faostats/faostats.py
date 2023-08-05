"""

"""


################
# Dependancies #
################

import pandas as pd
import glob as glob
import os
from sqlalchemy                 import create_engine
from sqlalchemy                 import Table, Column, String, MetaData, select, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import sessionmaker
import shutil
import zipfile

class data():

    @staticmethod
    def download():
        """
        Downloads data from UN website to a file location
        """
        #TODO complete this file
        pass

    @staticmethod
    def extract(**kwargs):
        """
        extracts the FAOSTAT file and then the subsequent folders in the file. It will then save the names of each sheet

        :return:
        """

        # Inputs
        fp = kwargs.get('filepath', '')
        fn = kwargs.get('filename', 'FAOSTAT')
        to_db = kwargs.get('to_db', False)
        delete_csv = kwargs.get('delete_csv',
                                True)  # option to delete csv after it has been uploaded as a table in db
        db_name = kwargs.get('db_name', 'faostat')
        db_user_name = kwargs.get('db_user_name', os.environ.get('POSTGRES_USER'))
        db_user_pw = kwargs.get('db_user_password', os.environ.get('POSTGRES_PW'))
        host = kwargs.get('host', "127.0.0.1")
        port = kwargs.get('port', '5432')
        driver = kwargs.get('driver', 'psycopg2')
        db_type = kwargs.get('db_type', 'postgresql')
        skip_table_if_exisits = kwargs.get('skip_table_if_exisits', False)

        # Extracting zipped FAOFILE

        with zipfile.ZipFile('%s/%s.zip' % (fp, fn), 'r') as zip_ref:
            zip_list = zip_ref.namelist()
            zip_ref.extractall('%s/%s' % (fp, fn))

        table_info = {}
        for file in zip_list:
            dir_name, file_extension = os.path.splitext(os.path.basename(file))
            path = '%s/%s/%s.zip' % (fp, fn, dir_name)
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall('%s/%s/' % (fp, fn))
                zip_ref.close()

                # general_cleaning
            os.remove('%s/%s/%s.zip' % (fp, fn, dir_name))
            csv_path = glob.glob('%s/%s/*.csv' % (fp, fn))[0]
            orig_csv_fn, file_ext = os.path.splitext(os.path.basename(csv_path))
            filename = data.sqlclean(dir_name)
            new_csv = '%s/%s/%s.csv' % (fp, fn, filename)
            old_csv = '%s/%s/%s.csv' % (fp, fn, orig_csv_fn)
            os.rename(old_csv, new_csv)

            if to_db:
                #name of table containing database info (i.e column names and rows etc)
                table_info_name = 'data_info'
                # Set up string to use for database connection.
                db_string = '%s+%s://%s:%s@%s:%s/%s' % (db_type,
                                                        driver,
                                                        db_user_name,
                                                        db_user_pw,
                                                        host,
                                                        port,
                                                        db_name)
                # Connecting to database
                engine = create_engine(db_string, pool_size=50, max_overflow=0)
                Session = sessionmaker(bind=engine)
                session = Session()
                Base = declarative_base()
                # Look up the existing tables from database
                Base.metadata.reflect(engine)
                # creates table in database if not already in
                if skip_table_if_exisits and engine.dialect.has_table(engine, filename):
                    df_raw = pd.read_csv(new_csv, encoding="ISO-8859-1", chunksize=1)
                    df = data.dataframeclean(df_raw)
                    if df.empty:
                        os.remove(new_csv)
                else:
                    for index, df_raw in enumerate(pd.read_csv(new_csv, encoding="ISO-8859-1", chunksize=50000)):
                        df = data.dataframeclean(df_raw)
                        if index == 0:
                            if not engine.dialect.has_table(engine, filename):
                                data.create_table(df, engine, filename, Base)
                            # clear old data
                            df_empty = pd.DataFrame(columns=list(df.columns))
                            df_empty.to_sql(filename, engine, if_exists='replace', index=False)
                        if df.empty:
                            os.remove(new_csv)
                            return
                        df.to_sql(filename, engine, if_exists='append', index=False)
                        print('batch %s from %s added to database' % (index, filename))
                # create or add table containing table and column data
                table_info.update({filename : list(df.columns)})
                # remove csv after adding to database
                if delete_csv:
                    os.remove(new_csv)
                data_info = pd.DataFrame.from_dict(table_info)
                if not engine.dialect.has_table(engine, table_info_name):
                    data.create_table(data_info, engine, table_info_name, Base)
                data_info.to_sql('data_info', engine, if_exists='replace', index=False)

        # Delete faostat folder once completed.
        try:
            shutil.rmtree('%s/%s' % (fp, fn))
        except:
            pass
        return

    @staticmethod
    def create_table(df, engine, filename, Base):
        p_key_list = ['Area Code', 'Element Code', 'Year Code', 'Item Code', 'Value']
        print('creating %s table.' % filename)
        meta = MetaData(engine)
        primary_key_flags = []
        # create primary key column
        print('columns: ', df.columns)
        for col_name in df.columns:
            if col_name == any(p_key_list):
                primary_key_flags.append(True)
            else:
                primary_key_flags.append(False)
        table = Table(filename, meta,
                      *(Column(col_name,
                               String,
                               primary_key=primary_key_flag)
                        for col_name, primary_key_flag in zip(df.columns, primary_key_flags)))
        table.create(engine)
        Base.metadata.reflect(engine)
        # primaryKeyColName = table.primary_key.columns.values()[0].name

    @staticmethod
    def sqlclean(string):
        ns = string.lower()
        ns = ns.replace('(', '')
        ns = ns.replace(')', '')
        ns = ns.replace(' ', '_')
        ns = ns.replace('agriculture', 'agri')
        ns = ns.replace('emissions', 'emiss')
        ns = ns.replace('normalized', 'norm')

        return ns

    @staticmethod
    def dataframeclean(df):
        num_cols = ['year', 'year_code', 'item_code', 'country_code', 'element_code', 'value']
        for col in df.columns:
            new_col = data.sqlclean(col)
            df.rename(columns={col: new_col}, inplace=True)
            if col in num_cols:
                df[new_col] = df[new_col].apply(pd.to_numeric, errors='coerce')

        return df


class analyse():

    def __init__(**kwargs):
        pass






