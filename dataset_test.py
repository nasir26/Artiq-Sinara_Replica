from artiq.experiment import *
import numpy as np

class DatasetDemo(EnvExperiment):
    """Test datasets and NumPy integration."""
    
    def build(self):
        self.setattr_argument("num_points", NumberValue(default=10, precision=0, step=1))
    
    def run(self):
        x_data = np.linspace(0, 2*np.pi, int(self.num_points))
        y_data = np.sin(x_data)
        
        self.set_dataset("x_values", x_data, broadcast=True)
        self.set_dataset("y_values", y_data, broadcast=True)
        
        print(f"Generated {self.num_points} data points")
        print(f"X range: {x_data[0]:.2f} to {x_data[-1]:.2f}")
        print(f"Y range: {y_data.min():.2f} to {y_data.max():.2f}")
    
    def analyze(self):
        y = self.get_dataset("y_values")
        print(f"\nAnalysis:")
        print(f"  Mean Y: {np.mean(y):.4f}")
        print(f"  Max Y: {np.max(y):.4f}")
        print(f"  Min Y: {np.min(y):.4f}")
