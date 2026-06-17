from artiq.experiment import *

class ArgumentsDemo(EnvExperiment):
    """Test experiment arguments."""
    
    def build(self):
        self.setattr_argument("count", NumberValue(default=10, precision=0, step=1))
        self.setattr_argument("message", StringValue(default="ARTIQ Test"))
        
    def run(self):
        print(f"Message: {self.message}")
        print(f"Count: {self.count}")
        for i in range(int(self.count)):
            print(f"  Iteration {i+1}")
