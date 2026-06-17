from artiq.experiment import *

class DMAPulseRepeat(EnvExperiment):
    """
    CoreDMA: record a TTL pulse sequence, replay it 1000x.
    Ion trap analogue: gate repetition / dynamical decoupling train.
    """

    def build(self):
        self.setattr_device("core")
        self.setattr_device("core_dma")
        self.setattr_device("ttl0")
        self.setattr_device("ttl1")      # fix: setattr, not attr

    @kernel
    def record_sequence(self):
        with self.core_dma.record("gate"):   # fix: colon
            self.ttl0.pulse(1*us)            # fix: indented inside with
            delay(500*ns)
            self.ttl1.pulse(1*us)
            delay(500*ns)

    @kernel
    def run(self):
        self.core.reset()
        self.record_sequence()
        handle = self.core_dma.get_handle("gate")
        self.core.break_realtime()
        for _ in range(1000):
            self.core_dma.playback_handle(handle)