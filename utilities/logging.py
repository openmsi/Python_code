#imports
import logging, pathlib

class Logger :
    """
    Class for a general logger. Logs messages and raises exceptions
    """

    def __init__(self,name=None) :
        """
        name = the name for this logger to use (probably something like the top module that owns it)
        """
        self._name = name
        if self._name is None :
            self._name = pathlib.Path(__file__).name.split('.')[0]
        self._logger_obj = logging.getLogger(self._name)
        self._logger_obj.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('[%(name)s at %(asctime)s] %(message)s','%Y-%m-%d %H:%M:%S'))
        self._logger_obj.addHandler(handler)

    #functions for logging different levels of messages
    
    def info(self,msg) :
        self._logger_obj.info(msg)
    
    def warning(self,msg) :
        if not msg.startswith('WARNING:') :
            msg = f'WARNING: {msg}'
        self._logger_obj.warning(msg)

    #function to log an error message and optionally raise an exception with the same message

    def error(self,msg,exception_type=None) :
        if not msg.startswith('ERROR:') :
            msg = f'ERROR: {msg}'
        self._logger_obj.error(msg)
        if exception_type is not None :
            raise exception_type(msg)

