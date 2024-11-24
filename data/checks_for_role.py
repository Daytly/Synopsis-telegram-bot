from data.db.dbClasses.user import User
from data.db.db_session import create_session


def check_is_register(user_id):
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)
    if user is None:
        return False
    return True

def check_is_admin(user_id):
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)
    if user is None:
        return False
    return user.is_admin