import time
import random
from ..core.game_net_api import GameNetAPI
from .game_data import (
    generate_score_update,
    generate_player_position,
    generate_chat_message,
    generate_game_state_save,
    is_reliable_event
)

def run_sender(duration=30, packet_rate=20):
    """
    Send realistic game traffic for a fixed duration.
    Recommended: duration=30s, packet_rate=20pps (per assignment spec)
    """
    api = GameNetAPI(port=8888, target_port=8889)
    start_time = time.time()
    interval = 1.0 / packet_rate
    event_generators = [
        generate_score_update,
        generate_player_position,
        generate_chat_message,
        generate_game_state_save
    ]

    print(f"[SENDER] Starting demo: {duration}s at ~{packet_rate} pps")
    try:
        while time.time() - start_time < duration:
            gen = random.choice(event_generators)
            payload = gen()
            reliable = is_reliable_event(payload)

            api.send(payload, reliable=reliable, timestamp=int(time.time()))

            if time.time() - start_time < 3:  # only log first 3 sec
                chan = "RELIABLE" if reliable else "UNRELIABLE"
                print(f"[SEND] {chan}: {payload[:50]}...")

            time.sleep(interval)
    finally:
        api.close()
        print(f"[SENDER] Demo finished after {duration} seconds.")