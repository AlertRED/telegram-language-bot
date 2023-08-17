class ExcludeLevelsFilter(object):
    def __init__(self, skip_levels: list):
        self.skip_levels: set = set(skip_levels)

    def filter(self, record):
        return self.getLogLevelName(record.levelno) not in self.skip_levels

    def getLogLevelName(self, levelno):
        switcher = {
            10: "DEBUG",
            20: "INFO",
            30: "WARNING",
            40: "ERROR",
            50: "CRITICAL"
        }
        return switcher.get(levelno, "INVALID")
