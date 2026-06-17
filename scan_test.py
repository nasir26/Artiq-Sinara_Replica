from artiq.experiment import *

class ScanDemo(EnvExperiment):
    """Test parameter scanning."""
    
    def build(self):
        self.setattr_argument("frequencies", Scannable(
            default=RangeScan(start=1.0, stop=10.0, npoints=5),
            unit="MHz"
        ))
    
    def run(self):
        print("Scanning frequencies:")
        for i, freq in enumerate(self.frequencies):
            print(f"  Point {i+1}: {freq:.2f} MHz")
        print("Scan complete!")
