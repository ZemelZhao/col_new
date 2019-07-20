import numpy as np
import os
import matplotlib.pyplot as plt
from base.log import Log
from base.conf import ConfigProcess
from cal.save import Save



if __name__ == '__main__':
    config_ini_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'config', 'config.ini')
    config_temp_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '.temp', 'config.ini')
    log = Log(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'log', 'log.out'))
    conf = ConfigProcess(config_ini_path, config_temp_path, log)

    dp = Save(conf, log, 1, 0)
    with open('temp.dat', 'rb') as f:
        data = f.read()
    dp.run(data)
