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
        # THIS runs on the RISC-V CPU inside Kasli, NOT on your laptop.
        
        self.core.reset()
        # Flushes the RTIO event queue. Sets cursor = current hardware time.
        # Without this: leftover events from a previous run can cause conflicts.

        self.core.break_realtime()
        # Adds ~125µs of slack: cursor = now + 125µs
        # Why needed: compiling + sending the kernel takes time.
        # Your first event must land AFTER the kernel arrives at the FPGA.
        # Without slack: first event timestamp is already in the past → underflow.

        t_start = now_mu()
        # now_mu() reads the cursor as int64 (machine units, 1ns each here).
        # t_start is just an integer. e.g. t_start = 125000 (= 125µs in ns)

        # --- TTL0: HIGH for 10µs ---
        self.ttl0.on()          # queues event: (t_start, ttl0, HIGH)
        delay(10*us)            # cursor += 10000 mu. Does NOT wait.
        self.ttl0.off()         # queues event: (t_start+10000, ttl0, LOW)

        at_mu(t_start)          # rewinds cursor back to t_start
        # This is the key move. Now we're back at the same start time.

        # --- TTL1: HIGH for 5µs, SAME start time as TTL0 ---
        self.ttl1.on()          # queues event: (t_start, ttl1, HIGH)
        delay(5*us)             # cursor += 5000 mu
        self.ttl1.off()         # queues event: (t_start+5000, ttl1, LOW)

        # cursor is now at t_start+5000, but ttl0 runs until t_start+10000
        # manually advance past the longest branch:
        at_mu(t_start + self.core.seconds_to_mu(10*us) + self.core.seconds_to_mu(1*us))
        # now cursor = t_start + 11µs. Safe dead time after both pulses.

        self.ttl0.on()
        delay(2*us)
        self.ttl0.off()