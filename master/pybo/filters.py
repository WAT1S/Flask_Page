def format_datetime(value, imt = "%Y-%m-%d %H:%M"):
    return value.strftime(imt)


def format_dateymdtime(value, imt = "%Y-%m-%d"):
    return value.strftime(imt)