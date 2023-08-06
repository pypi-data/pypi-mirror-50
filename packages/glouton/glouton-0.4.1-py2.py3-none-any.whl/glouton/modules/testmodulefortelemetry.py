
from glouton.modules.telemetryModuleBase import TelemetryModuleBase

class TestModuleForTelemetry(TelemetryModuleBase):
    def __init__(self, wdir):
        TelemetryModuleBase.__init__(self, wdir)
        self.count = 0

    def runAfterDownload(self, frame, full_path, telemetry):
        self.count += 1
        print('Timestamp ' + telemetry['timestamp'] + ' Frame ' +  frame + ' count ' + str(self.count))