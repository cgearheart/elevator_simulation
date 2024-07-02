import argparse
from typing import List
import sys
import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger('elevator')


def valid_int(value: str):
    """Validate if value is an integer"""
    try:
        return int(value)
    except:
        return False


def list_int(
    values: List[int]
):
    """Split floors list and only keep integer values"""
    values_list = values.split(',')
    # include only integers
    floors = [ int(x) for x in values_list if valid_int(x)]
    # notify if any ignored input values
    ignored = [ x for x in values_list if not valid_int(x)]
    if len(ignored) > 0:
        log.info(f"inputs ignored: {ignored}")
    return floors


def positive_float(
    value: str     
):
    """Validate times are positive numbers"""
    try:
        value = float(value)
        if value <= 0:
            log.error(f"{value} is not a positive value")
            raise argparse.ArgumentTypeError()
    except ValueError:
        log.exception(f"{value} is not a valid number")
        raise Exception() 
    return value


def remove_out_of_range(
    start_floor: int,
    floors: List[int],
    top_floor: int = None,
    bottom_floor: int = None
):
    """Remove any floors from list of stops that are greater than the top floor indicated"""
    if top_floor is not None and start_floor > top_floor:
        log.error(f"Top floor ({top_floor}) must be greater than or equal to the starting floor ({start_floor})")
        raise ValueError
    if bottom_floor is not None and start_floor < bottom_floor:
        log.error(f"Bottom floor ({bottom_floor}) must be less than or equal to the starting floor ({start_floor})")
        raise ValueError
    if top_floor < bottom_floor:
        log.error(f"Bottom floor ({bottom_floor}) must be less than the top floor ({top_floor})")
        raise ValueError
    out_of_range = [ x for x in floors if (top_floor is not None and x > top_floor) or (bottom_floor is not None and x < bottom_floor)]
    if len(out_of_range) > 0: 
        log.info(f"ignored out of range floors: {out_of_range}")
    in_range = [ x for x in floors if (top_floor is None or x < top_floor) and (bottom_floor is None or x > bottom_floor)]
    return in_range


def calc_travel_time(
    curr_floor: int,
    dest_floor: int,
    time_between_floors: float
):
    """Determine travel time between current floor and destination floor"""
    return abs(dest_floor - curr_floor)*time_between_floors


def calc_time_at_floor(
    floors: List[int],
    time_at_floor: float      
):
    """Determine amount of time spent waiting at the floor stops"""
    return len(floors)*time_at_floor


def operate_elevator(
    start_floor: int,
    floors: List[int],
    optimize: bool = False,
    time_between_floors: float = 10, 
    time_at_floor: float = 0, 
    top_floor: int = None,
    bottom_floor: int = None
):
    """Operate the elevator"""
    # filter floors list if top or bottom floor declared
    if top_floor is not None or bottom_floor is not None:
        floors = remove_out_of_range(start_floor=start_floor, floors=floors, top_floor=top_floor, bottom_floor=bottom_floor)
    # calculate optimized path if selected
    if optimize is True:
        floors = optimize_path(start_floor=start_floor, floors=floors)
    # add starting point to start of path
    floors.insert(0,start_floor)
    # time spent waiting at each floor
    time_waiting = calc_time_at_floor(floors=floors, time_at_floor=time_at_floor)
    # time spent traveling between the floors listed in the path
    travel_times = [calc_travel_time(curr_floor=i, dest_floor=j, time_between_floors=time_between_floors) for i, j in zip(floors[:-1], floors[1:])]
    total_travel_time = sum(travel_times) + time_waiting
    return total_travel_time, floors


def optimize_path(
    start_floor: int,
    floors: List[int],
):
    """Optimize the travel path to minimize the travel time between floors"""
    # get unique floor values
    floors = list(set(floors))
    # segment search space based on start floor location
    lower_floors = [ x for x in floors if x < start_floor]
    lower_floors.sort()
    upper_floors = [ x for x in floors if x > start_floor]
    upper_floors.sort()
    # determine if shorter to travel up or down first
    max_path_lower = start_floor - lower_floors[0] if len(lower_floors)>0 else 0
    max_path_upper = upper_floors[-1] - start_floor if len(upper_floors)>0 else 0
    # build path
    # all floors are above the starting floor
    if max_path_lower == 0:
        path = upper_floors
    # all floors are below the starting floor, reverse order and travel downward
    elif max_path_upper == 0:
        lower_floors.sort(reverse=True)
        path = lower_floors
    # traversing lower floors are shorter, iterate first
    elif max_path_lower <= max_path_upper:
        path = lower_floors
        path.extend(upper_floors)
    # traversing upper floors is shorter, iterate first
    else:
        path = upper_floors
        path.extend(lower_floors)
    return path


if __name__ == "__main__":
    # turn off stack trace printing
    sys.tracebacklimit = 0

    parser = argparse.ArgumentParser("elevator_simulation", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--start_floor', help="non-negative integer value where the elevator is located at the start of the simulation", type=int, required=True) 
    parser.add_argument('-f', '--floors', help="comma separated list of integers of which floors at which to stop", type=list_int, required=True)
    parser.add_argument('-t', '--time_between_floors', help="time in seconds to travel between each floor", type=positive_float, default=10)
    parser.add_argument('-w', '--time_at_floor', help="time in seconds to waiting at each floor", type=positive_float, default=0)
    parser.add_argument('-m', '--top_floor', help="maximum floor in the building", type=int, default=None)
    parser.add_argument('-b', '--bottom_floor', help="minimum floor in the building", type=int, default=None)
    parser.add_argument('-o', '--optimize', help="flag to optimize the traveled path", action='store_true', default=False)

    args = parser.parse_args()
    
    travel_time, path = operate_elevator(start_floor=args.start_floor, 
                                         floors=args.floors, 
                                         optimize=args.optimize, 
                                         time_between_floors=args.time_between_floors,
                                         time_at_floor=args.time_at_floor,
                                         top_floor=args.top_floor,
                                         bottom_floor=args.bottom_floor)
    
    print(f"{travel_time} {path}")
