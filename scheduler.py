import schedule

def set_scheduler(schedule_pattern, run_step=None):
    crons = schedule_pattern.split()
    minutes = 0
    hours = 0
    weekday = None
    is_minute_only = True
    if crons[0] != '*':
        minutes = int(crons[0])
    if crons[1] != '*':
        hours = int(crons[1])
        is_minute_only = False
    if crons[2] != '*':
        weekday = int(crons[2])
        is_minute_only = False

    if is_minute_only:
        schedule.every(minutes).minutes.do(run_step)
    elif weekday == None:
        formatted_time = '{0:02d}:{1:02d}'.format(hours, minutes)
        schedule.every().day.at(formatted_time).do(run_step)
    else:
        weekday_print = map_day_to_weekday(weekday)
        formatted_time = '{0:02d}:{1:02d}'.format(hours, minutes)
        if weekday_print == 'sunday':
            schedule.every().sunday.at(formatted_time).do(run_step)
        elif weekday_print == 'monday':
            schedule.every().monday.at(formatted_time).do(run_step)
        elif weekday_print == 'tuesday':
            schedule.every().tuesday.at(formatted_time).do(run_step)
        elif weekday_print == 'wednesday':
            schedule.every().wednesday.at(formatted_time).do(run_step)
        elif weekday_print == 'thursday':
            schedule.every().thursday.at(formatted_time).do(run_step)
        elif weekday_print == 'friday':
            schedule.every().friday.at(formatted_time).do(run_step)
        elif weekday_print == 'saturday':
            schedule.every().saturday.at(formatted_time).do(run_step)
        else:
            raise ValueError('input day is not valid')

def map_day_to_weekday(day):
    if day == 0:
        return 'sunday'
    elif day == 1:
        return 'monday'
    elif day == 2:
        return 'tuesday'
    elif day == 3:
        return 'wednesday'
    elif day == 4:
        return 'thursday'
    elif day == 5:
        return 'friday'
    elif day == 6:
        return 'saturday'
    else:
        raise ValueError('input day is not valid')

def test_print():
    print ("test_print....")

#set_scheduler('5 * *', test_print)
#set_scheduler('* 2 *', test_print)
#set_scheduler('* * 1', test_print)
#set_scheduler('10 23 *', test_print)
#set_scheduler('* 2 *', test_print)
#set_scheduler('5 * 1', test_print)