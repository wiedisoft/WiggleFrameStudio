from proglog import ProgressBarLogger


class ProgressLogger(ProgressBarLogger):
    def __init__(self, on_progress):
        super().__init__()
        self.on_progress = on_progress
        self.totals = {}

    def bars_callback(self, bar, attr, value, old_value=None):
        if attr == "total":
            self.totals[bar] = value

        elif attr == "index" and bar in self.totals:
            total = self.totals[bar]
            if total:
                progress = value / total
                self.on_progress(progress)
