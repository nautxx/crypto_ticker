class MessageBar:

    def __init__(self):
        pass

    def logger(self):
        path = Path(__file__).parent.absolute()
        file = open(str(path) + "/message_log.txt", "a")
        file.write("\n" + get_current_timestamp() + "_" + function + ": " + message)
        file.close