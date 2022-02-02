from time import strftime, gmtime, timezone


def getManyOrNone(manyToMany):
    return None if manyToMany is None else manyToMany.all()


def validateIntervalOrNone(dataDict, key, interval):
    value = dataDict.get(key)
    minVal, maxVal = interval
    if value is not None and not (minVal <= value <= maxVal):
        errorMessage = 'The %s must be in [%s, %s] or None' % (key, minVal, maxVal)
        raise Exception(errorMessage)


def getTimeString(utcTimeValue):

    if utcTimeValue is None:
        return None

    if utcTimeValue.tzinfo is not None:
        utcTimeValue = utcTimeValue.astimezone(utcTimeValue.tzinfo)
    return utcTimeValue.strftime('%Y-%m-%d %H:%M:%S.%f')
