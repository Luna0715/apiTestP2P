import  logging
import time
from logging import handlers
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'http://121.43.169.97:8081'
DB_URL = '121.43.169.97'
DB_USERNAME = 'student'
DB_PASSWORD = 'P2P_student_2022'
DB_MEMBER = 'czbk_member'
DB_FINANCE = 'czbk_finance'

#初始化日志配置
def init_log_config():
    #初始化日志对象
    logger = logging.getLogger()
    #设置日志级别
    logger.setLevel(logging.INFO)
    #创建控制台处理器和文件处理器
    sh = logging.StreamHandler()

    lofile = BASE_DIR + os.sep + "log" + os.sep +"log{}.log".format(time.strftime("%Y%m%d-%H%M%S"))
    fh = logging.handlers.TimedRotatingFileHandler(lofile,when='M',interval=5,backupCount=5,encoding='UTF-8')
    #设置日志格式，创建格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    # 将格式化器设置到日志器中
    formatter = logging.Formatter(fmt)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 将日志处理器添加到日志对象
    logger.addHandler(sh)
    logger.addHandler(fh)










