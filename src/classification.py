def classify_behavior(speed):
    if speed < 60:
        return "Normal Flight"
    elif speed < 150:
        return "Suspicious Movement"
    else:
        return "Restricted Zone Entry"
