"""
Turnīra datu serviss
Atbild par turnīra stāvokļa ielādi, saglabāšanu un pamata manipulācijām.

POSMS 3 – realizācijas plāns
"""

import json
import os
from typing import List, Dict


def load_tournament(data_file: str) -> Dict:
    if not os.path.exists(data_file):
        return {
            "status": "not_started",
            "players": [],
            "rounds": []
        }
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_tournament(data_file: str, data: Dict):
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_player(data_file: str, name: str):
    data = load_tournament(data_file)
    next_id = max([p['id'] for p in data.get('players', [])], default=0) + 1
    data.setdefault('players', []).append({
        "id": next_id,
        "name": name
    })
    save_tournament(data_file, data)


def reset_progress(data_file: str):
    """
    Atstāj spēlētājus, bet pilnībā atiestata turnīra gaitu
    """
    data = load_tournament(data_file)

    data['rounds'] = []
    data['status'] = 'not_started'

    save_tournament(data_file, data)


def reset_all(data_file: str):
    """
    Pilnībā atiestata turnīru, dzēš arī spēlētājus
    """
    data = {
        "status": "not_started",
        "players": [],
        "rounds": []
    }
    save_tournament(data_file, data)


def delete_player(data_file: str, player_id: int):
    data = load_tournament(data_file)

    if data.get('rounds'):
        raise ValueError("Turnīrs jau sācies – spēlētājus dzēst nedrīkst")

    data['players'] = [
        p for p in data.get('players', [])
        if p.get('id') != player_id
    ]

    save_tournament(data_file, data)


def update_player(data_file: str, player_id: int, name: str):
    data = load_tournament(data_file)

    if data.get('rounds'):
        raise ValueError("Turnīrs jau sācies – spēlētājus labot nedrīkst")

    for p in data.get('players', []):
        if p.get('id') == player_id:
            p['name'] = name.strip() if name else p['name']
            break

    save_tournament(data_file, data)