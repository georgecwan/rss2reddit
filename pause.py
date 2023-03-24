import time


# https://github.com/jgillick/python-pause/blob/master/pause/__init__.py
def until(timestamp):
    """
    Pause your program until a specific end time.
    'time' is either a valid datetime object or unix timestamp in seconds (i.e. seconds since Unix epoch)
    """
    end = timestamp

    # Type check
    if not isinstance(end, (int, float)):
        raise Exception('The timestamp parameter is not a number or datetime object')

    # Now we wait
    while True:
        now = time.time()
        diff = end - now

        # Time is up!
        if diff <= 0:
            break
        else:
            t = time.strftime('%Y-%m-%d %H:%M')
            if diff > 7200:     # >2 hours left
                print(f'[{t}] Sleeping for 1 hour...')
                time.sleep(3600)
            elif diff > 300:    # >5 minutes left
                print(f'[{t}] Sleeping for {round(diff / 120, 2)} minutes...')
                time.sleep(diff / 2)
            else:               # <5 minutes left
                print(f'[{t}] Sleeping for {round(diff, 2)} seconds...')
                time.sleep(diff)
