# AISVE - AI & Sustainability in VET Education

## Overview

AISVE (AI & Sustainability in VET Education) is part of a comprehensive 35-month European project (September 2023 - July 2026) that addresses the urgent need to integrate AI education in Vocational Education and Training (VET). This repository contains a collection of technological projects developed to bridge the skills gap and prepare the workforce for AI-driven changes while promoting sustainable solutions.

The project is driven by the recognition that AI is a transformative force in modern society, yet many students finishing compulsory education lack understanding of its workings, potential opportunities, and necessary precautions. In a digitally advancing Europe, integrating AI education is both urgent and essential.

This collection of projects ranges from basic sensor implementations to advanced AI-powered solutions, all designed to raise awareness about environmental issues and provide practical solutions for environmental monitoring and automation through hands-on learning experiences.

**Project Author:** Lucas Molino Piñar  
**Organization:** EVTA (European Vocational Training Association)  
**Project Duration:** 35 months (01/09/2023 - 31/07/2026)

## Project Structure

The repository is organized into progressive difficulty levels, with each project containing complete code and documentation:

```
AISVE/
├── PR1A/          # Level 1: Fire Detection System
│   ├── main.py
│   ├── README.md
│   └── requirements.txt
├── PR1B/          # Level 1: Simplified Solar Tracker
│   ├── main.py
│   ├── README.md
│   └── requirements.txt
├── PR2A/          # Level 2: Interactive Environmental Station
│   ├── main.py
│   ├── README.md
│   └── requirements.txt
├── PR2B/          # Level 2: Motion-Activated LED Lighting
│   ├── main.py
│   ├── README.md
│   └── requirements.txt
├── PR3A/          # Level 3: Rotten Apple Detector Using AI
│   ├── main.py
│   ├── model/
│   │   ├── best.pt
│   │   └── train_model.ipynb
│   ├── README.md
│   └── requirements.txt
├── PR3B/          # Level 3: Trash Detection and Segmentation
│   ├── main.py
│   ├── model/
│   │   ├── best.pt
│   │   └── pr3b.ipynb
│   ├── README.md
│   └── requirements.txt
└── PR4/           # Level 4: Automated Waste Classification System
    ├── main.py
    ├── model/
    │   ├── best.pt
    │   └── model_train.ipynb
    ├── README.md
    └── requirements.txt
```

Each project directory contains:
- `main.py` - Main Python implementation
- `README.md` - Project-specific documentation
- `requirements.txt` - Python dependencies
- `model/` - AI models and training notebooks (for advanced projects)

## Project Context and Objectives

### Main Objectives
- **Raise awareness** of sustainability and develop innovative approaches to teaching and learning
- **Develop skills and confidence** of teachers in the development and use of AI solutions
- **Encourage teachers** to design and share innovative and effective practices for sustainability through AI-based technologies
- **Create a network** of #AI-SAVES VET Clubs where students and teachers can produce collaborative solutions to address sustainability issues
- **Reinforce links** between schools, NGOs, companies, teacher training centers, professional associations, and universities

### Project Components
This repository contributes to the broader AISVE ecosystem which includes:
- **AI KIT:** Microprocessors, cameras, sensors, and actuators for hands-on learning
- **MooC:** Online course "AI-SAVES: Artificial Intelligence and Sustainable Automated Vision for Environmental Solutions"
- **AI-SAVES@ProjectHub:** Resource hub for sharing pedagogical projects within the VET community
- **#AI-SAVES VET Clubs:** School-based clubs for knowledge dissemination and ongoing development

### Target Groups
**Direct:**
- VET teachers and trainers from partnership organizations
- VET teachers and trainers from across Europe
- VET students

**Indirect:**
- VET Schools
- Companies
- NGOs and civil society organizations
- Environmental associations
- Other relevant stakeholders

## Projects by Difficulty Level

### Level 1 - Easy Projects 🟢

#### PR1A: Fire Detection System
A Raspberry Pi-based fire detection system using temperature sensors and LED indicators.

**Features:**
- Temperature monitoring with threshold alerts
- Three-stage LED warning system (green/yellow/red)
- Early fire detection for forest and indoor environments

**Hardware:**
- Raspberry Pi
- Temperature sensor
- 3 LEDs (green, yellow, red)
- Basic electronic components

#### PR1B: Simplified Solar Tracker
Smart solar panel simulation system that tracks light sources for maximum energy capture.

**Features:**
- Dual LDR light detection
- Servo motor control for panel orientation
- Automated light source tracking

**Hardware:**
- Raspberry Pi
- 2 LDR sensors
- Servo motor
- Electronic components

### Level 2 - Medium Projects 🟡

#### PR2A: Interactive Environmental Station
Real-time environmental monitoring station with user interface.

**Features:**
- Temperature, humidity, and light monitoring
- Interactive button-controlled display
- Real-time environmental data visualization

**Hardware:**
- Raspberry Pi
- Temperature/humidity sensor
- Light sensor
- 3 control buttons
- Display screen

#### PR2B: Motion-Activated LED Lighting
Energy-efficient lighting system activated by motion detection.

**Features:**
- Ultrasonic motion detection
- Automatic LED strip activation
- Configurable activation duration
- Energy consumption optimization

**Hardware:**
- Raspberry Pi
- Ultrasonic sensor
- LED strip
- Electronic components

### Level 3 - Advanced Projects 🟠

#### PR3A: Rotten Apple Detector Using AI
AI-powered system for food waste reduction through automated fruit quality assessment.

**Features:**
- Deep learning model for apple classification
- Fresh vs. rotten apple detection
- Camera-based image analysis
- Food waste reduction application

**Hardware:**
- Raspberry Pi
- Camera module
- Pre-trained AI model (`best.pt`)

**AI Components:**
- Custom trained YOLOv8 model
- Image classification pipeline
- Real-time inference capability

#### PR3B: Trash Detection and Segmentation
Advanced computer vision system for environmental cleanup monitoring.

**Features:**
- Trash detection in water environments
- Object segmentation capabilities
- Environmental monitoring application

**Hardware:**
- Raspberry Pi
- Camera module
- AI model for trash detection

### Level 4 - Integrated Project 🔴

#### PR4: Automated Waste Detection and Classification System
Comprehensive waste management solution combining multiple technologies.

**Features:**
- Multi-class waste classification (plastic, paper, glass)
- Proximity-activated system using ultrasonic sensors
- Adaptive lighting for optimal image capture
- Real-time classification results display
- Educational and practical waste sorting assistance

**Hardware:**
- Raspberry Pi
- Camera module
- Ultrasonic sensor
- LED strip for lighting
- Display screen
- Complete electronic circuit

**AI Components:**
- Advanced deep learning model
- Multi-class classification
- Real-time processing pipeline

## Technical Requirements

### Hardware Prerequisites
- Raspberry Pi (3B+ or 4 recommended)
- MicroSD card (32GB minimum)
- Various sensors and electronic components (specific to each project)
- Breadboard and jumper wires
- Power supply

### Software Prerequisites
- Raspberry Pi OS
- Python 3.7+
- OpenCV
- PyTorch (for AI projects)
- Additional dependencies listed in each project's `requirements.txt`

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/EVTA-EU/AISVE.git
   cd AISVE
   ```

2. **Navigate to desired project:**
   ```bash
   cd PR1A  # Example for Fire Detection System
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the project:**
   ```bash
   python main.py
   ```

## Circuit Diagrams and Documentation

Each project includes comprehensive documentation in its individual README.md file with:
- Hardware requirements and connections
- Setup instructions
- Usage examples
- Project-specific implementation details

For AI-powered projects (PR3A, PR3B, PR4), additional resources include:
- Training notebooks for model development
- Pre-trained models ready for deployment

## AI Model Information

Projects PR3A, PR3B, and PR4 include pre-trained deep learning models:
- **Model Format:** PyTorch (.pt files)
- **Training:** Custom datasets with environmental focus
- **Performance:** Optimized for Raspberry Pi deployment
- **Training Notebooks:** Jupyter notebooks included for model development

## Usage Examples

### Basic Sensor Projects (PR1A, PR1B, PR2A, PR2B)
These projects demonstrate fundamental IoT concepts and can be used for:
- Educational demonstrations
- Environmental monitoring installations
- Proof-of-concept implementations

### AI-Powered Projects (PR3A, PR3B, PR4)
Advanced projects suitable for:
- Research and development
- Commercial applications
- Advanced educational programs
- Environmental monitoring systems

## Contributing

We welcome contributions to improve and expand the AISVE project collection. Please:

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## Educational Impact

These projects serve multiple educational purposes:
- **STEM Education:** Hands-on learning with electronics and programming
- **Environmental Awareness:** Practical applications for sustainability
- **AI Literacy:** Introduction to machine learning concepts
- **Problem-Solving:** Real-world environmental challenges

## Support and Documentation

For detailed information about each project:
- Check individual project README.md files in each project directory
- Review training notebooks in `model/` folders for AI projects
- Refer to requirements.txt for specific dependencies

## Acknowledgments

This project is developed by Lucas Molino Piñar as part of the AISVE (AI & Sustainability in VET Education) initiative under the EVTA (European Vocational Training Association). The project contributes to a broader European effort to integrate AI education in vocational training and promote sustainable technology solutions for environmental challenges.

**EVTA's Role in AISVE:**
- Contributing 8 projects to the Project Hub
- Leading the European Online contest
- Hosting the final conference
- Organizing 2 National replication workshops

This work supports the mission to equip VET teachers and students with the skills to engage in AI and sustainability projects, creating a network of collaborative solutions for environmental challenges.

---
