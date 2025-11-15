#!/usr/bin/env python3
"""
Mouse Steering Simulation
Simulates steering wheel behavior by reading mouse scroll events
and controlling keys with a duty cycle.
"""

import threading
import time
from pynput import mouse, keyboard

# Constants
DUTY_CYCLE_PERIOD = 1.0 / 15.0  # Fixed period: 1/15 seconds (≈66.67ms)
MAX_SCROLL_STEPS = 15  # Maximum scroll steps for 100% duty cycle

# Global state
enabled = False
current_direction = None  # 'left' or 'right' or None
scroll_count = 0  # Number of scroll steps (0-15), determines duty cycle percentage
lock = threading.Lock()
tapping_thread = None
stop_tapping = threading.Event()


def calculate_duty_cycle(scroll_count):
    """
    Calculate duty cycle percentage based on scroll count.
    Returns the duty cycle as a value between 0.0 and 1.0.
    
    scroll_count ranges from 1 to 15, where:
    - 1 corresponds to 1/15 duty cycle (≈6.67%)
    - 15 corresponds to 15/15 duty cycle (100%)
    """
    if scroll_count <= 0:
        return 0.0
    
    # Duty cycle = scroll_count / MAX_SCROLL_STEPS
    return min(scroll_count / MAX_SCROLL_STEPS, 1.0)


def tap_key_continuously():
    """
    Continuously control the appropriate key based on current direction and duty cycle.
    Uses a fixed period (1/15 seconds) with variable duty cycle (0-100%).
    """
    global current_direction, scroll_count
    
    keyboard_controller = keyboard.Controller()
    
    while not stop_tapping.is_set():
        with lock:
            direction = current_direction
            count = scroll_count
        
        if direction and count > 0:
            # Calculate duty cycle (percentage of time key should be pressed)
            duty_cycle = calculate_duty_cycle(count)
            
            # Calculate how long to hold the key and how long to release
            press_duration = DUTY_CYCLE_PERIOD * duty_cycle
            release_duration = DUTY_CYCLE_PERIOD * (1.0 - duty_cycle)
            
            # Determine which key to press
            key_to_press = 'a' if direction == 'left' else 'd'
            
            # Press and hold the key for the duty cycle duration
            if press_duration > 0:
                keyboard_controller.press(key_to_press)
                time.sleep(press_duration)
                keyboard_controller.release(key_to_press)
            
            # Wait for the rest of the period
            if release_duration > 0:
                time.sleep(release_duration)
        else:
            time.sleep(0.01)  # Small sleep to prevent busy waiting


def on_scroll(x, y, dx, dy):
    """
    Handle mouse scroll events with duty cycle control.
    
    Scroll behavior:
    - When scroll_count is 0, scrolling up sets direction to 'right', scrolling down sets to 'left'
    - Scroll up increases the duty cycle (scroll_count++)
    - Scroll down decreases the duty cycle (scroll_count--)
    - When scroll_count reaches 0, the direction can be switched
    
    Examples:
    - Start: count=0, dir=None
    - Scroll up: count=1, dir='right', duty=1/15
    - Scroll up: count=2, dir='right', duty=2/15
    - ... (continue scrolling up)
    - Scroll up: count=15, dir='right', duty=15/15 (100%)
    - Scroll down: count=14, dir='right', duty=14/15
    - ... (continue scrolling down)
    - Scroll down: count=1, dir='right', duty=1/15
    - Scroll down: count=0, dir=None (neutral)
    - Scroll down: count=1, dir='left', duty=1/15
    """
    global current_direction, scroll_count, tapping_thread
    
    if not enabled:
        return
    
    with lock:
        if dy > 0:
            # Scroll up - increase duty cycle
            if current_direction == 'right' or current_direction is None:
                # Continue increasing right or start right from neutral
                current_direction = 'right'
                scroll_count = min(scroll_count + 1, MAX_SCROLL_STEPS)
            elif current_direction == 'left':
                # Decrease left duty cycle
                scroll_count = max(scroll_count - 1, 0)
                if scroll_count == 0:
                    current_direction = None
        elif dy < 0:
            # Scroll down - depends on current state
            if current_direction == 'left' or current_direction is None:
                # Continue increasing left or start left from neutral
                current_direction = 'left'
                scroll_count = min(scroll_count + 1, MAX_SCROLL_STEPS)
            elif current_direction == 'right':
                # Decrease right duty cycle
                scroll_count = max(scroll_count - 1, 0)
                if scroll_count == 0:
                    current_direction = None
        
        # Start tapping thread if not already running
        if tapping_thread is None or not tapping_thread.is_alive():
            stop_tapping.clear()
            tapping_thread = threading.Thread(target=tap_key_continuously, daemon=True)
            tapping_thread.start()


def on_press(key):
    """
    Handle keyboard press events.
    Numpad 0 toggles the script on/off.
    """
    global enabled, current_direction, scroll_count
    
    try:
        # Check for numpad 0
        if hasattr(key, 'vk') and key.vk == 96:  # VK code for numpad 0
            enabled = not enabled
            print(f"Mouse steering {'ENABLED' if enabled else 'DISABLED'}")
            
            if not enabled:
                # Reset state when disabling
                with lock:
                    current_direction = None
                    scroll_count = 0
    except AttributeError:
        pass


def main():
    """
    Main function to start the mouse steering simulation.
    """
    print("Mouse Steering Simulation - Duty Cycle Mode")
    print("=" * 50)
    print("Controls:")
    print("  - Scroll UP: Increase duty cycle (or decrease opposite direction)")
    print("  - Scroll DOWN: Increase left duty cycle (or decrease right)")
    print("  - Duty cycle: 0-100% over 15 scroll steps")
    print("  - Period: 1/15 seconds (fixed)")
    print("  - Numpad 0: Toggle ON/OFF")
    print("=" * 50)
    print("Press Ctrl+C to exit")
    print()
    print("Status: DISABLED (Press Numpad 0 to enable)")
    
    # Start listeners
    mouse_listener = mouse.Listener(on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_press)
    
    mouse_listener.start()
    keyboard_listener.start()
    
    try:
        # Keep the program running
        mouse_listener.join()
        keyboard_listener.join()
    except KeyboardInterrupt:
        print("\nExiting...")
        stop_tapping.set()
        mouse_listener.stop()
        keyboard_listener.stop()


if __name__ == "__main__":
    main()
