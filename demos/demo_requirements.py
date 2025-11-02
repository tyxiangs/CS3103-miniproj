import sys
import os
# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.game_net_api import GameNetAPI
import time

def run_receiver():
    """Show packets arriving with sequence numbers and latency"""
    print("🎯 RECEIVER - Showing packet arrival with seq numbers & latency")
    receiver = GameNetAPI(port=8889, target_port=8888)
    
    count = 0
    while count < 10:  # Show 10 packets then stop
        packet = receiver.receive()
        if packet:
            count += 1
        time.sleep(0.1)
    
    metrics = receiver.get_metrics()
    print(f"📊 METRICS: {metrics}")
    receiver.close()

def run_sender():
    """Show reliable vs unreliable sending"""
    print("🎯 SENDER - Showing reliable vs unreliable channels")
    time.sleep(1)
    sender = GameNetAPI(port=8888, target_port=8889)
    
    # REQUIRED: Mark packets as reliable/unreliable
    sender.send("CRITICAL: Player score update", reliable=True)
    time.sleep(0.5)
    sender.send("FAST: Player movement data", reliable=False) 
    time.sleep(0.5)
    sender.send("CRITICAL: Game state save", reliable=True)
    time.sleep(0.5)
    sender.send("FAST: Voice chat packet", reliable=False)
    
    # Show metrics
    metrics = sender.get_metrics()
    print(f"📊 SENT: {metrics['reliable_sent']} reliable, {metrics['unreliable_sent']} unreliable")
    sender.close()

if __name__ == "__main__":
    print("CS3103 REQUIREMENTS DEMO")
    print("1. Receiver (see packets arrive)")
    print("2. Sender (see both channels)")
    
    choice = input("Choice (1/2): ")
    if choice == "1":
        run_receiver()
    else:
        run_sender()