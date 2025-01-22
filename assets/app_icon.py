from PyQt6.QtGui import QIcon, QPainter, QColor, QLinearGradient
from PyQt6.QtCore import QSize, Qt

def create_app_icon():
    icon = QIcon()
    size = QSize(128, 128)
    
    # Create a painter to draw the icon
    painter = QPainter()
    painter.begin(icon.pixmap(size))
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Draw background gradient
    gradient = QLinearGradient(0, 0, 0, size.height())
    gradient.setColorAt(0, QColor(52, 152, 219))  # Blue
    gradient.setColorAt(1, QColor(41, 128, 185))  # Darker blue
    painter.fillRect(0, 0, size.width(), size.height(), gradient)
    
    # Draw car silhouette
    car_color = QColor(236, 240, 241)  # Light gray
    painter.setBrush(car_color)
    painter.setPen(Qt.PenStyle.NoPen)
    
    # Body
    painter.drawRect(20, 40, 88, 30)
    
    # Roof
    painter.drawRect(30, 20, 68, 20)
    
    # Windows
    window_color = QColor(52, 73, 94)  # Dark blue-gray
    painter.setBrush(window_color)
    painter.drawRect(35, 25, 25, 15)  # Front window
    painter.drawRect(65, 25, 25, 15)  # Back window
    
    # Wheels
    wheel_color = QColor(44, 62, 80)  # Very dark blue
    painter.setBrush(wheel_color)
    painter.drawEllipse(30, 60, 20, 20)  # Front wheel
    painter.drawEllipse(78, 60, 20, 20)  # Back wheel
    
    painter.end()
    return icon
