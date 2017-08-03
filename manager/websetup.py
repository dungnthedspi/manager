"""Setup the manager application"""
import logging

from manager.config.environment import load_environment
from manager.model.meta import Session, Base
from authkit.users.sqlalchemy_driver import UsersFromDatabase
from manager import model
from manager.model import meta

log = logging.getLogger(__name__)

log.info("Adding the AuthKit model...")
users = UsersFromDatabase(model)

def setup_app(command, conf, vars):
    """Place any commands to setup manager here"""
    # Don't reload the app if it was loaded under the testing environment
    load_environment(conf.global_conf, conf.local_conf)

    from manager.model.meta import Base, Session
    log.info("Creating tables")
    Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)

    meta.metadata.bind = meta.engine
    meta.metadata.drop_all(checkfirst=True)
    meta.metadata.create_all(checkfirst=True)
    # log.info("Adding roles and uses...")
    users.role_create("admin")
    users.role_create("delete")
    users.role_create("editor")
    users.group_create("admin")
    users.group_create("student")
    # users.user_create("foo", password="foo123")
    # users.user_add_role("foo", role="editor")
    # users.user_set_group("foo", 'student')
    users.user_create("admin@gmail.com", password="a123456")
    users.user_add_role("admin@gmail.com", role="delete")
    users.user_add_role("admin@gmail.com", role="admin")
    users.user_set_group("admin@gmail.com", 'admin')
    Session.commit()
    log.info("Successfully setup")

    # Create the tables if they don't already exist
    # Base.metadata.create_all(bind=Session.bind)
