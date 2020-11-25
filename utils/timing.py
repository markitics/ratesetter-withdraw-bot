

def as_duration(d, show_s_for_seconds = True, decimal_place_after_seconds = 0, show_all_hhmmss_regardless = False, colon_breakers = True):
    """
        input d is number of seconds (NOT a datetime.timedelta object)
    """
    # copied from audiotracks/models.py where I made this there
    if not colon_breakers:
        show_s_for_seconds = False; 
        # so that we don't wind up with "2 mins, 45 secss"
    if d and d > 0.0:
        if d > 3599 or show_all_hhmmss_regardless:
            hours = d / 3600
            remaining = d % 3600
            minutes = remaining / 60
            seconds = remaining % 60
            if show_all_hhmmss_regardless:
                # need everything to two digits for html input type=time
                if colon_breakers:
                    string_returned = '%02d:%02d:%02d' % (hours, minutes, seconds)    
                else:
                    # string_returned = u'%02d hours, %02d mins, %02d secs' % (hours, minutes, seconds)    
                    # Use prime and double prime for mins and secs: 2h 03′ 04″
                    # https://en.wikipedia.org/wiki/Prime_(symbol)
                    # string_returned = u'%02dh %02d\′ %02d\″' % (hours, minutes, seconds)  # fails encoding
                    string_returned = '%02dh %02d\u2032 %02d\u2033' % (hours, minutes, seconds)    
            else:
                #don't force leading zero on hours
                if colon_breakers:
                    string_returned = '%d:%02d:%02d' % (hours, minutes, seconds)
                else:
                    # string_returned = u'%d hours, %02d mins, %02d secs' % (hours, minutes, seconds)
                    string_returned = '%dh %02d\u2032 %02d\u2033' % (hours, minutes, seconds)
        elif d > 59:
            # hours = 0
            minutes = d / 60
            seconds = d % 60
            if colon_breakers:
                string_returned = '%d:%02d' % (minutes, seconds)
            else:
                string_returned = '%d′ %02d″' % (minutes, seconds)
        else:
            seconds = d
            if colon_breakers:
                string_returned = '%02d' % (seconds)
            else:
                string_returned = '%02d seconds' % (seconds)
        # now add .ms if appropriate:
        if decimal_place_after_seconds:
            # first, since |decimal_place_after_seconds:"3" is the only argument passed into filter,
            # force show_s_for_seconds to be off
            # show_s_for_seconds = False
            # todo: don't make this hard-coded
            # reason I'm doing it is it's simplest to just pass one argument in custom filter
            # note: there is a way if I pass in all arguments as one string and then split them here
            # Alternatively, split out separate function as below
            # 
            # Now on to the decimal
            # from math import modf
            # ms,s = modf(d)
            # string_returned += u'.%d' % (ms)
            string_returned += "." + ('%s' % (d + 0.0)).split('.')[1][:decimal_place_after_seconds]
            # seconds += ms
            # we want decimal point returned in seconds value
        else:
            pass
            # that's fine, seconds is already to nearest integer
        # finally add "s" is value is less than one minute:
        if show_s_for_seconds and d < 60.0:  
            string_returned += 's'
        return string_returned
    else:
        return '0:00' # formerly N/A, but this displays if we never started listening to a track,
        # see "continue listening from ___ in /listen homepage.
# tests
# as_duration(3.4, show_s_for_seconds = True, decimal_place_after_seconds = 0)
# as_duration(3.4, show_s_for_seconds = True, decimal_place_after_seconds = 2) # check for over-write of show_s
# as_duration(3.123456789, show_s_for_seconds = False, decimal_place_after_seconds = 3)

