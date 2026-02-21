def assess_risk(speed, restricted_entry, altitude_change, speed_change):

    if not restricted_entry:
        return "LOW RISK"

    elif restricted_entry and speed < 100:
        return "POTENTIAL RISK"

    elif restricted_entry and speed >= 100 and altitude_change < 50:
        return "MEDIUM RISK"

    elif restricted_entry and speed_change > 100:
        return "HIGH RISK"

    else:
        return "MEDIUM RISK"
