from artiq.experiment import *
# imports: EnvExperiment, @kernel, delay, now_mu, at_mu, us, ms, MHz etc.

class PulseSequence(EnvExperiment):

    def build(self):
        # Runs on HOST. Declare what hardware you need.
        self.setattr_device("core")   # the Kasli FPGA itself
        self.setattr_device("ttl0")   # TTL output channel 0
        self.setattr_device("ttl1")   # TTL output channel 1

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()
        t = now_mu()
        self.ttl0.on()
        delay(10*us)
        self.ttl0.off()
        self.record_time(t)           # RPC to host

    def record_time(self, t):
        self.set_dataset("t_start_mu", t, broadcast=True)

    def analyze(self):
        t = self.get_dataset("t_start_mu")
        print(f"Kernel started at {t} mu = {t*1e-9*1e6:.3f} µs")