def time_subtraction(first, second):
    #Second-minus-First
    [first_hours,  first_minutes,  first_seconds] = first.split(':')
    [second_hours,  second_minutes,  second_seconds] = second.split(':')
    first_hours = int(first_hours)
    second_hours = int(second_hours)
    first_minutes = int(first_minutes)
    second_minutes = int(second_minutes)
    first_seconds = float(first_seconds)
    second_seconds = float(second_seconds)
    
    if second_seconds >= first_seconds:
        result_seconds = second_seconds - first_seconds
    else:
        second_minutes = second_minutes - 1
        second_seconds = second_seconds + 60
        result_seconds = second_seconds - first_seconds
    
    if second_minutes >= first_minutes:
        result_minutes = second_minutes - first_minutes
    else:
        second_hours = second_hours - 1
        second_minutes = second_minutes + 60
        result_minutes = second_minutes - first_minutes
    
    result_hours = second_hours - first_hours
    
    result_hours = str(result_hours).zfill(2)
    result_minutes = str(result_minutes).zfill(2)
    result_seconds = str("%0.3f" % result_seconds).zfill(6)
    
    result = "%s:%s:%s" % (result_hours, result_minutes, result_seconds)
    
    return result