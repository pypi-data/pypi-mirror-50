# -*- coding: utf-8 -*-

"""Collection of methods for communication with database
"""

import abc
from io import StringIO

import pandas as pd
import psycopg2
from sqlalchemy import exc

from db_commuter.connections import *

__all__ = [
    "SQLiteCommuter",
    "PgCommuter"
]


class Commuter(abc.ABC):
    def __init__(self, connector):
        self.connector = connector

    @abc.abstractmethod
    def select(self, cmd, **kwargs):
        """Select data from database object using selection command (cmd)
        and put it in pandas object
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def insert(self, obj, data, **kwargs):
        """Insert pandas object (data) into database object (obj)
        """
        raise NotImplementedError()


class SQLCommuter(Commuter):
    """Parent class for SQL databases
    """
    def __init__(self, connector):
        super().__init__(connector)

    @abc.abstractmethod
    def delete_table(self, table_name, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def is_table_exist(self, table_name, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def execute(self, cmd, vars=None, commit=True):
        """Execute SQL command (cmd) and commit (if True) changes to database

        :param cmd: text, database command
        :param vars: parameters to command, may be provided as sequence or mapping
        :param commit: boolean, persist changes to database if True
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def execute_script(self, path2script, commit=True):
        """Execute multiple SQL statements separated by semicolon
        """
        raise NotImplementedError()

    def select(self, cmd, **kwargs):
        with self.connector.engine.connect() as conn:
            data = pd.read_sql_query(cmd, conn)

        return data

    def insert(self, table_name, data, **kwargs):
        """Insert pandas dataframe (data) into database table (table_name)

        :keyword schema: specify the schema, if None, use default schema.
        :keyword chunksize: rows will be written in batches of this size at a time
        :raises ValueError: if insert fails
        """
        schema = kwargs.get('schema', None)
        chunksize = kwargs.get('chunksize', None)

        with self.connector.engine.connect() as conn:
            try:
                data.to_sql(table_name,
                            con=conn,
                            schema=schema,
                            if_exists='append',
                            index=False,
                            chunksize=chunksize)
            except (ValueError, exc.IntegrityError) as e:
                raise ValueError(e)


class SQLiteCommuter(SQLCommuter):
    """Methods for communication with SQLite database
    """
    def __init__(self, path2db):
        super().__init__(SQLiteConnector(path2db))

    def delete_table(self, table_name, **kwargs):
        self.execute('drop table if exists %s' % table_name)

    def is_table_exist(self, table_name, **kwargs):
        cmd = 'select name from sqlite_master where type=\'table\' and name=\'%s\'' % table_name

        data = self.select(cmd)

        if len(data) > 0:
            return data.name[0] == table_name

        return False

    def execute(self, cmd, vars=None, commit=True):
        """Execute SQL command (cmd) and commit (if True) changes to database

        :param cmd: text, database command
        :param vars: parameters to command, may be provided as sequence or mapping
        :param commit: boolean, persist changes to database if True
        """
        # set the connection
        with self.connector.make_connection() as conn:
            # create cursor object
            cur = conn.cursor()
            # execute sql command
            if vars is None:
                cur.execute(cmd)
            else:
                cur.execute(cmd, vars)

            # save the changes
            if commit:
                conn.commit()

        # close the connection
        self.connector.close_connection()

    def execute_script(self, path2script, commit=True):
        with open(path2script, 'r') as fh:
            script = fh.read()

        with self.connector.make_connection() as conn:
            cur = conn.cursor()
            cur.executescript(script)

            if commit:
                conn.commit()

        self.connector.close_connection()


class PgCommuter(SQLCommuter):
    """Methods for communication with PostgreSQL database
    """
    def __init__(self, host, port, user, password, db_name, **kwargs):
        super().__init__(PgConnector(host, port, user, password, db_name, **kwargs))

    @classmethod
    def from_dict(cls, params, **kwargs):
        """Alternative constructor used access parameters from dictionary
        """
        return cls(params['host'], params['port'], params['user'],
                   params['password'], params['db_name'], **kwargs)

    def execute(self, cmd, vars=None, commit=True):
        """Execute SQL command (cmd) and commit (if True) changes to database

        :param cmd: text, database command
        :param vars: parameters to command, may be provided as sequence or mapping
        :param commit: boolean, persist changes to database if True
        """
        # set the connection
        with self.connector.make_connection() as conn:
            # create cursor object
            with conn.cursor() as cur:
                # execute sql command
                if vars is None:
                    cur.execute(cmd)
                else:
                    cur.execute(cmd, vars)

            # save the changes
            if commit:
                conn.commit()

        self.connector.close_connection()

    def execute_script(self, path2script, commit=True):
        with open(path2script, 'r') as fh:
            script = fh.read()

        with self.connector.make_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(script)

            if commit:
                conn.commit()

        self.connector.close_connection()

    def insert_fast(self, table_name, data):
        """Place dataframe to buffer and use copy_from method for inserting from buffer
        """
        with self.connector.make_connection() as conn:
            with conn.cursor() as cur:
                # put pandas frame to buffer
                s_buf = StringIO()
                data.to_csv(s_buf, index=False, header=False)
                s_buf.seek(0)
                # insert to table
                try:
                    cur.copy_from(s_buf, table_name, sep=',', null='')
                except (ValueError, exc.ProgrammingError, psycopg2.ProgrammingError, psycopg2.IntegrityError) as e:
                    raise ValueError(e)

            conn.commit()

        self.connector.close_connection()

    def delete_table(self, table_name, **kwargs):
        """
        :keyword schema: name of the database schema
        :keyword cascade: boolean, True if delete cascade
        """
        schema = kwargs.get('schema', None)
        cascade = kwargs.get('cascade', False)

        table_name = self.__get_table_name(schema, table_name)

        if cascade:
            self.execute('drop table if exists %s cascade' % table_name)
        else:
            self.execute('drop table if exists %s' % table_name)

    def is_table_exist(self, table_name, **kwargs):
        schema = kwargs.get('schema', 'public')

        with self.connector.make_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "select * from information_schema.tables where table_name=%s and table_schema=%s",
                    (table_name, schema))

        self.connector.close_connection()

        return bool(cur.rowcount)

    def get_connections_count(self):
        cmd = \
            f'select sum(numbackends) ' \
            f'from pg_stat_database'

        df = self.select(cmd)

        return df.iloc[0][0]

    @staticmethod
    def __get_table_name(schema, table_name):
        if schema is None:
            return table_name
        return schema + '.' + table_name

