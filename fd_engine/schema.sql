CREATE TABLE players (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(100),
    date_of_birth DATE,
    nationality VARCHAR(50),
    team VARCHAR(50),
    league VARCHAR(50),
    position VARCHAR(50),
    preferred_foot VARCHAR(5),
    data_source VARCHAR(50),
    metrics JSONB
);

CREATE TABLE player_vectors (
    player_id INT PRIMARY KEY REFERENCES players(player_id),
    embedding vector(53)
);

CREATE TABLE match_metadata (
    match_id INT PRIMARY KEY,
    competition_id INT,
    competition_name VARCHAR(100),
    season_id INT,
    season_name VARCHAR(50),
    home_team_id INT,
    home_team_name VARCHAR(100),
    away_team_id INT,
    away_team_name VARCHAR(100),
    match_date DATE,
    home_score INT,
    away_score INT
);

CREATE TABLE player_appearances (
    player_id INT REFERENCES players(player_id),
    match_id INT REFERENCES match_metadata(match_id),
    minutes_played INT,
    position_played VARCHAR(50),
    team_id INT,
    PRIMARY KEY (player_id, match_id)
);

CREATE TABLE processed_matches (
    match_id INT PRIMARY KEY,
    processed_at TIMESTAMP DEFAULT NOW(),
    source VARCHAR(50)
);

CREATE TABLE failed_matches (
    match_id INT PRIMARY KEY,
    failed_at TIMESTAMP DEFAULT NOW(),
    error_message TEXT,
    retry_count INT DEFAULT 0
);
