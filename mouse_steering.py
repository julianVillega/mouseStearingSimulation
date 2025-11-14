#!/usr/bin/env python3
"""
Mouse Steering Simulation
Simulates steering wheel behavior by reading mouse scroll events
and tapping A/D keys accordingly.
"""

import threading
import time
from pynput import mouse, keyboard

# Constants
MAX_FREQUENCY = 1 / 15  # Maximum tapping frequency (15 times per second)
MIN_FREQUENCY = 0  # Minimum frequency (no tapping)

# Global state
enabled = False
current_direction = None  # 'left' or 'right' or None
scroll_intensity = 0  # Controls tapping speed
lock = threading.Lock()
tapping_thread = None
stop_tapping = threading.Event()


def calculate_tap_delay(intensity):
    """
    Calculate delay between key taps based on scroll intensity.
    Returns delay in seconds. Returns None if no tapping should occur.
    """
    if intensity == 0:
        return None
    
    # Map intensity to frequency (0 to MAX_FREQUENCY)
    # Higher intensity = higher frequency = lower delay
    frequency = min(abs(intensity) * MAX_FREQUENCY, MAX_FREQUENCY)
    
    if frequency <= MIN_FREQUENCY:
        return None
    
    return 1 / frequency


def tap_key_continuously():
    """
    Continuously tap the appropriate key based on current direction and intensity.
    """
    global current_direction, scroll_intensity
    
    keyboard_controller = keyboard.Controller()
    
    while not stop_tapping.is_set():
        with lock:
            direction = current_direction
            intensity = scroll_intensity
        
        if direction and intensity > 0:
            delay = calculate_tap_delay(intensity)
            
            if delay:
                # Tap the appropriate key
                key_to_press = 'a' if direction == 'left' else 'd'
                keyboard_controller.press(key_to_press)
                keyboard_controller.release(key_to_press)
                
                # Wait before next tap
                time.sleep(delay)
            else:
                time.sleep(0.01)  # Small sleep to prevent busy waiting
        else:
            time.sleep(0.01)  # Small sleep to prevent busy waiting


def on_scroll(x, y, dx, dy):
    """
    Handle mouse scroll events.
    Scroll up (dy > 0) turns right (D key)
    Scroll down (dy < 0) turns left (A key)
    """
    global current_direction, scroll_intensity, tapping_thread
    
    if not enabled:
        return
    
    with lock:
        if dy > 0:
            # Scroll up - turn right
            current_direction = 'right'
            scroll_intensity = abs(dy)
        elif dy < 0:
            # Scroll down - turn left
            current_direction = 'left'
            scroll_intensity = abs(dy)
        
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
    global enabled, current_direction, scroll_intensity
    
    try:
        # Check for numpad 0
        if hasattr(key, 'vk') and key.vk == 96:  # VK code for numpad 0
            enabled = not enabled
            print(f"Mouse steering {'ENABLED' if enabled else 'DISABLED'}")
            
            if not enabled:
                # Reset state when disabling
                with lock:
                    current_direction = None
                    scroll_intensity = 0
    except AttributeError:
        pass


def main():
    """
    Main function to start the mouse steering simulation.
    """
    print("Mouse Steering Simulation")
    print("=" * 50)
    print("Controls:")
    print("  - Scroll UP: Turn right (taps D key)")
    print("  - Scroll DOWN: Turn left (taps A key)")
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
