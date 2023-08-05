

def td_format(td_object):
    """
    based on https://stackoverflow.com/a/13756038
    """
    seconds = int(td_object.total_seconds())
    periods = [
        ('an',       60*60*24*365),
        ('mois',        60*60*24*30),
        ('semaine',     60*60*24*7),
        ('jour',        60*60*24),
        ('heure',       60*60),
        ('minute',      60),
        ('seconde',     1)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 and period_name != "mois" else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)
