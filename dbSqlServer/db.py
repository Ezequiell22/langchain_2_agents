from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv
from urllib.parse import quote_plus
import os

_ = load_dotenv(find_dotenv())

odbc_str = (
    f"DRIVER={os.getenv('ODBC_DRIVER')};"
    f"SERVER={os.getenv('SERVER_DB')};"
    f"DATABASE={os.getenv('DATABASE')};"
    f"UID={os.getenv('USER_DB')};"
    f"PWD={os.getenv('PASS_DB')};"
    f"TrustServerCertificate=yes;"
)
quoted = quote_plus(odbc_str)
connection_string = f"mssql+pyodbc:///?odbc_connect={quoted}"

engine = create_engine(connection_string, echo=False)