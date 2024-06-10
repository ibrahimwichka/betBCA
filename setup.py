
import sqlite3
import flask
from app import drop_all_tables, create_tables, insert_data


drop_all_tables()
create_tables()
insert_data()