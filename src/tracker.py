# src/tracker.py

class TargetTracker:

    def __init__(self):
        self.targets = {}

    def update_target(self, target_id, position):

        if target_id not in self.targets:

            self.targets[target_id] = {
                "position": position,
                "history": [position]
            }

        else:

            self.targets[target_id]["position"] = position
            self.targets[target_id]["history"].append(position)

        return self.targets[target_id]

    def get_targets(self):
        return self.targets
