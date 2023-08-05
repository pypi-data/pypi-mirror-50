import os
import copy
import json

from pprint import pprint
from configparser import ConfigParser

print = pprint

CONFIG_NAME = "config.cfg"
CONFIG_PATH = os.path.join(
        os.path.dirname(
                os.path.dirname(__file__)), 
        "config",
        CONFIG_NAME
    )

parser = ConfigParser()
parser.read(CONFIG_PATH, encoding="utf-8")


class WebConfig:
    """服务相关配置
    """
    SECTION = "web"

    debug = parser.getboolean(SECTION, "debug")
    host = parser.get(SECTION, "host")
    port = parser.getint(SECTION, "port")
    threaded = parser.getboolean(SECTION, "threaded")
    expire = eval(parser.get(SECTION, "expire"))
    secret = parser.get(SECTION, "secret")
    hour = parser.get(SECTION, "hour")
    minute = parser.get(SECTION, "minute")


class LogConfig:
    """日志相关配置
    """
    SECTION = "log"

    console_level = parser.get(SECTION, "console_level")
    file_level = parser.get(SECTION, "file_level")
    max_bytes = parser.get(SECTION, "max_bytes")
    max_bytes = eval(max_bytes)
    backup_count = parser.getint(SECTION, "backup_count")
    formatter = parser.get(SECTION, "formatter")


class DBConfig:
    """数据库配置
    """
    SECTION = ""

    def __init__(self):
        self.host = parser.get(self.SECTION, "host")
        self.port = parser.getint(self.SECTION, "port")
        dbs  = parser.get(self.SECTION, "dbs")
        self.dbs = self.parse_dbs(dbs)
        self.user = parser.get(self.SECTION, "user")
        passwd = parser.get(self.SECTION, "passwd")
        self.passwd = self.parse_passwd(passwd)
        self.charset = parser.get(self.SECTION, "charset")

    def parse_dbs(self, dbs):
        return json.loads(dbs)

    def parse_passwd(self, passwd):
        if passwd.lower() == "none":
            return None
        return passwd

    def __call__(self):
        config = {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "passwd": self.passwd,
            "charset": self.charset,
        }
        configs = []
        for db in self.dbs:
            _config = config.copy()
            _config.update(db=db)
            configs.append(_config)
        return configs


class DevDBConfig(DBConfig):
    SECTION = "dev-mysql"


class ProductDBConfig(DBConfig):
    SECTION = "product-mysql"


class TestDBConfig(DBConfig):
    SECTION = "test-mysql"


db_config = {
    "dev": DevDBConfig,
    "product": ProductDBConfig,
    "test": ProductDBConfig,
    "default": DevDBConfig, 
}


opt = parser.get("env", "option")
cur_db_configs = db_config[opt]()()


sql_dict = {
    "db1": {
        "name1": "sql_statement1",
        
    },

    "db2": {
         "name2": "sql_statement2",
        
    },

    "db3": {
        "name3": "sql_statement3",

    }
}
