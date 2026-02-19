def issue_alert(risk_level):

    if risk_level == "HIGH RISK":                 #possible safe actions on high risk without dangerous actions or engaging or intercepting
        return (
            "Evacuate Zone",
            "Notify Authority",
            "Activate Surveillance",
            "Predict Actions",
            "Notify Medical Assistance",
            "Notify defence sectors/systems"
        )

    elif risk_level == "MEDIUM RISK":
        return (
            "Restrict Airspace",
            "Increase Surveillance",
            "Notify Local Authority",
            "Notify defence sectors/systems"
        )

    elif risk_level == "POTENTIAL RISK":
        return (
            "Monitor Continuously",
            "Track Object Movement",
            "Notify defence sectors/systems"
        )

    else:
        return (
            "Normal Monitoring",
        )
