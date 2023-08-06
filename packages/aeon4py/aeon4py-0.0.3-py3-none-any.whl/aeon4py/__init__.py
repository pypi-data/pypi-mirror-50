import threading

from aeoncloud.sessions.session_factory_adapter import ISessionFactoryAdapter
from aeoncloud.sessions.http_session_factory_adapter import HttpSessionFactoryAdapter

from aeon4py.sessions.java_session_factory_adapter import JavaSessionFactoryAdapter


def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


class Aeon:
    adapter = None


@synchronized
def get_adapter(use_http=False, working_directory=None) -> ISessionFactoryAdapter:

    if Aeon.adapter is not None:
        return Aeon.adapter

    if use_http:
        Aeon.adapter = HttpSessionFactoryAdapter()
    else:
        Aeon.adapter = JavaSessionFactoryAdapter(working_directory)

    return Aeon.adapter
