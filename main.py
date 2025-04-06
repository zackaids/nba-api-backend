# Things to add to the NBA stats website

# 1. Live & Historical Stats
# 2. Player Comparisons (Stats side by side)
# 3. Chatbot
# 4. Predictive Analytics (ML)
# 5. Data Visuals
# 6. Fantasy League helper
# 7. User Accounts/Social Media

import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, teamyearbyyearstats, leagueleaders, leaguedashplayerstats, leaguedashteamstats
from nba_api.live.nba.endpoints import scoreboard
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS(app)

@app.route('/')
def home():
    return "NBA Stats Backend is running!"

@app.route("/player/<name>", methods=["GET"])
def get_player_stats(name):
    player_dict = players.find_players_by_full_name(name)
    if not player_dict:
        return jsonify({"error": "Player not found"}), 404
    
    player_id = player_dict[0]["id"]
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame'
    )
    df = player_stats.get_data_frames()[0]
    player_data = df[df['PLAYER_ID'] == player_id]
    
    if player_data.empty:
        return jsonify({"error": "No stats available for this season"}), 404
    
    player_data = player_data.iloc[0].to_dict()
    for key, value in player_data.items():
        if pd.api.types.is_integer_dtype(type(value)):
            player_data[key] = int(value)
        elif pd.api.types.is_float_dtype(type(value)):
            player_data[key] = float(value)
    
    result = {
        "PLAYER_NAME": str(player_data['PLAYER_NAME']),
        "TEAM_ABBREVIATION": str(player_data['TEAM_ABBREVIATION']),
        "GP": int(player_data['GP']),
        "PTS": float(player_data['PTS']),
        "AST": float(player_data['AST']),
        "REB": float(player_data['REB']),
        "STL": float(player_data['STL']),
        "BLK": float(player_data['BLK']),
        "FG_PCT": float(player_data['FG_PCT']),
        "FG3_PCT": float(player_data['FG3_PCT']),
        "FT_PCT": float(player_data['FT_PCT']),
        "TOV": float(player_data['TOV'])
    }
    
    return jsonify([result])
# /team_stats/<team_id>
# function for getting team stats
@app.route("/team_stats/<team_id>")
def get_team_stats(team_id):
    team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id)
    stats_df = team_stats.get_data_frames()[0]
    return jsonify(stats_df.to_dict(orient="records"))
# 1610612747 lakers id

@app.route("/api/live_scores")
def get_live_scores():
    games = scoreboard.ScoreBoard()
    games_data = games.get_dict()

    live_scores = []
    
    for game in games_data["scoreboard"]["games"]:
        live_scores.append({
            "home_team": game["homeTeam"]["teamName"],
            "home_score": game["homeTeam"]["score"],
            "away_team": game["awayTeam"]["teamName"],
            "away_score": game["awayTeam"]["score"],
            "game_status": game["gameStatusText"] 
        })    
    return jsonify(live_scores)

@app.route("/api/stats_leaders/ppg")
def get_points_leaders():
    leaders = leagueleaders.LeagueLeaders(
        stat_category_abbreviation='PTS',
        season_type_all_star='Regular Season',
        per_mode48='PerGame'
    )
    df = leaders.get_data_frames()[0].head(5)
    results = []
    
    for _, row in df.iterrows():
        results.append({
            'player_name': row['PLAYER'],
            'player_id': row['PLAYER_ID'],
            'team_name': row['TEAM'],
            'stat_value': f"{row['PTS']:.1f}"
        })
    
    return jsonify(results)

@app.route("/api/stats_leaders/rpg")
def get_rebound_leaders():
    leaders = leagueleaders.LeagueLeaders(
        stat_category_abbreviation='REB',
        season_type_all_star='Regular Season',
        per_mode48='PerGame'
    )
    df = leaders.get_data_frames()[0].head(5)
    results = []
    
    for _, row in df.iterrows():
        results.append({
            'player_name': row['PLAYER'],
            'player_id': row['PLAYER_ID'],
            'team_name': row['TEAM'],
            'stat_value': f"{row['REB']:.1f}"
        })
    
    return jsonify(results)

@app.route("/api/stats_leaders/apg")
def get_assist_leaders():
    leaders = leagueleaders.LeagueLeaders(
        stat_category_abbreviation='AST',
        season_type_all_star='Regular Season',
        per_mode48='PerGame'
    )
    df = leaders.get_data_frames()[0].head(5)
    results = []
    
    for _, row in df.iterrows():
        results.append({
            'player_name': row['PLAYER'],
            'player_id': row['PLAYER_ID'],
            'team_name': row['TEAM'],
            'stat_value': f"{row['AST']:.1f}"
        })
    
    return jsonify(results)

@app.route("/api/stats_leaders/spg")
def get_steal_leaders():
    leaders = leagueleaders.LeagueLeaders(
        stat_category_abbreviation='STL',
        season_type_all_star='Regular Season',
        per_mode48='PerGame'
    )
    df = leaders.get_data_frames()[0].head(5)
    results = []
    
    for _, row in df.iterrows():
        results.append({
            'player_name': row['PLAYER'],
            'player_id': row['PLAYER_ID'],
            'team_name': row['TEAM'],
            'stat_value': f"{row['STL']:.1f}"
        })
    
    return jsonify(results)

@app.route("/api/stats_leaders/bpg")
def get_block_leaders():
    leaders = leagueleaders.LeagueLeaders(
        stat_category_abbreviation='BLK',
        season_type_all_star='Regular Season',
        per_mode48='PerGame'
    )
    df = leaders.get_data_frames()[0].head(5)
    results = []
    
    for _, row in df.iterrows():
        results.append({
            'player_name': row['PLAYER'],
            'player_id': row['PLAYER_ID'],
            'team_name': row['TEAM'],
            'stat_value': f"{row['BLK']:.1f}"
        })
    
    return jsonify(results)

@app.route("/api/stats_leaders/fgp")
def get_fg_percentage_leaders():
    leaders = leaguedashplayerstats.LeagueDashPlayerStats(
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame'
    )
    df = leaders.get_data_frames()[0]
    filtered_df = df[df['FGA'] >= 5].sort_values('FG_PCT', ascending=False).head(5)
    results = []
    
    for _, row in filtered_df.iterrows():
        results.append({
            'player_name': row['PLAYER_NAME'],
            'player_id': row['PLAYER_ID'],
            'team_name': row['TEAM_ABBREVIATION'],
            'stat_value': f"{row['FG_PCT'] * 100:.1f}%"
        })
    
    return jsonify(results)

@app.route("/api/stats_leaders/3pp")
def get_3p_percentage_leaders():
    leaders = leaguedashplayerstats.LeagueDashPlayerStats(
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame'
    )
    df = leaders.get_data_frames()[0]
    filtered_df = df[df['FG3A'] >= 1].sort_values('FG3_PCT', ascending=False).head(5)
    results = []
    
    for _, row in filtered_df.iterrows():
        results.append({
            'player_name': row['PLAYER_NAME'],
            'player_id': row['PLAYER_ID'],
            'team_name': row['TEAM_ABBREVIATION'],
            'stat_value': f"{row['FG3_PCT'] * 100:.1f}%"
        })
    
    return jsonify(results)

@app.route("/api/stats_leaders/ftp")
def get_ft_percentage_leaders():
    leaders = leaguedashplayerstats.LeagueDashPlayerStats(
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame'
    )
    df = leaders.get_data_frames()[0]
    filtered_df = df[df['FTA'] >= 1].sort_values('FT_PCT', ascending=False).head(5)
    results = []
    
    for _, row in filtered_df.iterrows():
        results.append({
            'player_name': row['PLAYER_NAME'],
            'player_id': row['PLAYER_ID'],
            'team_name': row['TEAM_ABBREVIATION'],
            'stat_value': f"{row['FT_PCT'] * 100:.1f}%"
        })
    
    return jsonify(results)

@app.route("/api/stats_leaders/all")
def get_all_stats_leaders():
    def response_to_dict(response):
        return response.get_json()
    stats = {
        'points': response_to_dict(get_points_leaders()),
        'rebounds': response_to_dict(get_rebound_leaders()),
        'assists': response_to_dict(get_assist_leaders()), 
        'steals': response_to_dict(get_steal_leaders()),
        'blocks': response_to_dict(get_block_leaders()),
        'fieldgoal': response_to_dict(get_fg_percentage_leaders()),
        'threepoint': response_to_dict(get_3p_percentage_leaders()),
        'freethrow': response_to_dict(get_ft_percentage_leaders())
    }
    
    return jsonify(stats)

# rebounds
# assists
# steals
# blocks
# fieldgoal
# threepoint
# freethrow

@app.route("/api/team_stats_leaders/ppg")
def get_team_points_leaders():
    team_stats = leaguedashteamstats.LeagueDashTeamStats(
        season_type_all_star="Regular Season",
        per_mode_detailed="PerGame"
    )
    df = team_stats.get_data_frames()[0].sort_values("PTS", ascending=False).head(5)
    results = []
    for _, row in df.iterrows():
        results.append({
            "team_name": row["TEAM_NAME"],
            "team_id": row["TEAM_ID"],
            "stat_value": f"{row["PTS"]:.1f}"
        })
    return jsonify(results)




@app.route("/api/team_stats_leaders/all")
def get_all_team_stats_leaders():
    def response_to_dict(response):
        return response.get_json()

    stats = {
        'points': response_to_dict(get_team_points_leaders()),
        # 'rebounds': response_to_dict(get_team_rebound_leaders()),
        # 'assists': response_to_dict(get_team_assist_leaders()), 
        # 'steals': response_to_dict(get_team_steal_leaders()),
        # 'blocks': response_to_dict(get_team_block_leaders()),
        # 'fieldgoal': response_to_dict(get_team_fg_percentage_leaders()),
        # 'threepoint': response_to_dict(get_team_3p_percentage_leaders()),
        # 'freethrow': response_to_dict(get_team_ft_percentage_leaders()),
        # 'wins': response_to_dict(get_team_wins_leaders()),
        # 'losses': response_to_dict(get_team_losses_leaders()),
        # 'winpct': response_to_dict(get_team_win_pct_leaders())
    }
    
    return jsonify(stats)

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True, port=os.getenv("PORT", default=5000))


# annotated-types==0.7.0
# blinker==1.9.0
# cachetools==5.5.2
# certifi==2025.1.31
# charset-normalizer==3.4.1
# click==8.1.8
# colorama==0.4.6
# Flask==3.1.0
# flask-cors==5.0.1
# grpcio==1.70.0
# grpcio-status==1.70.0
# gunicorn==20.1.0
# httplib2==0.22.0
# idna==3.10
# itsdangerous==2.2.0
# Jinja2==3.1.6
# MarkupSafe==3.0.2
# nba_api==1.7.0
# numpy
# pandas==2.2.3
# proto-plus==1.26.0
# protobuf==5.29.3
# pyasn1==0.6.1
# pyasn1_modules==0.4.1
# pydantic==2.10.6
# pydantic_core==2.27.2
# pyparsing==3.2.1
# python-dateutil==2.9.0.post0
# pytz==2025.1
# requests==2.32.3
# rsa==4.9
# six==1.17.0
# tqdm==4.67.1
# typing_extensions==4.12.2
# tzdata==2025.1
# uritemplate==4.1.1
# urllib3==2.3.0
# Werkzeug==3.1.3