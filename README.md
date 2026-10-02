# 🏏 IPL Auction Simulator

A Python + MySQL console simulation of an IPL mini-auction where a user builds a 7-player squad while competing against rule-based bot teams.

## Overview

This project was originally developed as my Class 12 Computer Science project. The portfolio version keeps the core mechanics while removing credentials from source code and organizing the project for GitHub.

## Features

- User registration and login
- IPL franchise selection
- ₹100 crore starting budget
- Competitive bidding against automated opponents
- Rule-based bot bidding
- Player ratings and base prices
- Roster composition logic
- Budget constraints
- Auction history
- Team persistence using MySQL
- Team rankings based on average player rating
- Input and budget validation

## Bot bidding logic

The bots use heuristic decision rules rather than machine learning. Their decisions consider:

- player rating
- player role
- current team composition
- remaining budget
- remaining roster slots
- player base price

Higher-rated players receive stronger bidding probabilities, while bots also prioritize roster positions they still need.

## Tech stack

- Python
- MySQL
- `mysql-connector-python`
- `random`
- SQL

## Project structure

```text
ipl-auction-simulator/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
└── screenshots/
```

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install and start MySQL

Create a local MySQL server and make sure it is running.

### 3. Set database environment variables

#### Windows PowerShell

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="YOUR_LOCAL_MYSQL_PASSWORD"
$env:MYSQL_DATABASE="mini_auction"
```

#### macOS/Linux

```bash
export MYSQL_HOST="localhost"
export MYSQL_USER="root"
export MYSQL_PASSWORD="YOUR_LOCAL_MYSQL_PASSWORD"
export MYSQL_DATABASE="mini_auction"
```

### 4. Run

```bash
python main.py
```

The program creates the required database/tables and loads the player dataset when it starts.

## Security note

Database credentials are intentionally kept outside the source code. Never commit your real password, `.env` files, or other secrets to a public repository.

## Future improvements

- Web-based interface
- Better statistical player valuation
- Historical IPL performance data
- Visualization dashboard
- Optimization-based bidding
- Machine-learning bidding agents
