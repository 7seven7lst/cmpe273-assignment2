import yaml
import sys
import os
import schedule
import time
from parser import parser
from scheduler import set_scheduler
from step_executer import invoke_step

if len(sys.argv) != 2:
    print("Must have a file input as an argument!")
    os.exit(1)

input_file = sys.argv[1]
with open(input_file) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    parsed_commands = yaml.load(file, Loader=yaml.FullLoader)
    steps, scheduler_pattern, scheduler_target = parser(parsed_commands)
    scheduler_target = int(scheduler_target[0])
    def wrapper():
        return invoke_step(scheduler_target, None, steps)
    
    set_scheduler(scheduler_pattern, wrapper)

    while True:
        schedule.run_pending()
        time.sleep(1)