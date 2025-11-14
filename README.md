# mouseStearingSimulation
Use mouse scroll to simulate the behavior of a steering wheel in driving games with WASD controls.

## Features
- **Scroll Up**: Turns right by tapping the D key
- **Scroll Down**: Turns left by tapping the A key
- **Variable Speed**: The more you scroll, the faster the keys are tapped
- **Frequency Control**: Key tapping frequency ranges from 0 to 15 times per second (1/15 seconds minimum delay)
- **Toggle Control**: Press Numpad 0 to enable/disable the simulation

## Requirements
- Python 3.7+
- pynput library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/julianVillega/mouseStearingSimulation.git
cd mouseStearingSimulation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python3 mouse_steering.py
```

**Controls:**
- **Scroll Mouse Up**: Turn right (simulates D key presses)
- **Scroll Mouse Down**: Turn left (simulates A key presses)
- **Numpad 0**: Toggle the simulation ON/OFF
- **Ctrl+C**: Exit the program

The script starts in **disabled** mode. Press Numpad 0 to enable it.

## How It Works

The script uses the `pynput` library to:
1. Listen to mouse scroll events
2. Listen to keyboard events (for the toggle key)
3. Simulate key presses (A or D) based on scroll direction

The tapping frequency is proportional to the scroll intensity, with a maximum frequency of 15 taps per second (minimum delay of 1/15 seconds between taps).

## Notes

- This script requires appropriate permissions to listen to input events and simulate key presses
- On Linux, you may need to run with appropriate permissions or add your user to the `input` group
- The script runs in the background and can be stopped with Ctrl+C
