import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.apps.sender_app import run_sender
from src.apps.receiver_app import run_receiver

def main():
    print("Advanced Game Transport Demo")
    print("1) Sender (sends realistic game data)")
    print("2) Receiver (logs with retransmit/reorder info)")
    choice = input("Choose role (1/2): ").strip()

    if choice == "1":
        run_sender(duration=30, packet_rate=20)
    elif choice == "2":
        run_receiver()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()