import time

timeMults = {"h": 3600, "m": 60, "s":1}

def parseTimeString(string):
    backLetter = string[-1]
    #Checking if this is a letter based format like 5m or 3s.
    if backLetter in timeMults:
        return int(string[:-1]) * timeMults[backLetter]
    
    #It might be a HH:MM:SS format, try the built in parser
    timeFormat = None
    try:
        timeFormat = time.strptime(string, "%H:%S:%M")

        return timeFormat.tm_hour * 3600 + timeFormat.tm_min * 60 + timeFormat.tm_sec
    except(ValueError):
        pass
    #No luck, try MM:SS
    try:
        timeFormat = time.strptime(string, "%S:%M")
        return timeFormat.tm_min * 60 + timeFormat.tm_sec
    except(ValueError):
        pass
    #Still nothing, try single seconds
    try:
        return int(string)
    except(ValueError):
        pass

    return -1

