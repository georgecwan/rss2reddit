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
            # 'logarithmic' sleeping to minimize loop iterations
            if diff > 300:
                t = time.strftime('%Y-%m-%d %H:%M')
                if diff > 7200:
                    print(f'[{t}] Sleeping for {round(diff/7200, 2)} hours...')
                elif diff > 120:
                    print(f'[{t}] Sleeping for {round(diff/120, 2)} minutes...')
                else:
                    print(f'[{t}] Sleeping for {round(diff/2, 2)} seconds...')
            time.sleep(diff / 2)
