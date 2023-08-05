# -*- coding: utf-8 -*-
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# Base.metadata.create_all(engine)
SQLALCHEMY_POOL_RECYCLE = 10
db = SQLAlchemy(use_native_unicode='utf8')
Base = declarative_base()

DBSession = sessionmaker()
Scoped = scoped_session(DBSession)


def generate_engine(url: str, pool_recycle: int = SQLALCHEMY_POOL_RECYCLE) -> Engine:
    return create_engine(url, encoding='utf-8', echo=True, pool_recycle=pool_recycle)


def call_procedure(url: str, procedure_name: str, *args: Any) -> None:
    """

    :param url:
    :param procedure_name: just procedure name not call procedure_name
    :param args:
    :return:
    """
    connection = generate_engine(url).raw_connection()
    cursor = connection.cursor()
    try:
        s = cursor.callproc(procedure_name, args=args)
        print(s)
        connection.commit()
    except Exception as e:
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
