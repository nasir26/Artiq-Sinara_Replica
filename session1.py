from artiq.experiment import *

class PulseSequence(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl1")

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()

        t_start = now_mu()                    # save cursor position

        # branch 1 — ttl0 for 10us
        self.ttl0.on()
        delay(10*us)
        self.ttl0.off()

        at_mu(t_start)                        # rewind cursor to t_start
        # branch 2 — ttl1 for 5us, same start
        self.ttl1.on()
        delay(5*us)
        self.ttl1.off()

        # cursor is now at t_start + 5us, but ttl0 runs until t_start + 10us
        # advance to after the longest branch manually
        at_mu(t_start + self.core.seconds_to_mu(10*us) + self.core.seconds_to_mu(1*us))

        self.ttl0.on()
        delay(2*us)
        self.ttl0.off()