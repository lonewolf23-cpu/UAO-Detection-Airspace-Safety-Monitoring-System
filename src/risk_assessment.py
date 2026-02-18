def assess_risk(speed, speed_change, restricted_entry, altitude_change, speed_change):

    if restricted_entry and speed > 150 and altitude_change > 50:  #Restricted + High Speed + Altitude Change[low/high]
        return "HIGH RISK"

    elif restricted_entry and speed_change > 100: #restricted + speed change here
        return "MEDIUM RISK"

    elif speed_change > 50:   #only speed change
        return "POTENTIAL RISK"

    else:
        return "LOW RISK"
