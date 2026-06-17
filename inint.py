# File: fpga_rtio_validation.py
from artiq.experiment import *
import numpy as np

class FPGA_RTIO_Validation(EnvExperiment):
    """Validate RTIO timing engine on Alveo U55C"""
    
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")  # Test channel
        self.setattr_device("ttl1")  # Reference channel
        
        # Test parameters
        self.n_pulses = 1000
        self.target_period_ns = 100  # 10 MHz test pattern
        
    @kernel
    def measure_rtio_jitter(self):
        """Generate precisely timed pulses and measure jitter"""
        timestamps = [0] * self.n_pulses
        
        self.core.reset()
        self.core.break_realtime()
        
        # Generate test pattern
        for i in range(self.n_pulses):
            t_start = now_mu()
            self.ttl0.pulse(50*ns)  # 50 ns pulse
            delay(self.target_period_ns*ns)
            timestamps[i] = now_mu()
            
        return timestamps
    
    @kernel
    def measure_gate_latency(self):
        """Measure gate execution latency"""
        self.core.break_realtime()
        
        latencies = [0] * 100
        for i in range(100):
            t0 = now_mu()
            self.ttl0.on()
            t1 = now_mu()
            self.ttl0.off()
            latencies[i] = self.core.mu_to_seconds(t1 - t0)
            delay(1*us)
            
        return latencies
    
    def analyze(self):
        """Analyze timing metrics"""
        timestamps = self.measure_rtio_jitter()
        latencies = self.measure_gate_latency()
        
        # Convert to time differences
        periods = np.diff(timestamps) * self.core.ref_period
        
        # Metrics
        mean_period = np.mean(periods)
        jitter_std = np.std(periods)
        jitter_pp = np.ptp(periods)  # Peak-to-peak
        max_deviation = np.max(np.abs(periods - self.target_period_ns*1e-9))
        
        mean_latency = np.mean(latencies)
        latency_std = np.std(latencies)
        
        print("\n" + "="*60)
        print("RTIO TIMING VALIDATION RESULTS")
        print("="*60)
        print(f"Reference Period: {self.core.ref_period*1e9:.3f} ns")
        print(f"Coarse Period: {8 * self.core.ref_period*1e9:.3f} ns")
        print(f"\nPulse Timing (n={self.n_pulses}):")
        print(f"  Target Period: {self.target_period_ns} ns")
        print(f"  Mean Period: {mean_period*1e9:.6f} ns")
        print(f"  Jitter (σ): {jitter_std*1e12:.3f} ps")
        print(f"  Jitter (p-p): {jitter_pp*1e12:.3f} ps")
        print(f"  Max Deviation: {max_deviation*1e12:.3f} ps")
        print(f"\nGate Latency:")
        print(f"  Mean: {mean_latency*1e9:.3f} ns")
        print(f"  Std Dev: {latency_std*1e12:.3f} ps")
        
        # Pass/Fail Criteria
        pass_criteria = {
            'jitter_std': (jitter_std*1e12 < 100, "Jitter < 100 ps"),
            'max_deviation': (max_deviation*1e12 < 500, "Max deviation < 500 ps"),
            'latency': (mean_latency*1e9 < 50, "Gate latency < 50 ns"),
            'determinism': (latency_std*1e12 < 50, "Latency variation < 50 ps")
        }
        
        print(f"\n{'PASS/FAIL CRITERIA':^60}")
        print("-"*60)
        all_pass = True
        for test, (passed, criterion) in pass_criteria.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{criterion:40s} {status:>20s}")
            all_pass = all_pass and passed
        
        print("="*60)
        if all_pass:
            print("STATUS: ALL TESTS PASSED")
        else:
            print("STATUS: FAILED - Review timing configuration")
        print("="*60)
        
        return all_pass