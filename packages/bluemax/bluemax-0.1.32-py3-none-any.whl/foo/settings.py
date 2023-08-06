""" add your settings here """
import logging


def extend(settings):
    """ change settings """
    logging.info('extending settings')
    # settings["broadcaster"] = "bluemax.work.redis_broadcaster:RedisBroadcaster"
    settings["REDIS_URL"] = "redis://localhost:6379"
    settings.setdefault("tornado",{})["STATIC_DIR"] = "foo/static"
    settings["DEBUG"] = True
    return settings
