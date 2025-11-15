# mouseStearingSimulation
Use mouse scroll to simulate the behavior of a steering wheel in driving games with WASD controls using a duty cycle mechanism.

## Features
- **Scroll Up**: Increases right steering duty cycle (or decreases left if active)
- **Scroll Down**: Increases left steering duty cycle (or decreases right if active)
- **Duty Cycle Control**: 15 scroll steps from 0% to 100% duty cycle
- **Fixed Period**: 1/15 seconds (≈66.67ms) per cycle
- **Progressive Control**: Each scroll click adjusts the duty cycle by 1/15 (≈6.67%)
- **Toggle Control**: Press Numpad 0 to enable/disable the simulation

## How Duty Cycle Works

The duty cycle determines what percentage of each fixed time period (1/15 second) the steering key is held down:

- **Scroll count 1**: Duty cycle = 1/15 (≈6.67%) - key pressed for ≈4.4ms every 66.67ms
- **Scroll count 7**: Duty cycle = 7/15 (≈46.67%) - key pressed for ≈31.1ms every 66.67ms
- **Scroll count 15**: Duty cycle = 15/15 (100%) - key pressed continuously

### Scroll Behavior Example:
1. **Start**: Direction = None, Count = 0
2. **Scroll Up**: Direction = Right, Count = 1, Duty = 1/15 (D key pressed 6.67% of time)
3. **Scroll Up**: Direction = Right, Count = 2, Duty = 2/15 (D key pressed 13.33% of time)
4. **...continue scrolling up 13 more times...**
5. **Scroll Up**: Direction = Right, Count = 15, Duty = 15/15 (D key pressed 100% of time)
6. **Scroll Down**: Direction = Right, Count = 14, Duty = 14/15 (decreases right steering)
7. **...continue scrolling down 14 more times...**
8. **Scroll Down**: Direction = None, Count = 0 (neutral position)
9. **Scroll Down**: Direction = Left, Count = 1, Duty = 1/15 (A key pressed 6.67% of time)

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
- **Scroll Mouse Up**: Increase right steering duty cycle (or decrease left if active)
- **Scroll Mouse Down**: Increase left steering duty cycle (or decrease right if active)
- **Numpad 0**: Toggle the simulation ON/OFF
- **Ctrl+C**: Exit the program

The script starts in **disabled** mode. Press Numpad 0 to enable it.

## How It Works

The script uses the `pynput` library to:
1. Listen to mouse scroll events
2. Listen to keyboard events (for the toggle key)
3. Control key presses (A or D) using a duty cycle mechanism

The duty cycle mechanism works with a fixed period of 1/15 seconds (≈66.67ms). Each scroll event adjusts the scroll count (0-15), which determines what percentage of each period the steering key is held down. For example:
- At scroll count 5: The key is pressed for 5/15 (≈33.33%) of each period
- At scroll count 15: The key is pressed for 15/15 (100%) of each period

This provides smooth, progressive steering control with 15 distinct levels from neutral to full lock in each direction.

## Notes

- This script requires appropriate permissions to listen to input events and simulate key presses
- On Linux, you may need to run with appropriate permissions or add your user to the `input` group
- The script runs in the background and can be stopped with Ctrl+C
