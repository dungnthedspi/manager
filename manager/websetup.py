"""Setup the manager application"""
import logging

from manager.config.environment import load_environment
from manager.model.meta import Session, Base

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup manager here"""
    # Don't reload the app if it was loaded under the testing environment
    load_environment(conf.global_conf, conf.local_conf)

    from manager.model.meta import Base, Session
    log.info("Creating tables")
    Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)
    log.info("Successfully setup")

    # Create the tables if they don't already exist
    Base.metadata.create_all(bind=Session.bind)
