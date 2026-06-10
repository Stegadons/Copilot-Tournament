"""
Flask aplikācijas entry-point

"""

from flask import Flask, request, redirect, url_for, render_template
import json
import os

from services import auth_service
from services import tournament_service
from services import bracket_service

STATUS_LABELS = {
    "not_started": "Nav sācies",
    "in_progress": "Notiek",
    "finished": "Pabeigts"
}


def _all_matches_finished(round_obj):
    return all(m.get('winner_id') is not None for m in round_obj.get('matches', []))


def _numeric_rounds(rounds):
    return [r for r in rounds if isinstance(r.get('round'), int)]


def _final_finished(rounds):
    numeric = _numeric_rounds(rounds)
    if not numeric:
        return False
    last = numeric[-1]
    return len(last['matches']) == 1 and _all_matches_finished(last)


def create_app():
    app = Flask(__name__)

    # ===== Konfigurācijas ielāde =====
    config_path = os.environ.get("CONFIG_PATH", "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Nav atrasts konfigurācijas fails: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    app.config['SECRET_KEY'] = config['secret_key']
    app.config['DATA_FILE'] = config['data_file']
    app.config['ADMINS'] = config.get('admins', [])

    # ===== Viewer =====
    @app.route('/')
    def index():
        return redirect(url_for('viewer_bracket'))

    @app.route('/viewer/bracket')
    def viewer_bracket():
        data = tournament_service.load_tournament(app.config['DATA_FILE'])
        return render_template(
            'viewer_bracket.html',
            rounds=data.get('rounds', [])
        )

    @app.route('/viewer/standings')
    def viewer_standings():
        data = tournament_service.load_tournament(app.config['DATA_FILE'])
        standings = bracket_service.calculate_standings(
            data.get('players', []),
            data.get('rounds', [])
        )
        return render_template(
            'viewer_standings.html',
            standings=standings
        )

    # ===== Admin autentifikācija =====
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        error = None

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                error = "Lūdzu ievadiet lietotājvārdu un paroli"
            elif auth_service.verify_credentials(username, password):
                auth_service.login_user(username)
                return redirect(url_for('admin_dashboard'))
            else:
                error = "Nepareizs lietotājvārds vai parole"

        return render_template('admin_login.html', error=error)

    @app.route('/admin/logout')
    def admin_logout():
        auth_service.logout_user()
        return redirect(url_for('index'))

    # ===== Admin dashboard =====
    @app.route('/admin')
    @auth_service.login_required
    def admin_dashboard():
        data = tournament_service.load_tournament(app.config['DATA_FILE'])
        status_code = data.get('status', 'not_started')
        return render_template(
            'admin_dashboard.html',
            players=len(data.get('players', [])),
            status=STATUS_LABELS.get(status_code, status_code)
        )

    # ===== Spēlētāji =====
    @app.route('/admin/players/add', methods=['POST'])
    @auth_service.login_required
    def admin_add_player():
        name = request.form.get('name')
        if name:
            tournament_service.add_player(app.config['DATA_FILE'], name)
        return redirect(url_for('admin_dashboard'))

    # ===== Bracket =====
    @app.route('/admin/bracket/generate', methods=['POST'])
    @auth_service.login_required
    def admin_generate_bracket():
        data = tournament_service.load_tournament(app.config['DATA_FILE'])
        data['rounds'] = bracket_service.generate_initial_bracket(data.get('players', []))
        data['status'] = 'in_progress'
        tournament_service.save_tournament(app.config['DATA_FILE'], data)
        return redirect(url_for('admin_rounds'))

    # ===== Raundi =====
    @app.route('/admin/rounds')
    @auth_service.login_required
    def admin_rounds():
        data = tournament_service.load_tournament(app.config['DATA_FILE'])
        return render_template(
            'admin_rounds.html',
            rounds=data.get('rounds', [])
        )

    @app.route('/admin/match/winner', methods=['POST'])
    @auth_service.login_required
    def admin_set_winner():
        data = tournament_service.load_tournament(app.config['DATA_FILE'])
        rounds = data.get('rounds', [])

        round_no = request.form.get('round')
        match_id = request.form.get('match')
        winner_id = request.form.get('winner')

        if not (round_no and match_id and winner_id):
            return redirect(url_for('admin_rounds'))

        # ===== 3. vietas raunds =====
        if round_no == 'third_place':
            for r in rounds:
                if r.get('round') == 'third_place':
                    r['matches'][0]['winner_id'] = int(winner_id)
                    break

            if _final_finished(rounds):
                data['status'] = 'finished'

        # ===== Skaitliskie raundi =====
        else:
            bracket_service.set_match_winner(
                rounds,
                int(round_no),
                int(match_id), int(winner_id)
            )

            numeric = _numeric_rounds(rounds)
            last_numeric = numeric[-1]

            if _all_matches_finished(last_numeric):
                match_count = len(last_numeric['matches'])

                # STARPRAUNDS
                if match_count > 2:
                    bracket_service.generate_next_round(rounds)

                # PUSFINĀLS
                elif match_count == 2:
                    bracket_service.generate_next_round(rounds)

                    if not any(r.get('round') == 'third_place' for r in rounds):
                        try:
                            rounds.append(bracket_service.generate_third_place_round(rounds))
                        except ValueError:
                            # 3. vieta nav iespējama — turpinām bez tās
                            pass

                # FINĀLS
                elif match_count == 1:
                    # Ja 3.vieta nav vai nav iespējama — noslēdzam turnīru
                    third = next((r for r in rounds if r.get('round') == 'third_place'), None)
                    if not third or _all_matches_finished(third):
                        data['status'] = 'finished'

        tournament_service.save_tournament(app.config['DATA_FILE'], data)
        return redirect(url_for('admin_rounds'))

    # ===== Reset =====
    @app.route('/admin/reset/progress', methods=['POST'])
    @auth_service.login_required
    def admin_reset_progress():
        tournament_service.reset_progress(app.config['DATA_FILE'])
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/reset/all', methods=['POST'])
    @auth_service.login_required
    def admin_reset_all():
        tournament_service.reset_all(app.config['DATA_FILE'])
        return redirect(url_for('admin_dashboard'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
