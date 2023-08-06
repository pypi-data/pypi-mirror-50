
class logger(object):

    # level
    RAW = 0
    INFO = 1
    WARN = 2
    ERROR = 3

    # level color
    LEVEL_COLORS = {RAW: "%s", \
        INFO: "\033[1;34m%s\033[0m", \
        WARN: "\033[1;33m%s\033[0m", \
        ERROR: "\033[1;31m%s\033[0m"}

    # promote text 
    PROM_COLOR = "\033[1;35m%s\033[0m"
    PROM_T = {RAW: PROM_COLOR % "**** ", \
        INFO: LEVEL_COLORS[INFO]  % "INFO ", \
        WARN: LEVEL_COLORS[WARN]  % "WARN ", \
        ERROR: LEVEL_COLORS[ERROR]  % "ERROR"}

    def __init__(self):
        pass


def log(level, msg, *args, **kwargs):
    msg_ = msg + ' ' + ' '.join([str(x) for x in args])
    print('[' + logger.PROM_T[level] + ']', \
        logger.LEVEL_COLORS[level] % msg_)