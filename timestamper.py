import time

def datetime_to_timestamp(datetimeObj):
    seconds_since_epoch = time.mktime(datetimeObj.timetuple()) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))
    return int(seconds_since_epoch)
