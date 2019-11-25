class Time:
    @staticmethod
    def format_seconds(seconds):
        try:
            return str(format(float(seconds), '.2f'))
        except:
            return seconds
