import socket
import time
from .packet import GamePacket
from .constants import *

class GameNetAPI:
    def __init__(self, host='localhost', port=8888, target_port=8889):
        self.host = host
        self.port = port
        self.target_port = target_port  # ← THIS WAS MISSING!
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self.socket.settimeout(0.1)
        self.next_seq = 0
        
        # Basic metrics for Person 4
        self.metrics = {
            'reliable_sent': 0,
            'unreliable_sent': 0, 
            'reliable_received': 0,
            'unreliable_received': 0,
            'total_latency': 0,
            'latency_count': 0
        }
    
    def send(self, data, reliable=True):
        """REQUIRED: Allow marking as reliable/unreliable"""
        channel = CHANNEL_RELIABLE if reliable else CHANNEL_UNRELIABLE
        packet = GamePacket(channel, self.next_seq, data)
        
        self.socket.sendto(packet.to_bytes(), (self.host, self.target_port))
        
        # Track metrics
        if reliable:
            self.metrics['reliable_sent'] += 1
        else:
            self.metrics['unreliable_sent'] += 1
            
        print(f"SENT #{self.next_seq} {'RELIABLE' if reliable else 'UNRELIABLE'}: {data[:20]}...")
        self.next_seq = (self.next_seq + 1) % 65536
        
    def receive(self):
        """REQUIRED: Receive and basic processing"""
        try:
            data, addr = self.socket.recvfrom(1024)
            packet = GamePacket.from_bytes(data)
            if packet:
                # Calculate latency (for Person 4's metrics)
                latency = (time.time() * 1000) - packet.timestamp
                self.metrics['total_latency'] += latency
                self.metrics['latency_count'] += 1
                
                if packet.channel_type == CHANNEL_RELIABLE:
                    self.metrics['reliable_received'] += 1
                else:
                    self.metrics['unreliable_received'] += 1
                
                print(f"RECV #{packet.seq_no} {'RELIABLE' if packet.channel_type == 0 else 'UNRELIABLE'}: "
                      f"{packet.payload[:20]}... ({latency:.1f}ms)")
                return packet
        except socket.timeout:
            pass
        return None
    
    def get_metrics(self):
        """REQUIRED: For Person 4's performance measurement"""
        return self.metrics.copy()
    
    def close(self):
        self.socket.close()