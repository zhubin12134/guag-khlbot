import os
import time



class Logger:
    """
    # 示例用法
    log = Logger()
    log.debug("This is a debug message.")
    log.info("This is a info message.")
    """

    STATU_LIST = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


    def __init__(self, debug_mode: bool = False) -> None:
        self.debug_mode = self.setDebugMode(debug_mode)
        self.file = self.getFile()


    def setDebugMode(self, debug_mode: bool) -> None:
        self.debug_mode = debug_mode

    def getFile(self):
        if not os.path.exists("log"):
            os.mkdir("log")
        return open("log/log.txt", mode="a+", encoding="utf-8", newline="")


    def log(self, status: str, info: any, *args) -> None:

        now = time.time()  # 获取当前时间
        formatted_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(now))  # 格式化时间

        msg = f"[{formatted_time}] [{status.upper()}] {info} {' '.join(args)}"


        if self.debug_mode:  # 开启debug，打印所有日志
            print(msg)
        else:
            if status != "DEBUG":   # 否则DEBUG级别日志不打印
                print(msg)
                self.file.write(msg + "\n")
                self.file.flush()
        return

    
    def __getattr__(self, name):
        """
        param name: 属性名
        return: 一个函数,
        通过类属性调用,返回一个函数,
        """
        if name.upper() in self.STATU_LIST:
            return lambda message, *args: self.log(name.upper(), message, *args)
        raise AttributeError(f"'Logger' object has no attribute '{name}'")


    def close(self):
        self.file.close()

    __del__ = close

    

log = Logger()


if __name__ == '__main__':
    log = Logger()
    log.debug("This is a debug message.")
    log.info("This is a info message.")
    log.setDebugMode(True)
    log.debug("This is a debug message.")
    log.info("This is a info message.")
    del log
    