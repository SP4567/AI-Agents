def forensic_reasoning(timeline):
    narrative = []
    last_user_action = None

    for event in timeline:
        if "login" in event["description"].lower():
            last_user_action = event
        if "process started" in event["description"].lower():
            if last_user_action:
                narrative.append(
                    f"Process execution likely followed user action at {last_user_action['time']}"
                )

    return narrative