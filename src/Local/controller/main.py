import sys 
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from view.window import Window

class Main(Window):
    def __init__(self):
        self.startWindow()
        
Main()