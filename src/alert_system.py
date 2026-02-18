def issue_alert(risk_level):

    if risk_level == "HIGH RISK":
        return "Evacuate Zone", "Notify Authority", "Activate Surveillance", "Predict Actions", "Notify medical assistance", "Notify defence sectors/systems"     #possible safe actions on high risk without dangerous actions or engaging or intercepting

    elif risk_level == "MEDIUM RISK":
        return "Restrict Airspace", "Increase Surveillance"

    elif risk_level == "POTENTIAL RISK":
        return "Monitor Continuously"

    else:
        return "Normal Monitoring"
