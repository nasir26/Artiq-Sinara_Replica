from artiq.experiment import *

class HelloWorld(EnvExperiment):
    """Simple Hello World experiment."""
    
    def build(self):
        pass
    
    def run(self):
        print("Hello from ARTIQ!")
        print("Installation successful!")
        for i in range(5):
            print(f"Count: {i}")
