class MessageBar:

    def __init__(self):
        pass

    def logger(self, timestamp, message, function):
        """
        Input timestamp, message, and function. Stores messages sent in message_log.txt. Stores both the function used and the message sent.
        """
        with open("message_log.txt", mode="a") as file:
            file.write(f"\n" + timestamp + "_" + function + ": " + message)