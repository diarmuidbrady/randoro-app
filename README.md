# Randoro

Randoro is a work-in-progress random interval timer designed to enhance training, productivity, and games by introducing controlled randomness to routines. This app is being built with a Flask backend and plans to expand to a React Native frontend for mobile devices.

## Features (Current and Planned)

### Current Features:

- **Flask Backend:**
    - Generates random intervals based on user-specified total duration, number of intervals, and minimum interval duration.
    - Displays generated intervals via a simple HTML interface.
    - Includes an auditory beep system to signal interval timings.

### Planned Features:

- **React Native Frontend:**
    - A mobile-friendly interface for configuring timers and receiving real-time interval notifications.
    - Enhanced design and usability for iOS and Android platforms.
- **User Authentication:**
    - Save timer configurations for easy reuse.

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** React Native (Mobile; in development)
- **Other Tools:**
    - HTML and JavaScript for current simple interface.
    - Planned containerisation and orchestration with Docker.

## Setup Instructions

### Prerequisites:

- Python 3.8+ installed locally
- Flask and necessary dependencies (see `requirements.txt`)

### To Run the Current Flask App:

1. Clone the repository:
    
    ```bash
    git clone https://github.com/diarmuidbrady/randoro-app.git
    cd randoro/flask-server
    ```
    
2. Set up a virtual environment and install dependencies:
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # Use venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```
    
3. Start the Flask server:
    
    ```bash
    python app.py
    ```
    
4. Open your browser and navigate to `http://127.0.0.1:5000`.

### Generating Random Intervals:

1. Enter the total duration, number of intervals, and minimum interval duration.
2. Press "Generate" to see the intervals.
3. Press "Start" to activate the auditory beep system.

## Roadmap

1. **Backend Enhancements:**
    - Add a RESTful API for serving random intervals to the React Native frontend.
    - Implement user-specific configurations and data storage.
2. **Frontend Development:**
    - Build a React Native mobile app with a clean and intuitive interface.
    - Enable interval notification through visual and haptic feedback.
3. **Deployment:**
    - Containerise the application with Docker.
    - Host on cloud services for wider accessibility.