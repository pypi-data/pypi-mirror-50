class LowVerbosityLogger(object):

    @staticmethod
    def debug(msg) -> None:
        pass

    @staticmethod
    def warning(msg) -> None:
        pass

    @staticmethod
    def error(msg) -> None:
        print(msg)


class MediumVerbosityLogger(LowVerbosityLogger):

    @staticmethod
    def warning(msg) -> None:
        print(msg)


class HighVerbosityLogger(MediumVerbosityLogger):

    @staticmethod
    def debug(msg) -> None:
        print(msg)
