import json
import random

def generate_score_update(player_id=None):
    return json.dumps({
        "type": "score_update",
        "player_id": player_id or random.randint(1, 4),
        "score": random.randint(0, 1000)
    })

def generate_player_position(player_id=None):
    return json.dumps({
        "type": "position",
        "player_id": player_id or random.randint(1, 4),
        "x": random.randint(0, 1920),
        "y": random.randint(0, 1080)
    })

def generate_chat_message():
    messages = ["GG!", "Wait!", "I'm lagging", "Amogus", "HELP ME"]
    return json.dumps({
        "type": "chat",
        "text": random.choice(messages)
    })

def generate_game_state_save():
    return json.dumps({
        "type": "state_save",
        "timestamp": random.randint(100000, 999999),
        "players": [generate_player_position(i) for i in range(1, 3)]
    })


def is_reliable_event(event_json):
    event = json.loads(event_json)
    if event["type"] == "score_update":
        return random.random() < 0.8  # 80% of scores are reliable
    if event["type"] == "state_save":
        return True
    return False