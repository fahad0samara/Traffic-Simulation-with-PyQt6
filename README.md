# 🚗 Autonomous Vehicle Navigation Simulator

A modern and interactive traffic simulation built with PyQt6, featuring autonomous vehicle navigation, dynamic weather effects, and realistic traffic scenarios.

![App Screenshot](assets/screenshot.png)

## ✨ Features

### 🎮 Core Gameplay
- Real-time vehicle control with smooth acceleration and braking
- Dynamic traffic system with AI-controlled vehicles
- Pedestrian simulation
- Traffic light system
- Collision detection and avoidance
- Safety scoring system

### 🌟 Special Effects
- Boost mode with particle effects
- Car tilting physics
- Metallic paint with reflections
- Dynamic lighting and shadows
- Weather particle systems

### 🌍 Environment
- Multiple weather conditions (Rain, Snow, Fog)
- Time of day changes (Day, Night, Sunset)
- Beautiful gradients and visual effects
- Realistic road and ground textures

### 📊 Statistics
- Speed monitoring
- Battery level tracking
- Distance traveled
- Safety score
- Time elapsed
- Traffic density controls

## 🎯 Controls

- **↑** - Accelerate
- **↓** - Brake
- **Space** - Emergency Stop
- **B** - Toggle Boost Mode

## 🛠️ Technical Architecture

### Components
1. **Simulation Core**
   - `TrafficSimulation` - Main simulation logic
   - `WeatherEffect` - Weather system management
   - `TrafficSystem` - Traffic and pedestrian AI

2. **User Interface**
   - `FullSimulation` - Main window and control panel
   - Custom-styled Qt widgets
   - Real-time statistics display

3. **Graphics Engine**
   - Custom QPainter rendering
   - Particle systems
   - Gradient and lighting effects

### Design Patterns
- Model-View-Controller (MVC) architecture
- Observer pattern for event handling
- State pattern for vehicle and weather states
- Factory pattern for vehicle creation

## 🚀 Installation

1. Clone the repository:
   ```bash
   cd autonomous_vehicle_navigation
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the simulation:
   ```bash
   python simulation/full_sim.py
   ```

## 📦 Dependencies

- Python 3.8+
- PyQt6
- NumPy
- PyQtGraph
- PyOpenGL (for advanced graphics)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎨 Credits

- Icons and UI design inspired by modern material design
- Weather effects based on particle system physics
- Traffic AI algorithms adapted from autonomous vehicle research

## 🔜 Future Plans

- [ ] Add multiplayer support
- [ ] Implement more advanced AI behaviors
- [ ] Add more vehicle types
- [ ] Create custom map editor
- [ ] Add sound effects and music
- [ ] Implement achievements system
- [ ] Add replay system
- [ ] Create scenario editor
