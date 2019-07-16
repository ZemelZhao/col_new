from configparser import ConfigParser
try:
	from .log import Log
except ImportError:
	from log import Log
import os
import sys

class ConfigProcess(object):
    """ DocString for ConfigProcess"""
    # config_ini()
    # config_read()
    # config_write()

    def __init__(self, conf_ini_path, conf_temp_path, log):
        #@todo: to be defined.
        self.conf_ini_path =  conf_ini_path
        self.conf_temp_path = conf_temp_path
        self.judge = True
        self.log = log

    def config_read_ini(self):
        """DocString for config_read"""
        #@todo: to be defined.
        parser = ConfigParser()
        self.judge = False
        parser.read(self.conf_ini_path)
        self.dict_section = dict(parser)
        list_dict_section = list(self.dict_section.keys())
        list_dict_section.remove('DEFAULT')
        self.dict_res = {}
        for i in list_dict_section:
            self.dict_res[i] = dict(self.dict_section[i])
        return self.dict_res

    def __config_write(self, cache_dict):
        """DocString for __config_write"""
        #@todo: to be defined.
        parser = ConfigParser()
        for i in cache_dict:
            parser.add_section(i)
            for j in cache_dict[i]:
                parser.set(i, j, str(cache_dict[i][j]))
        parser.write(open(self.conf_temp_path, 'w'))

    def __config_read(self):
        """DocString for __config_read"""
        #@todo: to be defined.
        if self.judge:
            self.dict_res = self.config_ini()
            self.judge = False
        else:
            parser = ConfigParser()
            parser.read(self.conf_temp_path)
            self.dict_section = dict(parser)
            list_dict_section = list(self.dict_section.keys())
            list_dict_section.remove('DEFAULT')
            self.dict_res = {}
            for i in list_dict_section:
                self.dict_res[i] = dict(self.dict_section[i])
        return self.dict_res


    def config_ini(self):
        """DocString for config_ini"""
        #@todo: to be defined.
        dict_conf = self.config_read_ini()
        self.__config_write(dict_conf)
        self.log.info(self, 'Initialize Config')
        return dict_conf

    def config_read(self):
        """DocString for config_read"""
        #@todo: to be defined.
        res_dict = self.__config_read()
        self.log.debug(self, 'Read Config')
        return res_dict

    def config_write(self, cache_dict):
        """DocString for config_write"""
        #@todo: to be defined.
        self.__config_write(cache_dict)
        self.log.info(self, 'Change Config')


if __name__ == '__main__':
    config_ini_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'config', 'config.ini')
    config_temp_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, '.temp', 'config.ini')
    log = Log(os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'log', 'log.out'))
    conread = ConfigProcess(config_ini_path, config_temp_path, log)
    data = conread.config_ini()
    data['Filter']['filter_notch'] = 60
    conread.config_write(data)
    data = conread.config_read()
    print(data)


