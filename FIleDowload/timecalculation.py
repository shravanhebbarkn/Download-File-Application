import math


def file_size(total_length):
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(total_length, 1024)))
    p = math.pow(1024, i)
    s = round(total_length / p, 2)
    name = size_name[i]
    return s,name


def download_time(file_size, file_units, bandwidth, bandwidth_units):
    file_size = convert_bits(file_size, file_units)
    bandwidth = convert_bits(bandwidth, bandwidth_units)

    time_taken = file_size / bandwidth
    return convert_seconds(time_taken)


def convert_bits(size, units):
    kilobits = float(size)

    if units == 'kb':
        return kilobits
    elif units == 'kB':
        return kilobits * 8
    elif units == 'MB':
        return kilobits * (2 ** 10) * 8
    elif units == 'Mb':
        return kilobits * (2 ** 10)
    elif units == 'GB':
        return kilobits * (2 ** 20) * 8
    elif units == 'Gb':
        return kilobits * (2 ** 20)
    elif units == 'TB':
        return kilobits * (2 ** 30) * 8
    elif units == 'Tb':
        return kilobits * (2 ** 30)
    else:
        return 0.0


def convert_seconds(sec):
    hour_string, minute_string, second_string = "hour", "minute", "second"
    hour, minute, second = int(sec / 3600), int((sec / 60) % 60), sec % 60

    if hour != 1:
        hour_string = hour_string + 's'
    if minute != 1:
        minute_string = minute_string + 's'
    if second != 1:
        second_string = second_string + 's'

    return ("{0} {1}, {2} {3}, {4} {5}").format(hour, hour_string, minute, minute_string, second, second_string)
