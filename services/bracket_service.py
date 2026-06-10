"""
Bracket un turnīra loģikas serviss
Pilna, pašpietiekama realizācija saskaņā ar PPS un PPA.

Atbild par:
- sākotnējā bracket ģenerēšanu (single elimination)
- BYE loģiku
- uzvarētāju virzīšanu pa raundiem
- 3. vietas spēles izveidi
- rezultātu tabulas (standings) aprēķinu

POSMS 4 – realizācijas plāns
"""

import random
from typing import Dict, List

# ======================
# Bracket ģenerēšana
# ======================

def generate_initial_bracket(players: List[Dict]) -> List[Dict]:
    """
    Izveido pirmo raundu ar randomizētiem spēlētājiem un BYE, ja nepieciešams.
    """
    shuffled = players[:]
    random.shuffle(shuffled)

    matches = []
    match_id = 1

    # Ja nepāra skaits — pēdējais saņem BYE
    if len(shuffled) % 2 == 1:
        bye_player = shuffled.pop()
        matches.append({
            "id": match_id,
            "player1_id": bye_player['id'],
            "player2_id": None,
            "winner_id": bye_player['id'],
            "is_bye": True
        })
        match_id += 1

    # Pārējie pāri
    for i in range(0, len(shuffled), 2):
        matches.append({
            "id": match_id,
            "player1_id": shuffled[i]['id'],
            "player2_id": shuffled[i + 1]['id'],
            "winner_id": None,
            "is_bye": False
        })
        match_id += 1

    return [{
        "round": 1,
        "matches": matches
    }]

# ======================
# Uzvarētāja iestatīšana
# ======================

def set_match_winner(rounds: List[Dict], round_number: int, match_id: int, winner_id: int):
    for rnd in rounds:
        if rnd['round'] == round_number:
            for match in rnd['matches']:
                if match['id'] == match_id:
                    match['winner_id'] = winner_id
                    return
    raise ValueError('Mačs nav atrasts')

# ======================
# Nākamais raunds / turnīra beigas
# ======================

def generate_next_round(rounds: List[Dict]) -> bool:
    last_round = rounds[-1]

    # ja ir nepabeigti mači – neko nedara
    if any(m['winner_id'] is None for m in last_round['matches']):
        return False

    winners = [m['winner_id'] for m in last_round['matches']]

    # ✅ JA PALICIS VIENS UZVARĒTĀJS → TURNĪRS BEIDZAS
    if len(winners) == 1:
        return False

    matches = []
    match_id = 1

    # BYE tikai starpraundos, ne finālā
    if len(winners) % 2 == 1:
        bye = winners.pop()
        matches.append({
            "id": match_id,
            "player1_id": bye,
            "player2_id": None,
            "winner_id": bye,
            "is_bye": True
        })
        match_id += 1

    for i in range(0, len(winners), 2):
        matches.append({
            "id": match_id,
            "player1_id": winners[i],
            "player2_id": winners[i + 1],
            "winner_id": None,
            "is_bye": False
        })
        match_id += 1

    rounds.append({
        "round": last_round['round'] + 1,
        "matches": matches
    })

    return True

# ======================
# Spēle par 3. vietu
# ======================

def generate_third_place_round(rounds: List[Dict]) -> Dict:
    if len(rounds) < 2:
        raise ValueError('Nepietiek raundu 3. vietas spēlei')

    semifinals = rounds[-2]['matches']
    losers = []

    for m in semifinals:
        if not m['is_bye'] and m['winner_id'] is not None:
            loser = m['player1_id'] if m['winner_id'] != m['player1_id'] else m['player2_id']
            losers.append(loser)

    if len(losers) != 2:
        raise ValueError('Nav iespējams noteikt 3. vietas dalībniekus')

    return {
        "round": 'third_place',
        "matches": [{
            "id": 1,
            "player1_id": losers[0],
            "player2_id": losers[1],
            "winner_id": None,
            "is_bye": False
        }]
    }

# ======================
# Rezultātu tabula
# ======================

def calculate_standings(players: List[Dict], rounds: List[Dict]) -> List[Dict]:
    stats = {p['id']: {
        "id": p['id'],
        "name": p['name'],
        "wins": 0,
        "losses": 0,
        "games": 0
    } for p in players}

    final_winner = None
    final_loser = None
    third_winner = None
    third_loser = None

    # --- apstrādā visus mačus ---
    for rnd in rounds:
        for m in rnd['matches']:
            if m.get('is_bye'):
                if m.get('winner_id') is not None:
                    stats[m['winner_id']]['wins'] += 1
                continue

            if m.get('winner_id') is None:
                continue

            p1 = m['player1_id']
            p2 = m['player2_id']
            w = m['winner_id']
            l = p1 if w == p2 else p2

            stats[w]['wins'] += 1
            stats[l]['losses'] += 1
            stats[w]['games'] += 1
            stats[l]['games'] += 1

            # --- identificē finālu ---
            if isinstance(rnd.get('round'), int) and len(rnd.get('matches', [])) == 1:
                final_winner = w
                final_loser = l

            # --- identificē 3. vietas spēli ---
            if rnd.get('round') == 'third_place':
                third_winner = w
                third_loser = l

    # --- TOP4 (fiksētās vietas) ---
    top_ids = []

    if final_winner:
        top_ids.append(final_winner)
    if final_loser:
        top_ids.append(final_loser)
    if third_winner:
        top_ids.append(third_winner)
    if third_loser:
        top_ids.append(third_loser)

    # --- pārējie spēlētāji ---
    remaining = [
        stats[p_id]
        for p_id in stats
        if p_id not in top_ids
    ]

    remaining_sorted = sorted(
        remaining,
        key=lambda x: (
            -x['wins'],
            -(x['wins'] - x['losses']),
            x['name']
        )
    )

    # --- apvieno galarezultātu ---
    ordered = [stats[p_id] for p_id in top_ids if p_id in stats]
    result = ordered + remaining_sorted

    return result
