"""
Imports
"""
import sys
from sqlalchemy.sql.expression import func


def _add_entity(database, entity):
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


def _update_entity(database):
    session = database.session
    session.expire_on_commit = False

    try:
        session.commit()
    except BaseException as ex:
        traceback = sys.exc_info()
        database.app.logger.info(ex.with_traceback(traceback[2]))
        session.rollback()
        raise


def _get_next_id(database, entity) -> int:
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
