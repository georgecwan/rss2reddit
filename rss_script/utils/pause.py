import time


# Inspiration: https://github.com/jgillick/python-pause/blob/master/pause/__init__.py
def until(timestamp) -> None:
    """
    Sleep until specified end time.

    Args:
        timestamp (int, float): Unix timestamp of when to wake up

    Returns:
        None
    """
    end = timestamp

    # Type check (int or float)
    if not isinstance(end, (int, float)):
        raise Exception('The timestamp parameter is not a number or datetime object')

    # Sleep in increments of no more than 1 hour. As the time gets closer, the increments get shorter in length
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
                print(f'[{t}] Sleeping for {round(diff / 120)} minutes...')
                time.sleep(diff / 2)
            else:               # <5 minutes left
                print(f'[{t}] Sleeping for {round(diff, 2)} seconds...')
                time.sleep(diff)
