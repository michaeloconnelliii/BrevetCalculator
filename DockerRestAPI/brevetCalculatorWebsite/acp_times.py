"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.

# Tables (lists) are based on ACP Brvet Control Times Calculator table: https://rusa.org/pages/acp-brevet-control-times-calculator
DISTANCES = [0, 200, 400, 600, 1000, 1300]
MIN_SPEED = [0, 15, 15, 15, 11.428, 13.333]
MAX_SPEED = [0, 34, 32, 30, 28, 26]

# Overall time limit for brevets according to offical ACP rules
RULES = { 200 : 13.5, 300 : 20.0, 400: 27.0, 600: 40.0, 1000: 75.0}

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    brevet_start_time = arrow.get(brevet_start_time, 'YYYY-MM-DD hh:mm')
    # Amount of time we will add to start time to calculate open time
    time_sum = 0
    # Algorithm
    for i in range(1, len(DISTANCES)):
        # Nothing left to calculate
        if control_dist_km <= 0:
            break
        else:
            if control_dist_km >= (DISTANCES[i] - DISTANCES[i - 1]):
                time_sum += ((DISTANCES[i] - DISTANCES[i - 1]) / MAX_SPEED[i])
            else:
                time_sum += (control_dist_km / MAX_SPEED[i])
            control_dist_km -= (DISTANCES[i] - DISTANCES[i - 1])
    # adjust the time using calculation results
    days = 0
    hours = 0
    minutes = 0
    if(time_sum >= 24):
        days = time_sum // 24
    # time_sum is in hours, integer division gets rid of decimal remainder (e.g. 2.23 // 1 = 2)
    # cast to int (whole number) for arrow's shift() function
    hours = (time_sum - (days * 24)) // 1
    hours = int(hours)
    minutes = round((time_sum - hours) * 60)
    minutes = int(minutes)

    # shifting start time based on calculations
    brevet_start_time = brevet_start_time.shift(days = days, hours = hours, minutes = minutes)

    # Converting brevet_start_time to iso format
    timezone = arrow.now().tzinfo # local timezone
    brevet_start_time = brevet_start_time.replace(tzinfo=timezone)
    brevet_start_time = brevet_start_time.isoformat()

    return brevet_start_time

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    brevet_start_time = arrow.get(brevet_start_time, 'YYYY-MM-DD hh:mm')

    # adjust the time using calculation results
    time_sum = 0

    # Special case: time limit for brevets according to offical rules
    if control_dist_km >= brevet_dist_km:
        if brevet_dist_km in RULES:
            time_sum = RULES[brevet_dist_km]
    # Special case: first 60 km
    elif control_dist_km <= 60:
        time_sum += (control_dist_km / 20) + 1
    else:
        # Algorithm
        # Amount of time we will add to start time to calculate open time
        for i in range(1, len(DISTANCES)):
            # Nothing left to calculate
            if control_dist_km <= 0:
                break
            else:
                if control_dist_km >= (DISTANCES[i] - DISTANCES[i - 1]):
                    time_sum += ((DISTANCES[i] - DISTANCES[i - 1]) / MIN_SPEED[i])
                else:
                    time_sum += (control_dist_km / MIN_SPEED[i])
                control_dist_km -= (DISTANCES[i] - DISTANCES[i - 1])

    days = 0
    hours = 0
    minutes = 0

    if(time_sum >= 24):
        days = time_sum // 24

    # time_sum is in hours, integer division gets rid of decimal remainder (e.g. 2.23 // 1 = 2)
    # cast to int (whole number) for arrow's shift() function
    hours = (time_sum - (days * 24)) // 1
    hours = int(hours)
    minutes = round((time_sum - hours) * 60)
    minutes = int(minutes)

    # shifting start time based on calculations
    brevet_start_time = brevet_start_time.shift(days = days, hours = hours, minutes = minutes)

    # Converting brevet_start_time to iso format
    timezone = arrow.now().tzinfo # local timezone
    brevet_start_time = brevet_start_time.replace(tzinfo=timezone)
    brevet_start_time = brevet_start_time.isoformat()

    return brevet_start_time
