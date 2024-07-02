# elevator_simulation
**Elevator Simulation Exercise implemented with Python 3.8**

Required Inputs:
---
- start_floor: integer value where the elevator is located at the start of the simulation
- floors: list of integers of which floors at which to stop

Optional Inputs:
---
- optimize mode: 
    - flag to execute the floor stops with less overall travel time 
    - default is to execute the floor stops in the order listed
- top_floor: highest floor input allowed (default is no limit)
- bottom_floor: lowest floor input allowed (default is no limit)
- time_between_floors: time in seconds to travel between each floor (default = 10 seconds)
- floor stop: time in seconds stopped at the floor to allow passengers to embark / depart (default = 0 seconds)

Output: 
---
- Total runtime of the elevator
- Ordered Path of floors visited

Execution:
---
`python src/elevator.py --start_floor=12 --floors=2,9,1,32`

Execute Test Functions with Verbose Output:
---
`python -m unittest test.test_elevator -v`

Assumptions:
---
- Invalid input values are logged and ignored
- Ground floor is at position 0
- Negative values are valid and represent basement level floors below ground level
- No valid inputs received results in an output of 0 seconds and no floors traveled
- If top floor is not determined, there is no maximum; likewise, if the bottom floor is not determined, there is no minimum
- Floor stop time default is currently set to 0, which is non-realitisic, but fits with the examples provided
- If included, the floor stop time is at every floor, including the starting and ending floors
- Duplicate floors when executing under exact path mode are included and ignored for optimized path mode

Features Not Implemented:
---
- Interactive mode of continuing to prompt for additional floors/paths
- Implementation of local minima for path segments within larger defined pathway
- Forced directionality (if someone gets on the elevator going down, don't change direction until desired floor reached)
- Monitoring for maximum capacity
- Typer implementation for direct function execution from command line, would require input cleansing to be abstracted from argsparser 
- Limit function scope
- Write logging to external file