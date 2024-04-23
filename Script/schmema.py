schemas = {
    "teamf": "teamf(team_id, full_name, abbreviation, nickname, year_founded)",
    "combinef": "combinef(player_id, season, wingspan, standing_reach, hand_width, hand_length, bench_press, standing_vertical_leap, three_quarter_sprint)",
    "playerf": "playerf(player_id, first_name, last_name, is_active)",
    "front_officef": "front_officef(team_id, city, state, owner, head_coach, general_manager)",
    "social_mediaf": "social_mediaf(team_id, facebook, instagram, twitter)",
    "arenaf": "arenaf(team_id, arena_name, arena_capacity)",
    "draftf": "draftf(player_id, season, team_drafted_to_id, round_number, round_pick, overall_pick_number)",
    "officialf": "officialf(official_id, game_id, first_name, last_name, jersey_num)",
    "attributesf": "attributesf(player_id, team_id, birth_date, country, height, weight, position, seasons_in_nba, Jersey_num)",
    "inactivesf": "inactivesf(game_id, player_id, team_id, jersey_num)",
    "gamef": "gamef(game_id, home_team_id, away_team_id, home_team_result, points_home, points_away, rebounds_home, rebounds_away, assists_home, assists_away, game_type)",
    "game_contextf": "game_contextf(game_id, season, national_tv_broadcaster, game_date, attendance, game_time)",
    "line_scoref": "line_scoref(game_id, home_team_id, away_team_id, pts_qtr1_home, pts_qtr2_home, pts_qtr3_home, pts_qtr4_home, pts_qtr1_away, pts_qtr2_away, pts_qtr3_away, pts_qtr4_away)"
}
schemasArguments = {
    'teamf': ['team_id', 'full_name', 'abbreviation', 'nickname', 'year_founded'],
    'combinef': ['player_id', 'season', 'wingspan', 'standing_reach', 'hand_width', 'hand_length', 'bench_press', 'standing_vertical_leap', 'three_quarter_sprint'],
    'playerf': ['player_id', 'first_name', 'last_name', 'is_active'],
    'front_officef': ['team_id', 'city', 'state', 'owner', 'head_coach', 'general_manager'],
    'social_mediaf': ['team_id', 'facebook', 'instagram', 'twitter'],
    'arenaf': ['team_id', 'arena_name', 'arena_capacity'],
    'draftf': ['player_id', 'season', 'team_drafted_to_id', 'round_number', 'round_pick', 'overall_pick_number'],
    'officialf': ['official_id', 'game_id', 'first_name', 'last_name', 'jersey_num'],
    'attributesf': ['player_id', 'team_id', 'birth_date', 'country', 'height', 'weight', 'position', 'seasons_in_nba', 'Jersey_num'],
    'inactivesf': ['game_id', 'player_id', 'team_id', 'jersey_num'],
    'gamef': ['game_id', 'home_team_id', 'away_team_id', 'home_team_result', 'points_home', 'points_away', 'rebounds_home', 'rebounds_away', 'assists_home', 'assists_away', 'game_type'],
    'game_contextf': ['game_id', 'season', 'national_tv_broadcaster', 'game_date', 'attendance', 'game_time'],
    'line_scoref': ['game_id', 'home_team_id', 'away_team_id', 'pts_qtr1_home', 'pts_qtr2_home', 'pts_qtr3_home', 'pts_qtr4_home', 'pts_qtr1_away', 'pts_qtr2_away', 'pts_qtr3_away', 'pts_qtr4_away']
}