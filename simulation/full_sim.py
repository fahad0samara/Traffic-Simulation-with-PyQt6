import sys
import random
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLabel, QProgressBar, QGroupBox, QSlider, QComboBox)
from PyQt6.QtGui import QPainter, QColor, QPen, QKeyEvent, QFont, QLinearGradient, QRadialGradient
from PyQt6.QtCore import Qt, QTimer, QPointF
from assets.app_icon import create_app_icon

# Set application style
APP_STYLE = """
QMainWindow {
    background-color: #2c3e50;
}

QGroupBox {
    background-color: #34495e;
    border: 2px solid #3498db;
    border-radius: 5px;
    margin-top: 1em;
    font-weight: bold;
    color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
    color: #3498db;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9;
}

QLabel {
    color: white;
}

QProgressBar {
    border: 2px solid #3498db;
    border-radius: 5px;
    text-align: center;
    color: white;
}

QProgressBar::chunk {
    background-color: #2ecc71;
    border-radius: 3px;
}

QComboBox {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 5px;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: url(none);
    border: none;
}

QComboBox QAbstractItemView {
    background-color: #2980b9;
    color: white;
    selection-background-color: #3498db;
}
"""

class WeatherEffect:
    def __init__(self):
        self.raindrops = []
        self.is_raining = False
        self.is_snowing = False
        self.is_foggy = False
        self.time_of_day = "day"  # day, night, sunset
        
    def update(self):
        if self.is_raining or self.is_snowing:
            # Add new particles
            for _ in range(5):
                x = random.randint(0, 800)
                y = random.randint(0, 600)
                speed = random.uniform(5, 10)
                self.raindrops.append([x, y, speed])
                
        # Update existing particles
        for drop in self.raindrops[:]:
            drop[1] += drop[2]  # Move down
            if drop[1] > 600:
                self.raindrops.remove(drop)

class TrafficSystem:
    def __init__(self):
        self.cars = []
        self.pedestrians = []
        self.traffic_lights = []
        
        # Initialize some traffic
        self.add_traffic_cars(3)
        self.add_pedestrians(2)
        self.add_traffic_lights(2)
        
    def check_collision(self, x1, w1, x2, w2):
        # Check if two objects overlap horizontally
        return (x1 < x2 + w2) and (x1 + w1 > x2)
        
    def add_traffic_cars(self, count):
        for _ in range(count):
            x = random.randint(100, 700)
            speed = random.uniform(1, 2)
            self.cars.append({
                'x': x,
                'speed': speed,
                'width': 40,  # Car width
                'lane': random.choice([0, 1])  # 0 for top lane, 1 for bottom lane
            })
            
    def add_pedestrians(self, count):
        for _ in range(count):
            x = random.randint(100, 700)
            speed = random.uniform(0.5, 1)
            self.pedestrians.append({'x': x, 'speed': speed})
            
    def add_traffic_lights(self, count):
        spacing = 800 / (count + 1)
        for i in range(count):
            x = int(spacing * (i + 1))
            self.traffic_lights.append({
                'x': x,
                'state': 'green',
                'timer': random.randint(50, 150)
            })
            
    def update(self, main_car_x=0, main_car_width=60):
        # Update traffic cars
        for car in self.cars:
            # Store old position for collision check
            old_x = car['x']
            
            # Update position
            car['x'] += car['speed']
            
            # Check collision with main car
            if self.check_collision(car['x'], car['width'], main_car_x, main_car_width):
                # If collision would occur, revert to old position and adjust speed
                car['x'] = old_x
                car['speed'] = max(0, car['speed'] - 0.1)  # Slow down
            else:
                car['speed'] = min(2, car['speed'] + 0.1)  # Speed up if no collision
            
            # Reset position if off screen
            if car['x'] > 800:
                car['x'] = -car['width']
                car['lane'] = random.choice([0, 1])  # Choose new lane
                
        # Update pedestrians
        for ped in self.pedestrians:
            ped['x'] += ped['speed']
            if ped['x'] > 800:
                ped['x'] = 0
                
        # Update traffic lights
        for light in self.traffic_lights:
            light['timer'] -= 1
            if light['timer'] <= 0:
                light['state'] = 'red' if light['state'] == 'green' else 'green'
                light['timer'] = random.randint(50, 150)

class SimulationView(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        
        # Initialize subsystems
        self.weather = WeatherEffect()
        self.traffic = TrafficSystem()
        
        # Car properties
        self.car_x = 50
        self.target_speed = 0
        self.current_speed = 0
        self.car_width = 60
        self.car_color = QColor(0, 100, 255)  # Nice blue color
        self.boost_mode = False
        self.boost_particles = []
        self.car_height = 30
        self.car_angle = 0
        
    def toggle_boost(self):
        self.boost_mode = not self.boost_mode
        if self.boost_mode:
            self.car_color = QColor(255, 165, 0)  # Orange for boost mode
        else:
            self.car_color = QColor(0, 100, 255)  # Back to blue
            
    def add_boost_particle(self):
        if self.boost_mode and self.current_speed > 0:
            self.boost_particles.append({
                'x': self.car_x,
                'y': random.randint(int(self.car_y - 10), int(self.car_y + 10)),
                'size': random.randint(5, 15),
                'life': 1.0
            })
            
    def update_boost_particles(self):
        new_particles = []
        for p in self.boost_particles:
            p['x'] -= 5
            p['life'] -= 0.1
            if p['life'] > 0:
                new_particles.append(p)
        self.boost_particles = new_particles
        
    def bounce_effect(self):
        self.car_angle = random.uniform(-5, 5)
        
    def set_speed(self, speed):
        old_speed = self.target_speed
        self.target_speed = speed
        if speed > old_speed:
            self.bounce_effect()
            
    def update_simulation(self):
        # Smoothly adjust current speed towards target speed
        if self.current_speed < self.target_speed:
            self.current_speed = min(self.target_speed, self.current_speed + 1)
        elif self.current_speed > self.target_speed:
            self.current_speed = max(self.target_speed, self.current_speed - 1)
            
        # Update car position based on current speed
        if self.current_speed > 0:
            self.car_x += self.current_speed / 10
            if self.car_x > self.width():
                self.car_x = 0
        
        # Update traffic with main car position
        self.traffic.update(self.car_x, self.car_width)
        
        # Update weather
        self.weather.update()
        
        # Add boost particles
        self.add_boost_particle()
        
        # Update boost particles
        self.update_boost_particles()
        
        # Trigger repaint
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background based on time of day
        if self.weather.time_of_day == "night":
            painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 50))
            # Add stars
            for _ in range(50):
                x = random.randint(0, self.width())
                y = random.randint(0, self.height() - 200)
                size = random.randint(1, 3)
                painter.fillRect(x, y, size, size, QColor(255, 255, 255))
        elif self.weather.time_of_day == "sunset":
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(255, 100, 0))
            gradient.setColorAt(0.5, QColor(255, 150, 50))
            gradient.setColorAt(1, QColor(100, 50, 0))
            painter.fillRect(0, 0, self.width(), self.height(), gradient)
        else:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(135, 206, 235))
            gradient.setColorAt(1, QColor(200, 230, 255))
            painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # Draw ground with gradient
        ground_y = self.height() - 200
        ground_gradient = QLinearGradient(0, ground_y, 0, self.height())
        ground_gradient.setColorAt(0, QColor(34, 139, 34))
        ground_gradient.setColorAt(1, QColor(28, 120, 28))
        painter.fillRect(0, ground_y, self.width(), 200, ground_gradient)
        
        # Draw road with perspective effect
        road_y = self.height() - 180
        road_height = 100
        road_gradient = QLinearGradient(0, road_y, 0, road_y + road_height)
        road_gradient.setColorAt(0, QColor(60, 60, 60))
        road_gradient.setColorAt(1, QColor(40, 40, 40))
        painter.fillRect(0, road_y, self.width(), road_height, road_gradient)
        
        # Draw lane markings with glow effect
        painter.setPen(QPen(Qt.GlobalColor.white, 3))
        center_y = road_y + road_height/2
        x = 0
        while x < self.width():
            # Draw glow
            glow = QRadialGradient(x + 15, int(center_y), 10)
            glow.setColorAt(0, QColor(255, 255, 255, 100))
            glow.setColorAt(1, QColor(255, 255, 255, 0))
            painter.fillRect(int(x), int(center_y - 10), 30, 20, glow)
            
            # Draw line
            painter.drawLine(int(x), int(center_y), int(x + 30), int(center_y))
            x += 50
            
        # Draw boost particles
        if self.boost_mode:
            for p in self.boost_particles:
                color = QColor(255, 165, 0, int(p['life'] * 255))
                painter.setBrush(color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(int(p['x']), int(p['y']), int(p['size']), int(p['size']))
                
        # Draw main car with tilt effect
        car_y = int(road_y + 35)
        self.car_y = car_y  # Store for particle effects
        
        # Save current transform
        painter.save()
        
        # Translate to car center and rotate
        painter.translate(int(self.car_x + self.car_width/2), int(car_y + self.car_height/2))
        painter.rotate(self.car_angle)
        
        # Draw car body with metallic effect
        gradient = QLinearGradient(-self.car_width/2, -self.car_height/2, 
                                 self.car_width/2, self.car_height/2)
        gradient.setColorAt(0, self.car_color.lighter(120))
        gradient.setColorAt(0.5, self.car_color)
        gradient.setColorAt(1, self.car_color.darker(120))
        
        painter.fillRect(int(-self.car_width/2), int(-self.car_height/2), 
                        self.car_width, self.car_height, gradient)
                        
        # Draw car roof
        painter.fillRect(int(-self.car_width/2 + 10), int(-self.car_height/2 - 20), 
                        30, 20, self.car_color.darker(150))
                        
        # Draw windows with reflection
        window_gradient = QLinearGradient(0, -self.car_height/2 - 15, 0, -self.car_height/2 - 5)
        window_gradient.setColorAt(0, QColor(200, 200, 255))
        window_gradient.setColorAt(1, QColor(150, 150, 200))
        painter.fillRect(int(-self.car_width/2 + 12), int(-self.car_height/2 - 18), 
                        26, 16, window_gradient)
                        
        # Restore transform
        painter.restore()
        
        # Draw headlights with glow
        if self.weather.time_of_day == "night":
            headlight_glow = QRadialGradient(int(self.car_x + self.car_width - 5), int(car_y + 15), 30)
            headlight_glow.setColorAt(0, QColor(255, 255, 200, 150))
            headlight_glow.setColorAt(1, QColor(255, 255, 100, 0))
            painter.fillRect(int(self.car_x + self.car_width - 35), car_y, 70, 30, headlight_glow)
        
        # Draw traffic lights
        for light in self.traffic.traffic_lights:
            color = QColor("green") if light['state'] == 'green' else QColor("red")
            painter.setBrush(color)
            painter.drawEllipse(int(light['x']), int(road_y - 20), 10, 10)
        
        # Draw traffic cars
        for car in self.traffic.cars:
            car_y = int(road_y + 15) if car['lane'] == 0 else int(road_y + 55)
            painter.fillRect(int(car['x']), car_y, car['width'], 20, QColor(255, 0, 0))
        
        # Draw pedestrians
        sidewalk_y = road_y + road_height + 10
        for ped in self.traffic.pedestrians:
            painter.setBrush(QColor(0, 255, 0))
            painter.drawEllipse(int(ped['x']), int(sidewalk_y), 5, 5)
        
        # Draw weather effects
        if self.weather.is_raining:
            painter.setPen(QPen(Qt.GlobalColor.white, 1))
            for drop in self.weather.raindrops:
                painter.drawLine(int(drop[0]), int(drop[1]), 
                               int(drop[0]), int(drop[1] + 10))
        elif self.weather.is_snowing:
            painter.setBrush(QColor(255, 255, 255))
            for drop in self.weather.raindrops:
                painter.drawEllipse(int(drop[0]), int(drop[1]), 2, 2)
                
        if self.weather.is_foggy:
            fog = QColor(200, 200, 200, 100)
            painter.fillRect(0, 0, self.width(), self.height(), fog)

class FullSimulation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Full Autonomous Vehicle Simulation")
        self.setGeometry(100, 100, 1200, 800)
        
        # Enable keyboard focus
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Create control panel
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # Create simulation view
        self.sim_view = SimulationView()
        main_layout.addWidget(self.sim_view, stretch=2)
        
        # Initialize simulation state
        self.speed = 0
        self.battery = 100
        self.distance = 0
        self.safety_score = 100
        self.cars_passed = 0
        self.time_elapsed = 0
        self.is_running = False
        
        # Set up timer for continuous updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)  # 60 FPS
        
        # Timer for stats update
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(1000)  # Update every second
        
        # Keyboard event timer
        self.key_timer = QTimer()
        self.key_timer.timeout.connect(self.handle_continuous_keys)
        self.key_timer.start(50)  # Check keys every 50ms
        self.keys_pressed = set()
        
    def keyPressEvent(self, event):
        if not self.is_running:
            return
            
        self.keys_pressed.add(event.key())
        
        # Add boost mode with B key
        if event.key() == Qt.Key.Key_B:
            self.sim_view.toggle_boost()
            if self.sim_view.boost_mode:
                self.speed_label.setStyleSheet("""
                    QLabel {
                        font-size: 24px;
                        color: orange;
                        font-weight: bold;
                        padding: 5px;
                        background-color: #f0f0f0;
                        border-radius: 5px;
                    }
                """)
            else:
                self.speed_label.setStyleSheet("""
                    QLabel {
                        font-size: 24px;
                        color: blue;
                        font-weight: bold;
                        padding: 5px;
                        background-color: #f0f0f0;
                        border-radius: 5px;
                    }
                """)
            
    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())
            
    def handle_continuous_keys(self):
        if not self.is_running:
            return
            
        if Qt.Key.Key_Up in self.keys_pressed:
            speed_increase = 4 if self.sim_view.boost_mode else 2
            self.speed = min(150 if self.sim_view.boost_mode else 100, self.speed + speed_increase)
            self.sim_view.set_speed(self.speed)
        elif Qt.Key.Key_Down in self.keys_pressed:
            self.speed = max(0, self.speed - 2)
            self.sim_view.set_speed(self.speed)
        elif Qt.Key.Key_Space in self.keys_pressed:
            self.speed = 0
            self.sim_view.set_speed(0)
            
        self.speed_label.setText(f"Speed: {self.speed} km/h")
        
    def create_control_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Vehicle Stats
        stats_group = QGroupBox("Vehicle Statistics")
        stats_layout = QVBoxLayout()
        
        # Speed display with big numbers
        self.speed_label = QLabel("Speed: 0 km/h")
        self.speed_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: blue;
                font-weight: bold;
                padding: 5px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
        """)
        stats_layout.addWidget(self.speed_label)
        
        # Battery with percentage
        battery_layout = QHBoxLayout()
        battery_layout.addWidget(QLabel("Battery:"))
        self.battery_bar = QProgressBar()
        self.battery_bar.setValue(100)
        self.battery_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                font-size: 14px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        battery_layout.addWidget(self.battery_bar)
        stats_layout.addLayout(battery_layout)
        
        # Distance with decimal places
        self.distance_label = QLabel("Distance: 0.0 km")
        self.distance_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        stats_layout.addWidget(self.distance_label)
        
        # Safety score
        self.safety_label = QLabel("Safety Score: 100%")
        self.safety_label.setStyleSheet("font-size: 18px; color: green; font-weight: bold;")
        stats_layout.addWidget(self.safety_label)
        
        # Cars passed counter
        self.cars_passed_label = QLabel("Cars Passed: 0")
        self.cars_passed_label.setStyleSheet("font-size: 18px;")
        stats_layout.addWidget(self.cars_passed_label)
        
        # Time elapsed
        self.time_label = QLabel("Time: 00:00")
        self.time_label.setStyleSheet("font-size: 18px; font-family: monospace;")
        stats_layout.addWidget(self.time_label)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Weather Controls
        weather_group = QGroupBox("Weather Controls")
        weather_layout = QVBoxLayout()
        
        self.weather_combo = QComboBox()
        self.weather_combo.addItems(["Clear", "Rain", "Snow", "Fog"])
        self.weather_combo.currentTextChanged.connect(self.change_weather)
        weather_layout.addWidget(self.weather_combo)
        
        self.time_combo = QComboBox()
        self.time_combo.addItems(["Day", "Night", "Sunset"])
        self.time_combo.currentTextChanged.connect(self.change_time)
        weather_layout.addWidget(self.time_combo)
        
        weather_group.setLayout(weather_layout)
        layout.addWidget(weather_group)
        
        # Traffic Controls
        traffic_group = QGroupBox("Traffic Controls")
        traffic_layout = QVBoxLayout()
        
        # Traffic car counter
        self.traffic_count_label = QLabel("Traffic Cars: 3")
        traffic_layout.addWidget(self.traffic_count_label)
        
        add_car_btn = QPushButton("Add Traffic Car")
        add_car_btn.clicked.connect(self.add_traffic_car)
        traffic_layout.addWidget(add_car_btn)
        
        # Pedestrian counter
        self.pedestrian_count_label = QLabel("Pedestrians: 2")
        traffic_layout.addWidget(self.pedestrian_count_label)
        
        add_ped_btn = QPushButton("Add Pedestrian")
        add_ped_btn.clicked.connect(self.add_pedestrian)
        traffic_layout.addWidget(add_ped_btn)
        
        traffic_group.setLayout(traffic_layout)
        layout.addWidget(traffic_group)
        
        # Vehicle Controls
        controls_group = QGroupBox("Vehicle Controls")
        controls_layout = QVBoxLayout()
        
        self.start_button = QPushButton("START")
        self.start_button.clicked.connect(self.toggle_simulation)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 20px;
                padding: 15px;
                border-radius: 10px;
                font-weight: bold;
            }
        """)
        controls_layout.addWidget(self.start_button)
        
        # Instructions
        instructions = QLabel(
            "Controls:\n"
            "↑ - Accelerate\n"
            "↓ - Brake\n"
            "Space - Emergency Stop\n"
            "B - Toggle Boost Mode"
        )
        instructions.setStyleSheet("font-family: monospace; font-size: 14px;")
        controls_layout.addWidget(instructions)
        
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        layout.addStretch()
        return panel
        
    def add_traffic_car(self):
        self.sim_view.traffic.add_traffic_cars(1)
        count = len(self.sim_view.traffic.cars)
        self.traffic_count_label.setText(f"Traffic Cars: {count}")
        
    def add_pedestrian(self):
        self.sim_view.traffic.add_pedestrians(1)
        count = len(self.sim_view.traffic.pedestrians)
        self.pedestrian_count_label.setText(f"Pedestrians: {count}")
        
    def update_stats(self):
        if self.is_running:
            self.time_elapsed += 1
            minutes = self.time_elapsed // 60
            seconds = self.time_elapsed % 60
            self.time_label.setText(f"Time: {minutes:02d}:{seconds:02d}")
            
            # Update safety score based on speed and proximity to other cars
            if self.speed > 80:
                self.safety_score = max(0, self.safety_score - 1)
            elif self.speed < 60:
                self.safety_score = min(100, self.safety_score + 0.5)
                
            self.safety_label.setText(f"Safety Score: {int(self.safety_score)}%")
            if self.safety_score < 50:
                self.safety_label.setStyleSheet("font-size: 18px; color: red; font-weight: bold;")
            elif self.safety_score < 80:
                self.safety_label.setStyleSheet("font-size: 18px; color: orange; font-weight: bold;")
            else:
                self.safety_label.setStyleSheet("font-size: 18px; color: green; font-weight: bold;")
                
    def change_weather(self, weather):
        self.sim_view.weather.is_raining = weather == "Rain"
        self.sim_view.weather.is_snowing = weather == "Snow"
        self.sim_view.weather.is_foggy = weather == "Fog"
        
    def change_time(self, time):
        self.sim_view.weather.time_of_day = time.lower()
        
    def toggle_simulation(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.setText("STOP")
            self.start_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    font-size: 20px;
                    padding: 15px;
                    border-radius: 10px;
                    font-weight: bold;
                }
            """)
            self.setFocus()
        else:
            self.speed = 0
            self.sim_view.set_speed(0)
            self.start_button.setText("START")
            self.start_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 20px;
                    padding: 15px;
                    border-radius: 10px;
                    font-weight: bold;
                }
            """)
            
    def update_simulation(self):
        # Update battery based on speed
        self.battery = max(0, self.battery - self.speed * 0.001)
        self.battery_bar.setValue(int(self.battery))
        
        # Update distance
        self.distance += self.speed * 0.001
        self.distance_label.setText(f"Distance: {self.distance:.1f} km")
        
        # Update simulation view
        self.sim_view.update_simulation()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for modern look
    app.setStyleSheet(APP_STYLE)
    
    # Set application icon
    app.setWindowIcon(create_app_icon())
    
    window = FullSimulation()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
