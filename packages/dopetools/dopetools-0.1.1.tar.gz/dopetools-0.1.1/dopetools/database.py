import sqlalchemy as db
from sqlalchemy.engine.reflection import Inspector
import pandas as pd
import time
import csv
from io import StringIO
from helper_funcs.general import get_time_interval


class DataBaseManager:
    """
    Manages connection to postgres data base.
    """
    def __init__(self):
        self.engine = []
        self.tables = {}

    @classmethod
    def create_tables(db_url, schema_name, table_model, symbols):
        schema_name = schema_name.lower()
        symbols = [symbol.lower() for symbol in symbols]

        # connect to database
        engine = db.create_engine(db_url)
        db_tables = {}

        # create schema first if required
        engine.execute('CREATE SCHEMA IF NOT EXISTS {};'.format(schema_name))

        # get names of already existing tables
        inspector = Inspector.from_engine(engine)
        existing_tables = inspector.get_table_names(schema_name)

        for symbol in symbols:
            db_tables[symbol] = table_model
            db_tables[symbol].__table__.name = symbol
            db_tables[symbol].__table__.schema = schema_name
            if symbol not in existing_tables:
                db_tables[symbol].__table__.create(engine)

        return engine, db_tables

    def write_into_DB(queue_to_db, db_engine, symbols,  schema_name, delta_t_save, offset_t_save, logger=[]):
        symbols = [symbol.lower() for symbol in symbols]
        agg_ticks = dict.fromkeys(symbols, pd.DataFrame())
        t_next_save = get_time_interval(time.time()*1000, delta_t_save, offset_t_save)
        while True:
            # Receive new ticks
            new_tick = queue_to_db.get()
            # get current symbol, index and time
            if not new_tick:
                continue
            symbol = new_tick.pop('symbol').lower()
            tmp = pd.DataFrame(new_tick, index=[0])
            if len(agg_ticks[symbol]) == 0:
                agg_ticks[symbol] = tmp
            else:
                agg_ticks[symbol] = agg_ticks[symbol].append(tmp)
            t_now = time.time()*1000
            if t_now > t_next_save:
                t_next_save = get_time_interval(t_now, delta_t_save, offset_t_save)
                for sym, df in agg_ticks.items():
                    if len(df) > 0:
                        df.to_sql(sym, db_engine,
                                  schema=schema_name,
                                  if_exists='append',
                                  index=False,
                                  method=psql_insert_copy)
                        if logger:
                            logger.info('Inserted table of size {} x {} into {}.{}'.format(df.shape[0], df.shape[1],
                                                                                           schema_name, sym))
                agg_ticks = dict.fromkeys(symbols, pd.DataFrame())
            queue_to_db.task_done()
        return True

    # for writing data into a postgresql database more quickly
    def psql_insert_copy(table, conn, keys, data_iter):
        # gets a DBAPI connection that can provide a cursor
        dbapi_conn = conn.connection
        with dbapi_conn.cursor() as cur:
            s_buf = StringIO()
            writer = csv.writer(s_buf)
            writer.writerows(data_iter)
            s_buf.seek(0)

            columns = ', '.join('"{}"'.format(k) for k in keys)
            if table.schema:
                table_name = '{}.{}'.format(table.schema, table.name)
            else:
                table_name = table.name

            sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
                table_name, columns)
            cur.copy_expert(sql=sql, file=s_buf)



def init_database_eval(schema_name, symbols, columns, db_url):
    # connect to database
    engine = db.create_engine(db_url)
    inspector = Inspector.from_engine(engine)
    metadata = db.MetaData()
    symbols = [symbol.lower() for symbol in symbols]

    # create schema first if required
    engine.execute('CREATE SCHEMA IF NOT EXISTS {};'.format(schema_name))
    existing_tables = inspector.get_table_names(schema_name)
    for symbol in symbols:
        if symbol not in existing_tables:
            # create a new table
            sql_tab = db.Table(symbol, metadata, schema=schema_name)
            # define here the functions that are available
            exposed_methods = {'sql_tab': sql_tab,
                               'Column': db.Column,
                               'Integer': db.Integer,
                               'BigInteger': db.BigInteger,
                               'Float': db.Float,
                               'Numeric': db.Numeric,
                               'Boolean': db.Boolean,
                               'Text': db.Text,
                               'null': db.null,
                               'String': db.String}
            # create new columns
            for col_name, definition in columns.items():
                execute_str = "sql_tab.append_column(Column('{}', {}, default= {}))".format(col_name, definition[0], definition[1])
                eval(execute_str, {'__builtins__': None}, exposed_methods)

    metadata.create_all(engine)  # Creates the table
    return engine


def import_model(module_name, class_name):
    # load table class definition
    module = __import__(module_name, fromlist=[class_name])
    return getattr(module, class_name)