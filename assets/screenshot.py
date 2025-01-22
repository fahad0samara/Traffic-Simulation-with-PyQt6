from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import sys
import os
from simulation.full_sim import FullSimulation

def capture_screenshot():
    app = QApplication(sys.argv)
    window = FullSimulation()
    window.show()
    
    # Wait for window to be fully rendered
    def take_shot():
        # Create assets directory if it doesn't exist
        os.makedirs('assets', exist_ok=True)
        
        # Capture the window
        screen = window.grab()
        screen.save('assets/screenshot.png', 'PNG')
        app.quit()
    
    # Schedule screenshot after window is shown
    QTimer.singleShot(1000, take_shot)
    app.exec()

if __name__ == '__main__':
    capture_screenshot()
