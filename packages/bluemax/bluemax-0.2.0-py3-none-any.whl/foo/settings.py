""" add your settings here """
import logging


def extend(settings):
    """ change settings """
    logging.info('extending settings')
    # settings["broadcaster"] = "bluemax.work.redis_broadcaster:RedisBroadcaster"
    settings["redis_url"] = "redis://localhost:6379"
    settings.setdefault("tornado",{})["static_dir"] = "foo/static"
    settings["debug"] = True
    return settings
