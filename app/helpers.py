"""
Imports
"""
import sys
from sqlalchemy.sql.expression import func

def add_entity(database, entity):
    """
    Adds an entity to the database
    """
    session = database.session
    session.expire_on_commit = False

    try:
        session.add(entity)
        session.commit()
    except BaseException as ex:
        traceback = sys.exc_info()
        database.app.logger.info(ex.with_traceback(traceback[2]))
        session.rollback()
        raise


def update_entity(database):
    """
    Updates an entity in the database
    """
    session = database.session
    session.expire_on_commit = False

    try:
        session.commit()
    except BaseException as ex:
        traceback = sys.exc_info()
        database.app.logger.info(ex.with_traceback(traceback[2]))
        session.rollback()
        raise


def get_next_id(database, entity) -> int:
    """
    Returns the next id for an entity
    """
    model = type(entity)
    session = database.session
    session.expire_on_commit = False
    this_id = 0

    try:
        max_id = session.query(func.max(model.id)).one_or_none()
        this_id = max_id[0] + 1
    except BaseException as ex:
        traceback = sys.exc_info()
        database.app.logger.info(ex.with_traceback(traceback[2]))
        raise

    return this_id

def get_id_by_item(database, entity, item_to_find, value_to_find) -> int:
    """
    Returns the id of an entity
    """
    session = database.session
    session.expire_on_commit = False
    this_id = 0
    try:
        this_id = session.query(entity). \
            filter_by(item_to_find == value_to_find).one_or_none()
    except BaseException as ex:
        traceback = sys.exc_info()
        database.app.logger.info(ex.with_traceback(traceback[2]))
        raise
    return this_id
