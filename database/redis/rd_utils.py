# ------------------------------------------------
#    External imports
# ------------------------------------------------
import redis
from redis import ResponseError, ConnectionError

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------
import logging

# ------------------------------------------------
#    Module Imports
# ------------------------------------------------
from errors.v1.handlers import DataAccessError
from config.v1.app_config import REDIS


# ------------------------------------------------
#    Redis Class
# ------------------------------------------------

class RedisConnect(object):
    """
        Connects to our Redis database

    :return:
    """
    def __init__(self):
        self.connect_data = REDIS
        try:
            self.connection = redis.Redis(REDIS['host'], REDIS['port'], REDIS['db'], REDIS['password'])
            self.check_connection()

        except redis.AuthenticationError:
            # We could use an HTTP error status code of 500 or 503
            raise DataAccessError(message="Redis Authentication Error", status_code=503)

    def check_connection(self):
        try:
            self.connection.randomkey()
            logging.info("Connected to Redis[db:%s] on %s:%s" % (self.connect_data['db'], self.connect_data['host'], self.connect_data['port']), exc_info=False)
        except ConnectionError as e:
            logging.error("Cannot connect to Redis[db:%s] on %s:%s" % (self.connect_data['db'], self.connect_data['host'], self.connect_data['port']), exc_info=False)

    def bgsave(self):
        """
            Asynchronously save the Redis db on disk
            In the case of an error during saving - Do not cause an exception - just log
        """
        if self.connection.bgsave():
            logging.info("Redis[db:%s] saved successfully" % self.connect_data['db'], exc_info=False)
        else:
            logging.error("Redis[db:%s] was NOT saved successfully" % self.connect_data['db'], exc_info=True)

    def set(self, k):
        """
            Save a Key/Value pair to the Redis cache
        :return:
        """

        try:
            self.connection.set(k, 1)
            self.bgsave()
        except ResponseError as e:
            logging.error("Redis did not save the key %s" % k, exc_info=True)

    def get(self, k):
        """
            Return a Key/Value pair to the Redis cache where the k is a name
        :
        :return:
        """
        try:
            return self.connection.get(k)
        except Exception:
            raise DataAccessError(message="Redis was unable to retrieve the key %s" % k, status_code=503)


# This is a pointer to the class RedisConnect above and can be imported by modules
# using - from database.redis.rd_utils import redis_connection
redis_connection = RedisConnect()


# Test code - will move to tests - later
# robj = redis_connection
#
# robj.set('erewtwertvwert3454756hgu46756h7567h65nbvg45645')
# print(robj.get('1'))

