import yaml
import sys
import os

def parser(parsed_commands):
    steps = parsed_commands['Steps']
    scheduler = parsed_commands['Scheduler']
    scheduler_pattern = scheduler['when']
    scheduler_target = scheduler['step_id_to_execute']
    return steps, scheduler_pattern, scheduler_target
