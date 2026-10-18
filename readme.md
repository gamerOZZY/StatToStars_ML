# StatToStars_ML 

**NBA Player Performance Classification using Machine Learning**

StatToStars_ML is a machine learning project focused on analyzing NBA player performance using historical season statistics. The project collects player statistics from NBA Stats, organizes the data into a Bronze layer, and establishes the foundation for building a classification model capable of distinguishing between good and poor individual seasons.

The project follows a data engineering approach inspired by the **Medallion Architecture**, separating raw data collection from subsequent data cleaning, transformation, feature engineering, and model development.

## Table of Contents

* [Project Overview](#project-overview)
* [Project Objectives](#project-objectives)
* [NBA API](#nba-api)
* [Data Architecture](#data-architecture)
* [Project Structure](#project-structure)
* [Bronze Layer](#bronze-layer)

  * [LeagueDashPlayerStats](#1-leaguedashplayerstats)
  * [Base Statistics](#11-base-statistics)
  * [Advanced Statistics](#12-advanced-statistics)
  * [LeagueDashPtStats](#2-leaguedashptstats)
* [Installation](#installation)
* [Data Extraction](#data-extraction)
* [Data Quality and Limitations](#data-quality-and-limitations)
* [Roadmap](#roadmap)
* [References](#references)

---

## Project Overview

Evaluating basketball players is a multidimensional problem. Traditional statistics such as points, rebounds, and assists provide useful information, but they do not fully describe a player's efficiency, defensive contributions, playmaking, or role within a team.

StatToStars_ML aims to build a dataset that captures several dimensions of NBA player performance.

The collected data includes:

* Traditional box-score statistics.
* Advanced efficiency and impact metrics.
* Shooting performance.
* Ball-handling and driving statistics.
* Passing and playmaking.
* Rebounding opportunities and outcomes.
* Defensive activity.
* Player movement and speed.
* Touches and possession-related statistics.

The initial dataset covers the following NBA seasons:

**2015-16 through 2025-26.**

The data is collected at the player-season level, using the regular season as the initial scope.

Each season is stored independently to facilitate historical analysis, data validation, and reproducible processing.

### Problem Definition

The intended machine learning task is binary classification.

The model will eventually receive a set of player statistics and predict whether the corresponding player-season satisfies a predefined performance criterion.

The prediction target will be defined during the data preparation and modeling stages.

A player's performance may vary between seasons, so the unit of observation is a **player in a specific season**, rather than a player throughout their entire career.

For example, a player may have different classifications in 2018-19 and 2023-24.

---

## Project Objectives

The project has the following objectives:

1. Collect historical NBA player statistics programmatically.
2. Build a structured dataset containing traditional and advanced statistics.
3. Preserve the original extracted data in a Bronze layer.
4. Prepare the data for cleaning, integration, and feature engineering.
5. Define a reproducible criterion for classifying player-season performance.
6. Train and evaluate machine learning classification models.
7. Identify which statistical features contribute most to the model's predictions.

The initial priority is to establish a reliable data collection pipeline before developing the classification model.

---

## NBA API

### What is the NBA API?

The NBA API is an interface through which applications can request structured basketball statistics and related information.

This project uses the Python package [`nba_api`](https://github.com/swar/nba_api), a community-maintained client that provides access to NBA.com statistics endpoints.

The package allows Python applications to send requests to the NBA Stats service and retrieve responses containing player statistics, team statistics, game information, and other basketball data.

The project primarily uses two endpoints:

* `LeagueDashPlayerStats`
* `LeagueDashPtStats`

### How does it work?

The general extraction process follows these steps:

1. Python initializes an endpoint using the `nba_api` package.
2. The request specifies parameters such as the season, season type, measurement type, and statistical aggregation mode.
3. The NBA Stats service processes the request.
4. The response is parsed into a Pandas DataFrame.
5. The DataFrame is exported to a CSV file.
6. The CSV is stored in the Bronze layer for subsequent processing.

For example, a request can retrieve the advanced statistics of NBA players during the 2023-24 regular season.

The returned data contains one or more records for players, depending on the endpoint's parameters and the service's response.

### Important considerations

The Python package is a client for NBA Stats endpoints, not a guarantee of unrestricted or permanently stable API access.

Requests may be affected by:

* Rate limiting.
* Temporary server errors.
* Changes to endpoint parameters.
* Changes in available fields.
* Historical data availability.
* Network connectivity.

For this reason, the extraction scripts implement retry mechanisms and pauses between requests.

Extracted files are stored locally so that subsequent processing does not require repeatedly requesting the same data.

**Official statistics portal:** [NBA Stats](https://www.nba.com/stats/)

**Python client documentation:** [nba_api on GitHub](https://github.com/swar/nba_api)

---

## Data Architecture

The project follows the principles of the Medallion Architecture.

The data is organized into three main layers:

| Layer  | Purpose                                                             | Current status |
| ------ | ------------------------------------------------------------------- | -------------- |
| Bronze | Preserve the extracted source data in its original tabular form.    | Implemented    |
| Silver | Clean, validate, standardize, and integrate the extracted datasets. | Planned        |
| Gold   | Prepare analytical datasets and model-ready features.               | Planned        |

### Bronze

Bronze contains the raw CSV files extracted from the NBA Stats endpoints.

At this stage, the project does not attempt to define which players are good or bad.

The objective is to preserve the collected information so that later transformations can be performed reproducibly.

### Silver

Silver will be responsible for operations such as:

* Standardizing column names and data types.
* Handling missing values.
* Identifying duplicate records.
* Validating player and team identifiers.
* Checking consistency across seasons.
* Integrating different statistical datasets.
* Evaluating historical data availability.
* Documenting and applying eligibility criteria.

### Gold

Gold will contain datasets prepared for analytical and machine learning tasks.

Potential outputs include:

* Player-season feature tables.
* Derived performance indicators.
* Target labels.
* Training and testing datasets.
* Aggregated analytical datasets.

The classification target and final feature selection will be established after evaluating the quality and coverage of the collected data.

---

## Project Structure

```text
StatToStars_ML/
│
├── .vscode/
│   └── settings.json
│
├── data/
│   ├── bronze/
│   │   ├── league_dash_player_stats/
│   │   │   ├── advanced/
│   │   │   │   ├── season_2015-16.csv
│   │   │   │   ├── ...
│   │   │   │   └── season_2025-26.csv
│   │   │   │
│   │   │   └── base/
│   │   │       ├── season_2015-16.csv
│   │   │       ├── ...
│   │   │       └── season_2025-26.csv
│   │   │
│   │   ├── league_dash_pt_stats/
│   │   │   ├── season_2015-16/
│   │   │   │   ├── catchshoot.csv
│   │   │   │   ├── defense.csv
│   │   │   │   ├── drives.csv
│   │   │   │   ├── efficiency.csv
│   │   │   │   ├── elbowtouch.csv
│   │   │   │   ├── painttouch.csv
│   │   │   │   ├── passing.csv
│   │   │   │   ├── possessions.csv
│   │   │   │   ├── posttouch.csv
│   │   │   │   ├── pullupshot.csv
│   │   │   │   ├── rebounding.csv
│   │   │   │   └── speeddistance.csv
│   │   │   ├── ...
│   │   │   └── season_2025-26/
│   │   │       └── ... (the same 12 category files)
│   ├── gold/ (empty)
│   └── silver/ (empty)
│
├── notebooks/ (empty)
├── scripts/
│   ├── extraer_estadisticas_temporada.bat
│   └── extraer_estadisticas_tracking.bat
│
├── src/
│   ├── ETL/
│   │   ├── extraer_estadisticas_temporada.py
│   │   └── extraer_estadisticas_tracking.py
│   └── prueba.py
│
├── .gitignore
└── readme.md
```

The local `venv/` virtual environment is omitted because Git ignores it.

### Directory descriptions

| Directory or file                       | Description                                                                       |
| --------------------------------------- | --------------------------------------------------------------------------------- |
| `.vscode/`                              | Visual Studio Code workspace configuration.                                       |
| `data/`                                 | Stores the project's datasets.                                                    |
| `data/bronze/`                          | Contains raw data extracted from NBA Stats.                                       |
| `data/bronze/league_dash_player_stats/` | Contains traditional and advanced player statistics.                              |
| `data/bronze/league_dash_pt_stats/`     | Contains player tracking statistics organized by season and measurement category. |
| `data/silver/`                          | Reserved for cleaned and integrated datasets.                                     |
| `data/gold/`                            | Reserved for analytical and model-ready datasets.                                 |
| `notebooks/`                            | Reserved for exploratory data analysis, visualization, and experimentation.       |
| `scripts/`                              | Contains Windows batch scripts for running the extraction pipelines.              |
| `src/ETL/`                              | Contains Python scripts responsible for data extraction.                          |
| `.gitignore`                            | Defines files and directories that should not be tracked by Git.                  |
| `src/prueba.py`                         | Additional Python script located in the `src/` directory.                         |
| `readme.md`                             | Project documentation.                                                            |

The ellipses in the tree represent the intervening seasons from 2016-17 through 2024-25.

---

# Bronze Layer

The Bronze layer contains two main datasets:

1. `league_dash_player_stats`
2. `league_dash_pt_stats`

They provide complementary views of player performance.

`LeagueDashPlayerStats` supplies traditional and advanced season statistics, while `LeagueDashPtStats` provides more specialized measurements related to player tracking and on-court actions.

## 1. LeagueDashPlayerStats

### What is it?

`LeagueDashPlayerStats` is an NBA Stats endpoint that returns player statistics for a selected season and set of query parameters.

The project uses it to collect general statistics and advanced statistics for NBA players.

The extracted CSV files are organized by season.

### Why are there two folders?

The directory contains two subdirectories:

```text
league_dash_player_stats/
├── base/
└── advanced/
```

These folders correspond to two different values of the endpoint's `MeasureType` parameter.

#### Base

The `base/` directory contains traditional box-score statistics.

These include points, rebounds, assists, steals, blocks, shooting percentages, turnovers, fouls, and other conventional measurements.

They describe what players produced statistically during the season.

#### Advanced

The `advanced/` directory contains advanced basketball metrics.

These include shooting efficiency, usage, assist and rebound percentages, offensive and defensive ratings, pace, and other measurements intended to provide more context than traditional box-score statistics alone.

They help characterize efficiency, involvement, and broader aspects of performance.

### Why keep them separate?

Keeping the two measurement types in separate directories has several advantages:

* Each dataset retains its original schema.
* The source of each metric remains explicit.
* Different statistical families can be validated independently.
* The project avoids unnecessarily duplicating or merging columns during extraction.
* Later processing can select and integrate the relevant fields in Silver.

The two datasets can eventually be joined using the player identifier and season, provided that their record granularity and team representation are validated first.

### File naming convention

```text
season_2015-16.csv
season_2016-17.csv
season_2017-18.csv
...
season_2025-26.csv
```

Each file represents one season.

The season in the filename is the season requested from the endpoint, not the calendar year in which the CSV was downloaded.

---

## 1.1 Base Statistics

The Base dataset contains traditional player statistics and related ranking fields.

### Player and team identification

| Variable            | Description                                            |
| ------------------- | ------------------------------------------------------ |
| `PLAYER_ID`         | Unique identifier assigned to the player by NBA Stats. |
| `PLAYER_NAME`       | Player's full name as returned by the endpoint.        |
| `NICKNAME`          | Player's nickname or short name, when provided.        |
| `TEAM_ID`           | Identifier of the team associated with the record.     |
| `TEAM_ABBREVIATION` | Team abbreviation, such as BOS or LAL.                 |
| `AGE`               | Player's age as reported for the season.               |

### Games, wins, and participation

| Variable | Description                                                                      |
| -------- | -------------------------------------------------------------------------------- |
| `GP`     | Games played.                                                                    |
| `W`      | Team wins associated with the player's record.                                   |
| `L`      | Team losses associated with the player's record.                                 |
| `W_PCT`  | Winning percentage associated with the record.                                   |
| `MIN`    | Average minutes played per game when the endpoint is requested in per-game mode. |

**Important:** `W`, `L`, and `W_PCT` describe team results associated with a player's record. They are not individual measures of player quality.

### Shooting statistics

| Variable  | Description                        |
| --------- | ---------------------------------- |
| `FGM`     | Field goals made.                  |
| `FGA`     | Field goals attempted.             |
| `FG_PCT`  | Field-goal percentage.             |
| `FG3M`    | Three-point field goals made.      |
| `FG3A`    | Three-point field goals attempted. |
| `FG3_PCT` | Three-point shooting percentage.   |
| `FTM`     | Free throws made.                  |
| `FTA`     | Free throws attempted.             |
| `FT_PCT`  | Free-throw percentage.             |

A shooting percentage is generally calculated as made shots divided by attempted shots. A zero-attempt case may produce a missing or otherwise specially represented percentage.

### Rebounding and playmaking

| Variable | Description         |
| -------- | ------------------- |
| `OREB`   | Offensive rebounds. |
| `DREB`   | Defensive rebounds. |
| `REB`    | Total rebounds.     |
| `AST`    | Assists.            |

### Defensive statistics

| Variable | Description                                                     |
| -------- | --------------------------------------------------------------- |
| `STL`    | Steals.                                                         |
| `BLK`    | Blocks credited to the player.                                  |
| `BLKA`   | Shots blocked against the player while the player was shooting. |

`BLK` and `BLKA` describe different events and should not be treated as interchangeable.

### Turnovers and fouls

| Variable | Description                         |
| -------- | ----------------------------------- |
| `TOV`    | Turnovers committed.                |
| `PF`     | Personal fouls committed.           |
| `PFD`    | Personal fouls drawn by the player. |

### Scoring and other performance measurements

| Variable           | Description                                                                                                                          |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| `PTS`              | Points scored.                                                                                                                       |
| `PLUS_MINUS`       | Point differential while the player is on the court, according to the endpoint's aggregation rules.                                  |
| `NBA_FANTASY_PTS`  | Fantasy-point statistic provided by the endpoint.                                                                                    |
| `DD2`              | Number of double-doubles.                                                                                                            |
| `TD3`              | Number of triple-doubles.                                                                                                            |
| `WNBA_FANTASY_PTS` | WNBA-related fantasy-point field present in the returned schema. Its relevance to NBA player modeling should be verified before use. |
| `FP_HIGH_SCORE`    | High fantasy-score field provided by the endpoint. Verify its exact aggregation definition before using it.                          |

The fantasy-related columns are source fields, not necessarily essential predictors for the classification task.

### Ranking variables

The Base dataset includes ranking columns for many of the preceding statistics.

| Variable                | Description                                           |
| ----------------------- | ----------------------------------------------------- |
| `GP_RANK`               | Ranking for games played.                             |
| `W_RANK`                | Ranking for wins.                                     |
| `L_RANK`                | Ranking for losses.                                   |
| `W_PCT_RANK`            | Ranking for winning percentage.                       |
| `MIN_RANK`              | Ranking for minutes.                                  |
| `FGM_RANK`              | Ranking for field goals made.                         |
| `FGA_RANK`              | Ranking for field goals attempted.                    |
| `FG_PCT_RANK`           | Ranking for field-goal percentage.                    |
| `FG3M_RANK`             | Ranking for three-pointers made.                      |
| `FG3A_RANK`             | Ranking for three-point attempts.                     |
| `FG3_PCT_RANK`          | Ranking for three-point percentage.                   |
| `FTM_RANK`              | Ranking for free throws made.                         |
| `FTA_RANK`              | Ranking for free-throw attempts.                      |
| `FT_PCT_RANK`           | Ranking for free-throw percentage.                    |
| `OREB_RANK`             | Ranking for offensive rebounds.                       |
| `DREB_RANK`             | Ranking for defensive rebounds.                       |
| `REB_RANK`              | Ranking for total rebounds.                           |
| `AST_RANK`              | Ranking for assists.                                  |
| `TOV_RANK`              | Ranking for turnovers.                                |
| `STL_RANK`              | Ranking for steals.                                   |
| `BLK_RANK`              | Ranking for blocks.                                   |
| `BLKA_RANK`             | Ranking for shots blocked against the player.         |
| `PF_RANK`               | Ranking for personal fouls committed.                 |
| `PFD_RANK`              | Ranking for personal fouls drawn.                     |
| `PTS_RANK`              | Ranking for points.                                   |
| `PLUS_MINUS_RANK`       | Ranking for plus/minus.                               |
| `NBA_FANTASY_PTS_RANK`  | Ranking for the NBA fantasy-point statistic.          |
| `DD2_RANK`              | Ranking for double-doubles.                           |
| `TD3_RANK`              | Ranking for triple-doubles.                           |
| `WNBA_FANTASY_PTS_RANK` | Ranking associated with the WNBA fantasy-point field. |
| `FP_HIGH_SCORE_RANK`    | Ranking associated with the high fantasy-score field. |

Rankings are contextual fields whose exact ordering and comparison population should be verified against the endpoint's behavior.

They should not automatically be treated as independent performance measurements.

### Team count

| Variable     | Description                                                                      |
| ------------ | -------------------------------------------------------------------------------- |
| `TEAM_COUNT` | Number of teams associated with the player in the returned statistical grouping. |

A player who changes teams during a season may appear in team-specific records or in an aggregated record, depending on the endpoint's grouping and filters.

Always validate the returned data before assuming one row per player-season.

---

## 1.2 Advanced Statistics

The Advanced dataset contains metrics related to shooting efficiency, usage, passing, rebounding, possession, and offensive or defensive performance.

These fields complement traditional statistics by describing how a player produces results rather than simply counting events.

### Player and team identification

| Variable            | Description                           |
| ------------------- | ------------------------------------- |
| `PLAYER_ID`         | Unique player identifier.             |
| `PLAYER_NAME`       | Player's full name.                   |
| `NICKNAME`          | Player's nickname or short name.      |
| `TEAM_ID`           | Identifier of the associated team.    |
| `TEAM_ABBREVIATION` | Team abbreviation.                    |
| `AGE`               | Player's reported age for the season. |

### Games and playing time

| Variable | Description                                       |
| -------- | ------------------------------------------------- |
| `GP`     | Games played.                                     |
| `W`      | Wins associated with the record.                  |
| `L`      | Losses associated with the record.                |
| `W_PCT`  | Winning percentage associated with the record.    |
| `MIN`    | Average minutes played per game in per-game mode. |

### Offensive and defensive ratings

| Variable             | Description                                                                                                      |
| -------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `E_OFF_RATING`       | Estimated offensive rating supplied by the endpoint.                                                             |
| `OFF_RATING`         | Offensive rating: points produced per 100 possessions under the endpoint's definition.                           |
| `sp_work_OFF_RATING` | Additional field supplied by NBA Stats. Its precise meaning should be verified before use.                       |
| `E_DEF_RATING`       | Estimated defensive rating.                                                                                      |
| `DEF_RATING`         | Defensive rating, generally expressed as points allowed per 100 possessions under the applicable definition.     |
| `sp_work_DEF_RATING` | Additional technical field supplied by the endpoint. Verify its definition before use.                           |
| `E_NET_RATING`       | Estimated net rating.                                                                                            |
| `NET_RATING`         | Net rating, representing the difference between offensive and defensive rating under the endpoint's conventions. |
| `sp_work_NET_RATING` | Additional technical field supplied by the endpoint. Verify its definition before use.                           |

Offensive, defensive, and net ratings depend on the NBA's statistical definitions and should not be interpreted as pure measures of individual contribution.

### Passing and ball movement

| Variable    | Description                                                                                                              |
| ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| `AST_PCT`   | Assist percentage, describing the proportion of relevant teammate field goals assisted by the player while on the court. |
| `AST_TO`    | Assist-to-turnover ratio.                                                                                                |
| `AST_RATIO` | Assists relative to the player's offensive possessions, under the endpoint's definition.                                 |

### Rebounding percentages

| Variable   | Description                   |
| ---------- | ----------------------------- |
| `OREB_PCT` | Offensive rebound percentage. |
| `DREB_PCT` | Defensive rebound percentage. |
| `REB_PCT`  | Total rebound percentage.     |

These percentages estimate a player's share of available rebound opportunities under the applicable NBA definitions.

### Turnover percentages

| Variable     | Description                                               |
| ------------ | --------------------------------------------------------- |
| `TM_TOV_PCT` | Team turnover percentage under the endpoint's definition. |
| `E_TOV_PCT`  | Estimated turnover percentage.                            |

These fields have different definitions and should not be treated as duplicates.

### Shooting efficiency

| Variable  | Description                                                                                                                  |
| --------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `EFG_PCT` | Effective field-goal percentage, which adjusts field-goal efficiency to account for the additional value of three-pointers.  |
| `TS_PCT`  | True shooting percentage, which estimates scoring efficiency by accounting for field goals, three-pointers, and free throws. |

Effective field-goal percentage is commonly defined as:

`eFG% = (FGM + 0.5 × FG3M) / FGA`

True shooting percentage uses a formula that accounts for free-throw attempts. The exact calculation follows the NBA's convention.

### Usage and pace

| Variable       | Description                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------------ |
| `USG_PCT`      | Usage percentage, estimating the proportion of team possessions used by the player while on the court. |
| `E_USG_PCT`    | Estimated usage percentage.                                                                            |
| `E_PACE`       | Estimated pace.                                                                                        |
| `PACE`         | Pace estimate expressed as possessions per 48 minutes under the endpoint's definition.                 |
| `PACE_PER40`   | Pace normalized to 40 minutes.                                                                         |
| `sp_work_PACE` | Additional technical field supplied by the endpoint. Verify its precise definition before use.         |

Usage describes involvement, not necessarily efficiency or quality. A high usage percentage can accompany either excellent or poor shooting efficiency.

### Other performance measurements

| Variable | Description                                                                                                                                                      |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PIE`    | Player Impact Estimate, a composite statistic intended to summarize a player's statistical contribution relative to the game statistics included in its formula. |
| `POSS`   | Possession-related statistic returned by the endpoint. Its aggregation should be checked against the selected mode.                                              |
| `FGM`    | Field goals made in the advanced dataset's returned grouping.                                                                                                    |
| `FGA`    | Field goals attempted in the advanced dataset's returned grouping.                                                                                               |
| `FGM_PG` | Field goals made per game.                                                                                                                                       |
| `FGA_PG` | Field goals attempted per game.                                                                                                                                  |
| `FG_PCT` | Field-goal percentage.                                                                                                                                           |

### Ranking variables

Ranking fields provide contextual rankings for the corresponding advanced statistics.

| Variable                  | Description                                   |
| ------------------------- | --------------------------------------------- |
| `GP_RANK`                 | Ranking for games played.                     |
| `W_RANK`                  | Ranking for wins.                             |
| `L_RANK`                  | Ranking for losses.                           |
| `W_PCT_RANK`              | Ranking for winning percentage.               |
| `MIN_RANK`                | Ranking for minutes.                          |
| `E_OFF_RATING_RANK`       | Ranking for estimated offensive rating.       |
| `OFF_RATING_RANK`         | Ranking for offensive rating.                 |
| `sp_work_OFF_RATING_RANK` | Ranking associated with `sp_work_OFF_RATING`. |
| `E_DEF_RATING_RANK`       | Ranking for estimated defensive rating.       |
| `DEF_RATING_RANK`         | Ranking for defensive rating.                 |
| `sp_work_DEF_RATING_RANK` | Ranking associated with `sp_work_DEF_RATING`. |
| `E_NET_RATING_RANK`       | Ranking for estimated net rating.             |
| `NET_RATING_RANK`         | Ranking for net rating.                       |
| `sp_work_NET_RATING_RANK` | Ranking associated with `sp_work_NET_RATING`. |
| `AST_PCT_RANK`            | Ranking for assist percentage.                |
| `AST_TO_RANK`             | Ranking for assist-to-turnover ratio.         |
| `AST_RATIO_RANK`          | Ranking for assist ratio.                     |
| `OREB_PCT_RANK`           | Ranking for offensive rebound percentage.     |
| `DREB_PCT_RANK`           | Ranking for defensive rebound percentage.     |
| `REB_PCT_RANK`            | Ranking for total rebound percentage.         |
| `TM_TOV_PCT_RANK`         | Ranking for team turnover percentage.         |
| `E_TOV_PCT_RANK`          | Ranking for estimated turnover percentage.    |
| `EFG_PCT_RANK`            | Ranking for effective field-goal percentage.  |
| `TS_PCT_RANK`             | Ranking for true shooting percentage.         |
| `USG_PCT_RANK`            | Ranking for usage percentage.                 |
| `E_USG_PCT_RANK`          | Ranking for estimated usage percentage.       |
| `E_PACE_RANK`             | Ranking for estimated pace.                   |
| `PACE_RANK`               | Ranking for pace.                             |
| `sp_work_PACE_RANK`       | Ranking associated with `sp_work_PACE`.       |
| `PIE_RANK`                | Ranking for Player Impact Estimate.           |
| `FGM_RANK`                | Ranking for field goals made.                 |
| `FGA_RANK`                | Ranking for field goals attempted.            |
| `FGM_PG_RANK`             | Ranking for field goals made per game.        |
| `FGA_PG_RANK`             | Ranking for field goals attempted per game.   |
| `FG_PCT_RANK`             | Ranking for field-goal percentage.            |

### Team count

| Variable     | Description                                                         |
| ------------ | ------------------------------------------------------------------- |
| `TEAM_COUNT` | Number of teams represented in the endpoint's statistical grouping. |

### Important considerations for Advanced

Some fields may be highly correlated.

For example:

* `EFG_PCT` and `TS_PCT` both describe shooting efficiency, but they are not equivalent.
* `OFF_RATING`, `DEF_RATING`, and `NET_RATING` are related by definition.
* `USG_PCT` measures involvement, not necessarily effectiveness.
* Ranking fields can encode information already present in the underlying metric.
* Team-level context can influence some ratings.

These variables will be evaluated during feature selection rather than automatically retained in the final model.

---

# 2. LeagueDashPtStats

## What is it?

`LeagueDashPtStats` is an NBA Stats endpoint that provides player tracking statistics organized into specialized measurement categories.

Unlike traditional box-score statistics, these datasets describe specific actions and contexts, such as:

* Catch-and-shoot attempts.
* Pull-up shots.
* Drives toward the basket.
* Passes and assists.
* Touches in particular areas of the court.
* Defensive activity.
* Rebounding opportunities.
* Player movement and distance covered.

The endpoint allows the extraction of multiple statistical categories by selecting a measurement type.

The project stores each category in a separate CSV file for each season.

### Directory structure

```text
league_dash_pt_stats/
├── season_2015-16/
│   ├── catchshoot.csv
│   ├── defense.csv
│   ├── drives.csv
│   ├── efficiency.csv
│   ├── elbowtouch.csv
│   ├── painttouch.csv
│   ├── passing.csv
│   ├── possessions.csv
│   ├── posttouch.csv
│   ├── pullupshot.csv
│   ├── rebounding.csv
│   └── speeddistance.csv
│
├── season_2016-17/
├── season_2017-18/
└── ...
```

Each season directory contains the tracking categories extracted for that season.

The categories are kept separate because their columns describe different basketball actions and may have different units, definitions, and missing-data patterns.

### Common identification fields

Many tracking datasets share the following columns:

| Variable            | Description                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------- |
| `PLAYER_ID`         | Unique player identifier.                                                                   |
| `PLAYER_NAME`       | Player's name.                                                                              |
| `TEAM_ID`           | Identifier of the associated team.                                                          |
| `TEAM_ABBREVIATION` | Team abbreviation.                                                                          |
| `GP`                | Games played.                                                                               |
| `W`                 | Wins associated with the record.                                                            |
| `L`                 | Losses associated with the record.                                                          |
| `MIN`               | Minutes played, generally represented as average minutes per game when using per-game mode. |

These fields provide context for the tracking measurements.

As with `LeagueDashPlayerStats`, team-related fields should not be interpreted as individual performance metrics.

---

## 2.1 CatchShoot

**File:** `catchshoot.csv`

This dataset describes catch-and-shoot performance.

Catch-and-shoot attempts occur when a player receives the ball and shoots without first creating the shot through a dribble sequence.

| Variable              | Description                                                   |
| --------------------- | ------------------------------------------------------------- |
| `CATCH_SHOOT_FGM`     | Catch-and-shoot field goals made.                             |
| `CATCH_SHOOT_FGA`     | Catch-and-shoot field-goal attempts.                          |
| `CATCH_SHOOT_FG_PCT`  | Field-goal percentage on catch-and-shoot attempts.            |
| `CATCH_SHOOT_PTS`     | Points scored through catch-and-shoot actions.                |
| `CATCH_SHOOT_FG3M`    | Catch-and-shoot three-pointers made.                          |
| `CATCH_SHOOT_FG3A`    | Catch-and-shoot three-point attempts.                         |
| `CATCH_SHOOT_FG3_PCT` | Catch-and-shoot three-point percentage.                       |
| `CATCH_SHOOT_EFG_PCT` | Effective field-goal percentage for catch-and-shoot attempts. |

These metrics can help identify players who are effective when receiving passes and shooting immediately.

They are particularly useful for analyzing off-ball shooting, spacing, and perimeter scoring.

---

## 2.2 Defense

**File:** `defense.csv`

This dataset contains defensive activity and opponent shooting measurements near the rim.

| Variable         | Description                                                                     |
| ---------------- | ------------------------------------------------------------------------------- |
| `STL`            | Steals recorded in the dataset's statistical grouping.                          |
| `BLK`            | Blocks recorded in the dataset's statistical grouping.                          |
| `DREB`           | Defensive rebounds.                                                             |
| `DEF_RIM_FGM`    | Opponent field goals made in the defensive rim context tracked by the endpoint. |
| `DEF_RIM_FGA`    | Opponent field-goal attempts in the tracked rim context.                        |
| `DEF_RIM_FG_PCT` | Field-goal percentage associated with those tracked rim attempts.               |

These statistics provide information about defensive events and shot outcomes near the basket.

However, the tracked rim statistics should not be interpreted as a complete measure of defensive ability. They do not independently capture every aspect of positioning, switching, contesting, or team defense.

---

## 2.3 Drives

**File:** `drives.csv`

This dataset describes drives, which are attacking actions in which a player moves toward the basket with the ball.

| Variable           | Description                                                                             |
| ------------------ | --------------------------------------------------------------------------------------- |
| `DRIVES`           | Number of drives recorded.                                                              |
| `DRIVE_FGM`        | Field goals made following drives.                                                      |
| `DRIVE_FGA`        | Field-goal attempts following drives.                                                   |
| `DRIVE_FG_PCT`     | Field-goal percentage following drives.                                                 |
| `DRIVE_FTM`        | Free throws made in the tracked drive context.                                          |
| `DRIVE_FTA`        | Free throws attempted in the tracked drive context.                                     |
| `DRIVE_FT_PCT`     | Free-throw percentage in the tracked drive context.                                     |
| `DRIVE_PTS`        | Points scored following drives.                                                         |
| `DRIVE_PTS_PCT`    | Percentage of the relevant points attributed to drives under the endpoint's definition. |
| `DRIVE_PASSES`     | Passes made during or following drives under the endpoint's tracking definition.        |
| `DRIVE_PASSES_PCT` | Percentage associated with drive passes.                                                |
| `DRIVE_AST`        | Assists associated with drives.                                                         |
| `DRIVE_AST_PCT`    | Assist percentage associated with drives.                                               |
| `DRIVE_TOV`        | Turnovers associated with drives.                                                       |
| `DRIVE_TOV_PCT`    | Turnover percentage associated with drives.                                             |
| `DRIVE_PF`         | Personal fouls associated with drives.                                                  |
| `DRIVE_PF_PCT`     | Percentage associated with drive-related fouls.                                         |

The dataset helps characterize penetration, finishing, passing decisions, and turnover tendencies during drives.

It can help distinguish a player who creates advantages by attacking the basket from one whose production mainly comes from perimeter shooting.

---

## 2.4 Efficiency

**File:** `efficiency.csv`

This dataset combines points and shooting efficiency across several tracked action types.

| Variable             | Description                                                |
| -------------------- | ---------------------------------------------------------- |
| `POINTS`             | Points recorded for the player in the endpoint's grouping. |
| `DRIVE_PTS`          | Points generated through drives.                           |
| `DRIVE_FG_PCT`       | Field-goal percentage on drives.                           |
| `CATCH_SHOOT_PTS`    | Points generated through catch-and-shoot actions.          |
| `CATCH_SHOOT_FG_PCT` | Catch-and-shoot field-goal percentage.                     |
| `PULL_UP_PTS`        | Points generated through pull-up shots.                    |
| `PULL_UP_FG_PCT`     | Field-goal percentage on pull-up shots.                    |
| `PAINT_TOUCH_PTS`    | Points associated with paint touches.                      |
| `PAINT_TOUCH_FG_PCT` | Field-goal percentage associated with paint-touch actions. |
| `POST_TOUCH_PTS`     | Points associated with post touches.                       |
| `POST_TOUCH_FG_PCT`  | Field-goal percentage associated with post-touch actions.  |
| `ELBOW_TOUCH_PTS`    | Points associated with elbow touches.                      |
| `ELBOW_TOUCH_FG_PCT` | Field-goal percentage associated with elbow-touch actions. |
| `EFF_FG_PCT`         | Effective field-goal percentage provided by this dataset.  |

This dataset is useful for comparing scoring production across different offensive contexts.

The statistics should be interpreted alongside their corresponding opportunities. A high number of points does not necessarily imply high efficiency.

---

## 2.5 ElbowTouch

**File:** `elbowtouch.csv`

An elbow touch occurs when a player receives or controls the ball in the elbow area of the court, near the intersection of the free-throw line and the lane.

| Variable                 | Description                                                                |
| ------------------------ | -------------------------------------------------------------------------- |
| `TOUCHES`                | Total touches in the relevant tracked grouping.                            |
| `ELBOW_TOUCHES`          | Touches recorded in the elbow area.                                        |
| `ELBOW_TOUCH_FGM`        | Field goals made following elbow-touch actions.                            |
| `ELBOW_TOUCH_FGA`        | Field-goal attempts following elbow-touch actions.                         |
| `ELBOW_TOUCH_FG_PCT`     | Field-goal percentage following elbow touches.                             |
| `ELBOW_TOUCH_FTM`        | Free throws made in the elbow-touch context.                               |
| `ELBOW_TOUCH_FTA`        | Free throws attempted in the elbow-touch context.                          |
| `ELBOW_TOUCH_FT_PCT`     | Free-throw percentage in the elbow-touch context.                          |
| `ELBOW_TOUCH_PTS`        | Points associated with elbow-touch actions.                                |
| `ELBOW_TOUCH_PASSES`     | Passes associated with elbow-touch actions.                                |
| `ELBOW_TOUCH_AST`        | Assists associated with elbow-touch actions.                               |
| `ELBOW_TOUCH_AST_PCT`    | Assist percentage associated with elbow touches.                           |
| `ELBOW_TOUCH_TOV`        | Turnovers associated with elbow-touch actions.                             |
| `ELBOW_TOUCH_TOV_PCT`    | Turnover percentage associated with elbow touches.                         |
| `ELBOW_TOUCH_FOULS`      | Fouls associated with elbow-touch actions under the endpoint's definition. |
| `ELBOW_TOUCH_PASSES_PCT` | Percentage associated with elbow-touch passes.                             |
| `ELBOW_TOUCH_FOULS_PCT`  | Percentage associated with elbow-touch fouls.                              |
| `ELBOW_TOUCH_PTS_PCT`    | Percentage associated with elbow-touch points.                             |

These statistics can help identify players who act as decision-makers from the elbow, including players who create scoring opportunities for teammates.

---

## 2.6 PaintTouch

**File:** `painttouch.csv`

A paint touch occurs when a player touches the ball in the painted area near the basket, according to the tracking system's definition.

| Variable                 | Description                                        |
| ------------------------ | -------------------------------------------------- |
| `TOUCHES`                | Total touches in the relevant tracked grouping.    |
| `PAINT_TOUCHES`          | Touches recorded in the painted area.              |
| `PAINT_TOUCH_FGM`        | Field goals made following paint touches.          |
| `PAINT_TOUCH_FGA`        | Field-goal attempts following paint touches.       |
| `PAINT_TOUCH_FG_PCT`     | Field-goal percentage following paint touches.     |
| `PAINT_TOUCH_FTM`        | Free throws made in the paint-touch context.       |
| `PAINT_TOUCH_FTA`        | Free throws attempted in the paint-touch context.  |
| `PAINT_TOUCH_FT_PCT`     | Free-throw percentage in the paint-touch context.  |
| `PAINT_TOUCH_PTS`        | Points associated with paint touches.              |
| `PAINT_TOUCH_PTS_PCT`    | Percentage associated with paint-touch points.     |
| `PAINT_TOUCH_PASSES`     | Passes associated with paint touches.              |
| `PAINT_TOUCH_PASSES_PCT` | Percentage associated with paint-touch passes.     |
| `PAINT_TOUCH_AST`        | Assists associated with paint touches.             |
| `PAINT_TOUCH_AST_PCT`    | Assist percentage associated with paint touches.   |
| `PAINT_TOUCH_TOV`        | Turnovers associated with paint touches.           |
| `PAINT_TOUCH_TOV_PCT`    | Turnover percentage associated with paint touches. |
| `PAINT_TOUCH_FOULS`      | Fouls associated with paint-touch actions.         |
| `PAINT_TOUCH_FOULS_PCT`  | Percentage associated with paint-touch fouls.      |

Paint-touch statistics can help describe interior scoring, passing out of the paint, and the ability to create opportunities near the basket.

---

## 2.7 Passing

**File:** `passing.csv`

This dataset describes passing activity and different forms of assist creation.

| Variable              | Description                                                                                                 |
| --------------------- | ----------------------------------------------------------------------------------------------------------- |
| `PASSES_MADE`         | Passes made.                                                                                                |
| `PASSES_RECEIVED`     | Passes received.                                                                                            |
| `AST`                 | Assists.                                                                                                    |
| `FT_AST`              | Free-throw assists as defined by the endpoint.                                                              |
| `SECONDARY_AST`       | Secondary assists, sometimes called hockey assists.                                                         |
| `POTENTIAL_AST`       | Potential assists, representing passes that could have resulted in an assist under the tracking definition. |
| `AST_POINTS_CREATED`  | Points created through assists, under the endpoint's definition.                                            |
| `AST_ADJ`             | Adjusted assists, as defined by the endpoint.                                                               |
| `AST_TO_PASS_PCT`     | Assist-to-pass percentage.                                                                                  |
| `AST_TO_PASS_PCT_ADJ` | Adjusted assist-to-pass percentage.                                                                         |

These variables help characterize playmaking and passing involvement beyond the conventional assist count.

Potential assists and secondary assists are particularly useful when analyzing players whose passing creates advantages that do not always appear in the traditional box score.

---

## 2.8 Possessions

**File:** `possessions.csv`

This dataset describes touches, possession time, and scoring production in different court areas.

| Variable              | Description                                         |
| --------------------- | --------------------------------------------------- |
| `POINTS`              | Points recorded in the relevant grouping.           |
| `TOUCHES`             | Number of touches.                                  |
| `FRONT_CT_TOUCHES`    | Touches in the frontcourt.                          |
| `TIME_OF_POSS`        | Time of possession under the endpoint's definition. |
| `AVG_SEC_PER_TOUCH`   | Average seconds per touch.                          |
| `AVG_DRIB_PER_TOUCH`  | Average dribbles per touch.                         |
| `PTS_PER_TOUCH`       | Points per touch.                                   |
| `ELBOW_TOUCHES`       | Touches in the elbow area.                          |
| `POST_TOUCHES`        | Touches in the post area.                           |
| `PAINT_TOUCHES`       | Touches in the painted area.                        |
| `PTS_PER_ELBOW_TOUCH` | Points per elbow touch.                             |
| `PTS_PER_POST_TOUCH`  | Points per post touch.                              |
| `PTS_PER_PAINT_TOUCH` | Points per paint touch.                             |

These measurements can help distinguish players who create offense through frequent ball possession from players who score efficiently with fewer touches.

The time and touch statistics should be interpreted together because they describe different aspects of offensive involvement.

---

## 2.9 PostTouch

**File:** `posttouch.csv`

Post touches occur when a player handles the ball in the post area, typically near the basket with their back or side oriented toward the defender.

| Variable                | Description                                             |
| ----------------------- | ------------------------------------------------------- |
| `TOUCHES`               | Total touches in the relevant grouping.                 |
| `POST_TOUCHES`          | Touches in the post area.                               |
| `POST_TOUCH_FGM`        | Field goals made following post touches.                |
| `POST_TOUCH_FGA`        | Field-goal attempts following post touches.             |
| `POST_TOUCH_FG_PCT`     | Field-goal percentage following post touches.           |
| `POST_TOUCH_FTM`        | Free throws made in the post-touch context.             |
| `POST_TOUCH_FTA`        | Free throws attempted in the post-touch context.        |
| `POST_TOUCH_FT_PCT`     | Free-throw percentage in the post-touch context.        |
| `POST_TOUCH_PTS`        | Points associated with post touches.                    |
| `POST_TOUCH_PTS_PCT`    | Percentage associated with post-touch points.           |
| `POST_TOUCH_PASSES`     | Passes associated with post touches.                    |
| `POST_TOUCH_PASSES_PCT` | Percentage associated with post-touch passes.           |
| `POST_TOUCH_AST`        | Assists associated with post-touch actions.             |
| `POST_TOUCH_AST_PCT`    | Assist percentage associated with post-touch actions.   |
| `POST_TOUCH_TOV`        | Turnovers associated with post-touch actions.           |
| `POST_TOUCH_TOV_PCT`    | Turnover percentage associated with post-touch actions. |
| `POST_TOUCH_FOULS`      | Fouls associated with post-touch actions.               |
| `POST_TOUCH_FOULS_PCT`  | Percentage associated with post-touch fouls.            |

These variables can help characterize post scoring, passing decisions, and ball security in interior offensive situations.

---

## 2.10 PullUpShot

**File:** `pullupshot.csv`

A pull-up shot is taken after a player uses a dribble to create a shooting opportunity rather than immediately shooting after receiving a pass.

| Variable          | Description                                        |
| ----------------- | -------------------------------------------------- |
| `PULL_UP_FGM`     | Pull-up field goals made.                          |
| `PULL_UP_FGA`     | Pull-up field-goal attempts.                       |
| `PULL_UP_FG_PCT`  | Pull-up field-goal percentage.                     |
| `PULL_UP_PTS`     | Points scored through pull-up shots.               |
| `PULL_UP_FG3M`    | Pull-up three-pointers made.                       |
| `PULL_UP_FG3A`    | Pull-up three-point attempts.                      |
| `PULL_UP_FG3_PCT` | Pull-up three-point percentage.                    |
| `PULL_UP_EFG_PCT` | Effective field-goal percentage for pull-up shots. |

These statistics help characterize self-created perimeter scoring and shooting performance after dribbling.

They can be particularly informative when comparing players who create their own shots with players who primarily finish plays created by teammates.

---

## 2.11 Rebounding

**File:** `rebounding.csv`

This dataset provides detailed rebounding measurements, including contested rebounds, uncontested rebounds, opportunities, and average rebound distances.

### Offensive rebounding

| Variable              | Description                                                                                                |
| --------------------- | ---------------------------------------------------------------------------------------------------------- |
| `OREB`                | Offensive rebounds.                                                                                        |
| `OREB_CONTEST`        | Contested offensive rebounds.                                                                              |
| `OREB_UNCONTEST`      | Uncontested offensive rebounds.                                                                            |
| `OREB_CONTEST_PCT`    | Percentage associated with contested offensive rebounds.                                                   |
| `OREB_CHANCES`        | Offensive rebound opportunities.                                                                           |
| `OREB_CHANCE_PCT`     | Offensive rebound conversion percentage.                                                                   |
| `OREB_CHANCE_DEFER`   | Offensive rebound opportunities deferred to teammates or otherwise classified as deferred by the endpoint. |
| `OREB_CHANCE_PCT_ADJ` | Adjusted offensive rebound opportunity percentage.                                                         |
| `AVG_OREB_DIST`       | Average distance associated with offensive rebounds.                                                       |

### Defensive rebounding

| Variable              | Description                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------------- |
| `DREB`                | Defensive rebounds.                                                                           |
| `DREB_CONTEST`        | Contested defensive rebounds.                                                                 |
| `DREB_UNCONTEST`      | Uncontested defensive rebounds.                                                               |
| `DREB_CONTEST_PCT`    | Percentage associated with contested defensive rebounds.                                      |
| `DREB_CHANCES`        | Defensive rebound opportunities.                                                              |
| `DREB_CHANCE_PCT`     | Defensive rebound conversion percentage.                                                      |
| `DREB_CHANCE_DEFER`   | Defensive rebound opportunities deferred or otherwise classified as deferred by the endpoint. |
| `DREB_CHANCE_PCT_ADJ` | Adjusted defensive rebound opportunity percentage.                                            |
| `AVG_DREB_DIST`       | Average distance associated with defensive rebounds.                                          |

### Total rebounding

| Variable             | Description                                                                         |
| -------------------- | ----------------------------------------------------------------------------------- |
| `REB`                | Total rebounds.                                                                     |
| `REB_CONTEST`        | Contested rebounds.                                                                 |
| `REB_UNCONTEST`      | Uncontested rebounds.                                                               |
| `REB_CONTEST_PCT`    | Percentage associated with contested rebounds.                                      |
| `REB_CHANCES`        | Total rebound opportunities.                                                        |
| `REB_CHANCE_PCT`     | Rebound opportunity conversion percentage.                                          |
| `REB_CHANCE_DEFER`   | Rebound opportunities deferred or otherwise classified as deferred by the endpoint. |
| `REB_CHANCE_PCT_ADJ` | Adjusted rebound opportunity percentage.                                            |
| `AVG_REB_DIST`       | Average distance associated with rebounds.                                          |

These variables help distinguish players who collect many rebounds because they encounter many opportunities from players who convert a high proportion of their opportunities.

Contested rebound measurements can also help describe performance in situations where opponents challenge for the ball.

The exact definitions of deferred opportunities and adjusted percentages should be verified against the NBA Stats documentation before they are used in derived metrics.

---

## 2.12 SpeedDistance

**File:** `speeddistance.csv`

This dataset describes the distance covered and speed recorded for a player during tracked activity.

| Variable         | Description                                           |
| ---------------- | ----------------------------------------------------- |
| `DIST_FEET`      | Total distance in feet.                               |
| `DIST_MILES`     | Total distance in miles.                              |
| `DIST_MILES_OFF` | Distance in miles associated with offensive activity. |
| `DIST_MILES_DEF` | Distance in miles associated with defensive activity. |
| `AVG_SPEED`      | Average speed across the tracked activity.            |
| `AVG_SPEED_OFF`  | Average speed during offensive activity.              |
| `AVG_SPEED_DEF`  | Average speed during defensive activity.              |

These fields provide information about movement and physical activity.

They should not be interpreted as direct measures of athletic ability or player quality. The measurements can be affected by playing time, role, team system, and the nature of the player's responsibilities.

---

# Installation

## Requirements

The project requires:

* Python 3.10 or a compatible version.
* `nba_api`.
* `pandas`.
* Internet connectivity for data extraction.

The extraction scripts use Pandas to handle tabular responses and write CSV files.

### 1. Clone the repository

```bash
git clone <repository-url>
cd StatToStars_ML
```

Replace `<https://github.com/gamerOZZY/StatToStars_ML.git>` with the repository's actual URL.

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, activate the environment using an appropriate method for your system or use Command Prompt.

### 3. Install dependencies

```bash
pip install nba_api pandas
```

---

# Data Extraction

The extraction scripts are located in `src/ETL/`:

```text
src/
├── ETL/
│   ├── extraer_estadisticas_temporada.py
│   └── extraer_estadisticas_tracking.py
└── prueba.py
```

The project also includes Windows batch scripts in `scripts/` to simplify execution.

## 1. Extract Base and Advanced Statistics

The script `extraer_estadisticas_temporada.py` retrieves player statistics using `LeagueDashPlayerStats`.

It collects both measurement types:

* `Base`
* `Advanced`

Example:

```powershell
python src/ETL/extraer_estadisticas_temporada.py --temporadas "2023-24"
```

To collect several seasons:

```powershell
python src/ETL/extraer_estadisticas_temporada.py --temporadas "2015-16" "2016-17" "2017-18" "2018-19" "2019-20" "2020-21" "2021-22" "2022-23" "2023-24" "2024-25" "2025-26"
```

The resulting CSV files are stored in:

```text
data/bronze/league_dash_player_stats/
├── base/
└── advanced/
```

## 2. Extract Player Tracking Statistics

The script `extraer_estadisticas_tracking.py` retrieves tracking statistics using `LeagueDashPtStats`.

Example:

```powershell
python src/ETL/extraer_estadisticas_tracking.py --temporadas "2023-24"
```

To extract several seasons:

```powershell
python src/ETL/extraer_estadisticas_tracking.py --temporadas "2015-16" "2016-17" "2017-18" "2018-19" "2019-20" "2020-21" "2021-22" "2022-23" "2023-24" "2024-25" "2025-26"
```

The resulting CSV files are organized by season and measurement category:

```text
data/bronze/league_dash_pt_stats/
└── season_2023-24/
    ├── catchshoot.csv
    ├── defense.csv
    ├── drives.csv
    ├── efficiency.csv
    ├── elbowtouch.csv
    ├── painttouch.csv
    ├── passing.csv
    ├── possessions.csv
    ├── posttouch.csv
    ├── pullupshot.csv
    ├── rebounding.csv
    └── speeddistance.csv
```

The actual categories and successful extractions depend on the endpoint's available data and the installed `nba_api` version.

### Historical availability

Although the collection covers the 2015-16 through 2025-26 seasons, not every tracking metric is necessarily available for every season.

A missing CSV or an empty response should be investigated rather than automatically interpreted as a zero value.

The extraction process should distinguish between:

* A successful extraction containing records.
* A successful extraction containing no records.
* A failed request.
* A measurement that is unavailable for a historical season.

---

# Data Quality and Limitations

The Bronze layer is intended to preserve source data, not guarantee that all records are ready for modeling.

Several considerations are important for later processing.

## 1. Player-season identification

The eventual analytical dataset will generally need to identify observations by player and season.

However, some endpoint responses can contain multiple team-specific records for a player who changed teams.

Before combining datasets, verify whether the appropriate key is:

* `PLAYER_ID` and season.
* `PLAYER_ID`, team, and season.
* Another grouping defined by the endpoint.

Do not assume that every CSV contains exactly one row per player-season.

## 2. Different statistical units

Some columns represent counts, others percentages, averages, rates, or rankings.

These cannot be interpreted or combined interchangeably.

For example:

* `PTS` represents scoring production.
* `TS_PCT` describes scoring efficiency.
* `USG_PCT` describes offensive involvement.
* `PTS_PER_TOUCH` relates scoring to touches.
* `PTS_RANK` represents a relative ranking.

The statistical unit and aggregation mode should be retained when designing downstream transformations.

## 3. Missing data

Historical tracking coverage may vary by category and season.

Missing values should not automatically be replaced with zero because zero means something different from an unavailable measurement.

Silver should distinguish between missing values, unavailable statistics, and genuine zero observations wherever possible.

## 4. Rankings

Ranking variables are derived from the underlying statistics and can encode relative information about a player.

They may also depend on the comparison population and endpoint parameters.

For the initial model, their usefulness should be evaluated rather than assumed.

## 5. Correlated features

Several variables measure closely related concepts.

Examples include:

* `FG_PCT` and `EFG_PCT`.
* `EFG_PCT` and `TS_PCT`.
* `OFF_RATING`, `DEF_RATING`, and `NET_RATING`.
* Counts, percentages, and rankings derived from the same event.
* Points and points per touch.

These relationships should be considered during feature selection and model evaluation.

## 6. Avoiding target leakage

The final classification label must be defined before the model is trained.

If a statistic is used directly to determine whether a player-season is classified as good or poor, that same statistic should not be included as a predictor without a carefully justified alternative design.

Otherwise, the model may simply reproduce the labeling rule instead of learning a useful predictive relationship.

## 7. Temporal evaluation

NBA statistics change across seasons, and a player's observations may be correlated over time.

A random split of player-season records can produce overly optimistic evaluation if related observations appear in both training and testing sets.

A temporal evaluation, in which earlier seasons are used for training and later seasons for testing, is a useful approach when the goal is to predict future-season performance.

---

# Roadmap

The planned development stages are:

* [x] Create the initial project structure.
* [x] Implement extraction of Base player statistics.
* [x] Implement extraction of Advanced player statistics.
* [x] Implement extraction of Player Tracking categories.
* [x] Store the extracted data as season-specific CSV files in Bronze.
* [ ] Validate historical coverage and endpoint consistency.
* [ ] Develop Silver transformations and data-quality checks.
* [ ] Integrate the statistical datasets at the appropriate grain.
* [ ] Perform exploratory data analysis.
* [ ] Define and document the classification target.
* [ ] Build a model-ready Gold dataset.
* [ ] Train baseline classification models.
* [ ] Evaluate models using appropriate classification metrics.
* [ ] Analyze feature importance and model limitations.

---

# References

* [NBA Stats](https://www.nba.com/stats/) - NBA statistical portal.
* [nba_api GitHub repository](https://github.com/swar/nba_api) - Python client for NBA Stats endpoints.
* [LeagueDashPlayerStats documentation](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguedashplayerstats.md) - Documentation for player statistics.
* [LeagueDashPtStats documentation](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguedashptstats.md) - Documentation for player tracking statistics.

---

## Disclaimer

This is an educational and analytical machine learning project. It is not affiliated with or endorsed by the NBA.

The collected statistics are intended for research, data engineering, and machine learning experimentation. Their definitions, historical availability, and aggregation behavior should be verified against the source endpoint before being used to draw conclusions about player performance.
