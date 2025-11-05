from ..core.game_net_api import GameNetAPI
import json
import time

def run_receiver():
    api = GameNetAPI(port=8889, target_port=8888)
    print("[RECEIVER] Waiting for packets...")

    try:
        while True:
            result = api.receive()
            if result is None:
                continue

            #game packet
            payload = result.payload
            seq_no = result.seq_no
            channel_type = result.channel_type
            latency_ms = (time.time() - result.timestamp) * 1000
            # print(f"timestamp: {result.timestamp}, time: {time.time()}")
            chan = "RELIABLE" if channel_type == 0 else "UNRELIABLE"

            try:
                parsed = json.loads(payload)
                payload_str = json.dumps(parsed, separators=(',', ':'))
            except:
                payload_str = payload

            print(f"[RECV] #{seq_no} {chan}: {payload_str} ({latency_ms:.1f}ms)")

    except KeyboardInterrupt:
        print("\n[RECEIVER] Stopped.")
    finally:
        api.close()