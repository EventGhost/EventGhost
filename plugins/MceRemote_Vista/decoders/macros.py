# This file contains macros that are used across all of the various protocols
# These macros normalize the timings for an IR protocol.

# these 2 constants are used to calculate the high and low of a single
# timing value. other IR libraries use a +-25% tolerance.. I feel this
# tolerance is way to large. Most IR receivers are "tuned" to an ideal
# frequency and if a signal comes in outside of that range is received
# the closer to the boundaries of the max and min frequencies the receiver
# is able to read the more signal dedrigation occurs..
# if this value is set to 25% it is going to effect frequencies that are
# in the "sweet spot" in a negitive manner. If some stray data or corrupted
# data is received the code will then get decoded improperly. We want to avoid
# this issue. The most popular protocols use frequencies that are in this sweet
# spot. so we want to favor these protocols. This threshold can be adjusted
# realtime so they can be changed via a setting inside of an application
# and would not require a restart of the application.
#
TIMING_TOLERANCE = 10.0

import math


# some protocols use to low of a mark and space to properly calculate
# if it is within the allowed tolerance they can be incorrectly identified.
def PAIR_MATCH(mark, space, expected_mark, expected_space, raw=True):
    # raw timings have a positive mark and a negitive space.
    if raw and (space > 0 or mark < 0):
        return False
    elif not raw and (space < 0 or mark < 0):
        return False

    space = abs(space)
    expected_space = abs(expected_space)

    expected_pair = expected_mark + expected_space
    pair = mark + space

    high = math.floor(expected_pair + ((expected_pair * TIMING_TOLERANCE) / 100.0))
    low = math.floor(expected_pair - ((expected_pair * TIMING_TOLERANCE) / 100.0))
    return low <= pair <= high
