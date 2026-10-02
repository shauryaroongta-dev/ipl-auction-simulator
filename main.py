"""
IPL Auction Simulator
A Python + MySQL console simulation of an IPL mini-auction.

Original school project: Class 12 Computer Science
Refactored for portfolio/GitHub use:
- credentials are read from environment variables
- no real passwords are stored in source control
"""

import os
import random
import mysql.connector as myc


DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE", "mini_auction")

TEAMS = [
    "Mumbai Indians",
    "Chennai Super Kings",
    "Royal Challengers Bengaluru",
    "Gujarat Titans",
    "Kolkata Knight Riders",
]

PLAYERS = [
    ("Virat Kohli", "batsman", 12, None, "No", 9.5),
    ("Rohit Sharma", "batsman", 12, None, "No", 9.0),
    ("MS Dhoni", "batsman", 10, None, "Yes", 8.8),
    ("KL Rahul", "batsman", 10, None, "Yes", 8.0),
    ("Rishabh Pant", "batsman", 10, None, "Yes", 8.5),
    ("Shubman Gill", "batsman", 9, None, "No", 8.4),
    ("David Warner", "batsman", 9, None, "No", 8.6),
    ("Devdutt Padikkal", "batsman", 8, None, "No", 7.8),
    ("Prithvi Shaw", "batsman", 8, None, "No", 7.5),
    ("Yashasvi Jaiswal", "batsman", 8, None, "No", 7.9),
    ("Hardik Pandya", "allrounder", 10, "Medium-Fast", "No", 8.7),
    ("Ravindra Jadeja", "allrounder", 9, "Left-arm Orthodox", "No", 8.6),
    ("Ben Stokes", "allrounder", 11, "Medium-Fast", "No", 8.9),
    ("Andre Russell", "allrounder", 11, "Fast", "No", 9.0),
    ("Glenn Maxwell", "allrounder", 10, "Off-spin", "No", 8.4),
    ("Marcus Stoinis", "allrounder", 9, "Medium-Fast", "No", 8.0),
    ("Liam Livingstone", "allrounder", 9, "Leg-spin", "No", 8.2),
    ("Washington Sundar", "allrounder", 8, "Off-spin", "No", 7.8),
    ("Axar Patel", "allrounder", 8, "Left-arm Orthodox", "No", 8.1),
    ("Vijay Shankar", "allrounder", 7, "Medium-Fast", "No", 7.2),
    ("Jasprit Bumrah", "bowler", 12, "Fast", "No", 9.6),
    ("Mohammed Shami", "bowler", 9, "Fast", "No", 8.2),
    ("Yuzvendra Chahal", "bowler", 9, "Leg-spin", "No", 8.3),
    ("Rashid Khan", "bowler", 11, "Leg-spin", "No", 9.4),
    ("Bhuvneshwar Kumar", "bowler", 8, "Medium-Fast", "No", 8.0),
    ("Kuldeep Yadav", "bowler", 8, "Chinaman", "No", 7.9),
    ("Umran Malik", "bowler", 8, "Fast", "No", 8.1),
    ("T Natarajan", "bowler", 8, "Medium-Fast", "No", 7.8),
    ("Varun Chakravarthy", "bowler", 7, "Mystery Spin", "No", 7.6),
    ("Avesh Khan", "bowler", 7, "Fast", "No", 7.4),
    ("Sanju Samson", "batsman", 9, None, "Yes", 8.2),
    ("Ishan Kishan", "batsman", 9, None, "Yes", 8.1),
    ("Dinesh Karthik", "batsman", 8, None, "Yes", 7.6),
    ("Wriddhiman Saha", "batsman", 7, None, "Yes", 7.2),
    ("Rahul Tripathi", "batsman", 7, None, "No", 7.5),
    ("Mayank Agarwal", "batsman", 7, None, "No", 7.4),
    ("Ajinkya Rahane", "batsman", 6, None, "No", 7.0),
    ("Manish Pandey", "batsman", 6, None, "No", 6.9),
    ("Ruturaj Gaikwad", "batsman", 8, None, "No", 8.0),
    ("Shreyas Iyer", "batsman", 9, None, "No", 8.3),
    ("Sunil Narine", "allrounder", 10, "Off-spin", "No", 8.6),
    ("Jason Holder", "allrounder", 9, "Medium-Fast", "No", 8.0),
    ("Moeen Ali", "allrounder", 9, "Off-spin", "No", 8.1),
    ("Chris Woakes", "allrounder", 8, "Medium-Fast", "No", 7.9),
    ("Pat Cummins", "allrounder", 10, "Fast", "No", 8.5),
    ("Mitchell Marsh", "allrounder", 9, "Medium-Fast", "No", 8.0),
    ("Riyan Parag", "allrounder", 7, "Leg-spin", "No", 7.2),
    ("Shivam Dube", "allrounder", 7, "Medium-Fast", "No", 7.3),
    ("Deepak Hooda", "allrounder", 7, "Off-spin", "No", 7.4),
    ("Krunal Pandya", "allrounder", 7, "Left-arm Orthodox", "No", 7.6),
    ("Kagiso Rabada", "bowler", 11, "Fast", "No", 9.0),
    ("Anrich Nortje", "bowler", 10, "Fast", "No", 8.7),
    ("Trent Boult", "bowler", 10, "Fast", "No", 8.8),
    ("Josh Hazlewood", "bowler", 9, "Fast", "No", 8.4),
    ("Lockie Ferguson", "bowler", 9, "Fast", "No", 8.2),
    ("Mustafizur Rahman", "bowler", 8, "Medium-Fast", "No", 7.9),
    ("Alzarri Joseph", "bowler", 8, "Fast", "No", 7.8),
    ("Obed McCoy", "bowler", 7, "Medium-Fast", "No", 7.5),
    ("Reece Topley", "bowler", 7, "Medium-Fast", "No", 7.3),
    ("Mark Wood", "bowler", 8, "Fast", "No", 8.0),
    ("Arshdeep Singh", "bowler", 8, "Medium-Fast", "No", 7.8),
    ("Harshal Patel", "bowler", 8, "Medium-Fast", "No", 7.7),
    ("Shardul Thakur", "bowler", 8, "Medium-Fast", "No", 7.9),
    ("Rahul Chahar", "bowler", 7, "Leg-spin", "No", 7.5),
    ("Sandeep Sharma", "bowler", 7, "Medium-Fast", "No", 7.4),
    ("Jaydev Unadkat", "bowler", 6, "Medium-Fast", "No", 7.1),
    ("Navdeep Saini", "bowler", 7, "Fast", "No", 7.2),
    ("Mohit Sharma", "bowler", 6, "Medium-Fast", "No", 6.9),
    ("Khaleel Ahmed", "bowler", 7, "Medium-Fast", "No", 7.3),
    ("Chetan Sakariya", "bowler", 7, "Medium-Fast", "No", 7.2),
    ("Tilak Varma", "batsman", 7, None, "No", 7.6),
    ("Abhishek Sharma", "batsman", 7, None, "No", 7.4),
    ("Jitesh Sharma", "batsman", 6, None, "Yes", 7.1),
    ("Heinrich Klaasen", "batsman", 8, None, "Yes", 8.0),
    ("Jos Buttler", "batsman", 10, None, "Yes", 8.5),
]


def setup_database():
    """Create the database/tables and load the player dataset."""
    if not DB_PASSWORD:
        print("❌ MYSQL_PASSWORD is not set.")
        print("Set MYSQL_PASSWORD in your environment before running the game.")
        return False

    try:
        con = myc.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cur = con.cursor()

        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        cur.execute(f"USE `{DB_NAME}`")

        cur.execute("DROP TABLE IF EXISTS user_team")
        cur.execute("DROP TABLE IF EXISTS ipl_players_2025")
        cur.execute("DROP TABLE IF EXISTS users")

        cur.execute(
            """
            CREATE TABLE users (
                username VARCHAR(50) PRIMARY KEY,
                password VARCHAR(50),
                team VARCHAR(50)
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE ipl_players_2025 (
                player_id INT AUTO_INCREMENT PRIMARY KEY,
                player_name VARCHAR(50),
                role VARCHAR(15),
                base_price INT NOT NULL,
                bowler_type VARCHAR(30),
                wicket_keeper VARCHAR(5),
                rating DECIMAL(3,1),
                is_sold BOOLEAN DEFAULT FALSE,
                sold_to VARCHAR(50) DEFAULT NULL,
                sold_price INT DEFAULT NULL
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE user_team (
                username VARCHAR(50),
                assembled_team TEXT,
                FOREIGN KEY (username) REFERENCES users(username)
            )
            """
        )

        cur.executemany(
            """
            INSERT INTO ipl_players_2025
            (player_name, role, base_price, bowler_type, wicket_keeper, rating)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            PLAYERS,
        )

        con.commit()
        con.close()
        print("✅ Database setup complete with fresh player data!")
        return True

    except myc.Error as exc:
        print(f"❌ Database setup error: {exc}")
        return False


def get_connection():
    """Return a connection to the application's database."""
    try:
        return myc.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
    except myc.Error as exc:
        print(f"❌ Connection error: {exc}")
        return None


def print_header(title):
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)


def signup():
    print_header("SIGN UP")
    con = get_connection()
    if not con:
        return

    cursor = con.cursor()

    try:
        username = input("Create a username: ").strip()
        if not username:
            print("❌ Username cannot be empty!")
            return

        password = input("Create a password: ").strip()
        if not password:
            print("❌ Password cannot be empty!")
            return

        print("\nChoose your IPL team:")
        for idx, team in enumerate(TEAMS, start=1):
            print(f"{idx}. {team}")

        choice = input("Enter your choice (1-5): ").strip()
        if choice not in {"1", "2", "3", "4", "5"}:
            print("❌ Invalid choice. Signup cancelled.")
            return

        team = TEAMS[int(choice) - 1]

        cursor.execute(
            "SELECT * FROM users WHERE username = %s",
            (username,),
        )
        if cursor.fetchone():
            print("⚠️ Username already exists. Try logging in instead.")
            return

        cursor.execute(
            """
            INSERT INTO users (username, password, team)
            VALUES (%s, %s, %s)
            """,
            (username, password, team),
        )
        con.commit()

        print(f"✅ Signup successful! You selected {team}.")

        bot_count = 0
        for bot_team in TEAMS:
            if bot_team == team:
                continue

            bot_name = (
                "BOT_"
                + bot_team.replace(" ", "")
                .replace("Challengers", "C")
            )

            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (bot_name,),
            )
            if not cursor.fetchone():
                cursor.execute(
                    """
                    INSERT INTO users (username, password, team)
                    VALUES (%s, %s, %s)
                    """,
                    (bot_name, "botpass", bot_team),
                )
                bot_count += 1

        con.commit()
        print(f"🤖 {bot_count} bot teams created. Ready for mini auction!")

    except myc.Error as exc:
        print(f"❌ Signup error: {exc}")
    finally:
        con.close()


def login():
    print_header("LOGIN")
    con = get_connection()
    if not con:
        return None

    cursor = con.cursor()

    try:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE username = %s AND password = %s
            """,
            (username, password),
        )

        result = cursor.fetchone()
        if result is not None:
            print(f"✅ Login successful! Welcome back, {username} 🎉")
            return username

        print("❌ Incorrect username or password. Please try again.")
        return None

    except myc.Error as exc:
        print(f"❌ Login error: {exc}")
        return None
    finally:
        con.close()


def start_auction(username):
    print_header("IPL MINI AUCTION 2025")
    print("--- MINI AUCTION RULES ---")
    print("1. You have a budget of 100 crores.")
    print("2. You must build a team of exactly 7 players.")
    print("3. Bidding continues until no one bids higher.")
    print("4. Bots will compete aggressively!")

    input("\nPress Enter to start the auction...")

    con = get_connection()
    if not con:
        return

    cursor = con.cursor()

    try:
        cursor.execute(
            """
            UPDATE ipl_players_2025
            SET is_sold = FALSE, sold_to = NULL, sold_price = NULL
            """
        )
        con.commit()

        team_limit = 7
        user_budget = 100
        user_team = []

        cursor.execute(
            "SELECT team FROM users WHERE username = %s",
            (username,),
        )
        row = cursor.fetchone()
        if not row:
            print("❌ User not found.")
            return

        user_team_name = row[0]

        for team in TEAMS:
            if team == user_team_name:
                continue

            bot_name = (
                "BOT_"
                + team.replace(" ", "")
                .replace("Challengers", "C")
            )

            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (bot_name,),
            )

            if not cursor.fetchone():
                cursor.execute(
                    """
                    INSERT INTO users (username, password, team)
                    VALUES (%s, %s, %s)
                    """,
                    (bot_name, "botpass", team),
                )

        con.commit()

        cursor.execute(
            "SELECT username, team FROM users WHERE username LIKE 'BOT_%'"
        )
        bot_data = cursor.fetchall()

        bot_teams = {
            bot_user: {
                "team_name": bot_team,
                "players": [],
                "budget": 100,
            }
            for bot_user, bot_team in bot_data
        }

        print(f"🤖 {len(bot_teams)} bot teams ready to compete!")

        cursor.execute(
            """
            SELECT player_id, player_name, role, base_price, rating,
                   wicket_keeper, bowler_type
            FROM ipl_players_2025
            WHERE is_sold = FALSE
            ORDER BY rating DESC
            """
        )

        players_list = list(cursor.fetchall())
        random.shuffle(players_list)

        players_auctioned = 0

        while len(user_team) < team_limit and players_auctioned < len(players_list):
            all_teams_full = len(user_team) >= team_limit
            for bot_info in bot_teams.values():
                if len(bot_info["players"]) < team_limit:
                    all_teams_full = False
                    break

            if all_teams_full:
                break

            (
                player_id,
                name,
                role,
                base_price,
                rating,
                wicket_keeper,
                bowler_type,
            ) = players_list[players_auctioned]

            cursor.execute(
                "SELECT is_sold FROM ipl_players_2025 WHERE player_id = %s",
                (player_id,),
            )
            sold_row = cursor.fetchone()
            if sold_row and sold_row[0]:
                players_auctioned += 1
                continue

            if base_price is None or base_price <= 0:
                base_price = 5

            print("\n" + "=" * 60)
            print(f"🏏 AUCTIONING: {name}")
            print(f" Role: {role.upper()}")
            print(f" Base Price: ₹{base_price} cr")
            print(f" Rating: {rating}/10")
            if wicket_keeper == "Yes":
                print(" Wicket Keeper: Yes")
            if bowler_type:
                print(f" Bowling: {bowler_type}")
            print("=" * 60)

            print("\n📊 YOUR STATUS:")
            print(f" Team Size: {len(user_team)}/{team_limit}")
            print(f" Budget Left: ₹{user_budget} cr")

            current_bid = base_price
            highest_bidder = None
            passed_users = set()

            print(f"\n💰 BIDDING STARTS AT ₹{current_bid} CR")

            max_rounds = 15

            for _ in range(max_rounds):
                someone_bid_this_round = False

                if (
                    username not in passed_users
                    and user_budget > current_bid
                    and len(user_team) < team_limit
                ):
                    try:
                        user_input = input(
                            f"\nYour bid (current: ₹{current_bid}cr, 0 to pass): "
                        ).strip()

                        if user_input == "0":
                            passed_users.add(username)
                            print("🚫 You passed on this player.")
                        else:
                            user_bid = int(float(user_input))

                            if user_bid <= current_bid:
                                print("❌ Bid must be higher than current bid!")
                                continue

                            if user_bid > user_budget:
                                print(
                                    f"❌ Insufficient budget! "
                                    f"You have ₹{user_budget}cr left."
                                )
                                continue

                            current_bid = user_bid
                            highest_bidder = username
                            someone_bid_this_round = True
                            print(f"✅ You bid ₹{user_bid}cr")

                    except ValueError:
                        print("❌ Please enter a valid number!")
                        continue

                eligible_bots = []

                for bot_name, bot_info in bot_teams.items():
                    if (
                        bot_name not in passed_users
                        and bot_info["budget"] > current_bid
                        and len(bot_info["players"]) < team_limit
                    ):
                        eligible_bots.append((bot_name, bot_info))

                random.shuffle(eligible_bots)

                for bot_name, bot_info in eligible_bots:
                    keepers = sum(
                        1
                        for p in bot_info["players"]
                        if p.get("wicket_keeper") == "Yes"
                    )
                    batsmen = sum(
                        1 for p in bot_info["players"] if p["role"] == "batsman"
                    )
                    bowlers = sum(
                        1 for p in bot_info["players"] if p["role"] == "bowler"
                    )
                    allrounders = sum(
                        1
                        for p in bot_info["players"]
                        if p["role"] == "allrounder"
                    )

                    should_bid = False

                    if (
                        wicket_keeper == "Yes"
                        and keepers == 0
                        and len(bot_info["players"]) > 3
                    ):
                        should_bid = True
                    elif role == "batsman" and batsmen < 3:
                        should_bid = True
                    elif role == "bowler" and bowlers < 2:
                        should_bid = True
                    elif role == "allrounder" and allrounders < 1:
                        should_bid = True

                    if rating >= 9.0:
                        should_bid = True
                    elif rating >= 8.5 and random.random() < 0.85:
                        should_bid = True
                    elif rating >= 8.0 and random.random() < 0.70:
                        should_bid = True
                    elif rating >= 7.5 and random.random() < 0.50:
                        should_bid = True
                    elif rating >= 7.0 and random.random() < 0.35:
                        should_bid = True

                    remaining_budget = bot_info["budget"]
                    remaining_slots = team_limit - len(bot_info["players"])
                    reserve_budget = (
                        max(0, (remaining_slots - 1) * 5)
                        if remaining_slots > 1
                        else 0
                    )
                    max_bot_bid = min(
                        remaining_budget - reserve_budget,
                        base_price * 2.0,
                    )

                    if (
                        max_bot_bid <= current_bid
                        or remaining_budget <= current_bid
                    ):
                        continue

                    if should_bid and current_bid < max_bot_bid:
                        if wicket_keeper == "Yes" and keepers == 0:
                            bid_increment = random.randint(1, 3)
                        elif rating >= 9.0:
                            bid_increment = random.randint(1, 3)
                        else:
                            bid_increment = random.randint(1, 2)

                        bot_bid = min(
                            current_bid + bid_increment,
                            max_bot_bid,
                            remaining_budget,
                        )

                        if bot_bid > current_bid and bot_bid <= bot_info["budget"]:
                            current_bid = bot_bid
                            highest_bidder = bot_name
                            someone_bid_this_round = True
                            print(
                                f"🤖 {bot_info['team_name']} bids ₹{bot_bid}cr "
                                f"(Budget: ₹{bot_info['budget']}cr)"
                            )
                            break

                    if random.random() < 0.25:
                        passed_users.add(bot_name)

                if not someone_bid_this_round:
                    break

                total_participants = 1 + len(bot_teams)
                if len(passed_users) >= total_participants - 1:
                    break

            if highest_bidder is None:
                print(f"\n🚫 No bids for {name}. Player unsold.")

            elif highest_bidder == username:
                user_budget -= current_bid
                user_team.append(
                    {
                        "name": name,
                        "role": role,
                        "price": current_bid,
                        "rating": rating,
                        "wicket_keeper": wicket_keeper,
                    }
                )

                cursor.execute(
                    """
                    UPDATE ipl_players_2025
                    SET is_sold = TRUE, sold_to = %s, sold_price = %s
                    WHERE player_id = %s
                    """,
                    (username, current_bid, player_id),
                )
                con.commit()
                print(f"\n🎉 SOLD! You got {name} for ₹{current_bid}cr!")

            else:
                bot_teams[highest_bidder]["budget"] -= current_bid
                bot_teams[highest_bidder]["players"].append(
                    {
                        "name": name,
                        "role": role,
                        "price": current_bid,
                        "rating": rating,
                        "wicket_keeper": wicket_keeper,
                    }
                )

                cursor.execute(
                    """
                    UPDATE ipl_players_2025
                    SET is_sold = TRUE, sold_to = %s, sold_price = %s
                    WHERE player_id = %s
                    """,
                    (highest_bidder, current_bid, player_id),
                )
                con.commit()

                winner_team = bot_teams[highest_bidder]["team_name"]
                print(f"\n🤖 SOLD to {winner_team} for ₹{current_bid}cr")

            players_auctioned += 1

            if (
                (user_budget < 6 and len(user_team) < team_limit)
                or (
                    len(players_list) - players_auctioned < 5
                    and len(user_team) < team_limit
                )
            ):
                remaining = team_limit - len(user_team)

                if remaining > 0:
                    print(
                        f"\n⚠️ Auto-completing team with "
                        f"{remaining} available players..."
                    )

                    cursor.execute(
                        """
                        SELECT player_id, player_name, role, base_price,
                               rating, wicket_keeper
                        FROM ipl_players_2025
                        WHERE is_sold = FALSE AND base_price <= %s
                        ORDER BY base_price ASC
                        LIMIT %s
                        """,
                        (
                            max(user_budget // remaining, 5),
                            remaining,
                        ),
                    )

                    for (
                        p_id,
                        p_name,
                        p_role,
                        p_price,
                        p_rating,
                        p_wk,
                    ) in cursor.fetchall():

                        if len(user_team) >= team_limit or user_budget < p_price:
                            break

                        user_budget -= p_price
                        user_team.append(
                            {
                                "name": p_name,
                                "role": p_role,
                                "price": p_price,
                                "rating": p_rating,
                                "wicket_keeper": p_wk,
                            }
                        )

                        cursor.execute(
                            """
                            UPDATE ipl_players_2025
                            SET is_sold = TRUE, sold_to = %s, sold_price = %s
                            WHERE player_id = %s
                            """,
                            (username, p_price, p_id),
                        )
                        print(f"🔄 Auto-bought {p_name} for ₹{p_price}cr")
                        con.commit()

        print("\n🤖 Auto-completing all teams to 7 players...")

        # Complete user team if necessary.
        if len(user_team) < team_limit:
            remaining = team_limit - len(user_team)
            cursor.execute(
                """
                SELECT player_id, player_name, role, base_price,
                       rating, wicket_keeper
                FROM ipl_players_2025
                WHERE is_sold = FALSE
                ORDER BY base_price ASC
                LIMIT %s
                """,
                (remaining,),
            )

            for (
                p_id,
                p_name,
                p_role,
                p_price,
                p_rating,
                p_wk,
            ) in cursor.fetchall():

                if len(user_team) >= team_limit:
                    break

                slots_left = team_limit - len(user_team)
                actual_price = min(
                    p_price,
                    max(user_budget // slots_left, 5),
                )

                user_team.append(
                    {
                        "name": p_name,
                        "role": p_role,
                        "price": actual_price,
                        "rating": p_rating,
                        "wicket_keeper": p_wk,
                    }
                )

                user_budget = max(0, user_budget - actual_price)

                cursor.execute(
                    """
                    UPDATE ipl_players_2025
                    SET is_sold = TRUE, sold_to = %s, sold_price = %s
                    WHERE player_id = %s
                    """,
                    (username, actual_price, p_id),
                )
                print(
                    f"🔄 Auto-assigned {p_name} "
                    f"for ₹{actual_price}cr"
                )
                con.commit()

        # Complete bot teams if necessary.
        for bot_name, bot_info in bot_teams.items():
            remaining_slots = team_limit - len(bot_info["players"])

            if remaining_slots <= 0:
                continue

            print(
                f"🤖 Auto-completing {bot_info['team_name']} "
                f"with {remaining_slots} players..."
            )

            cursor.execute(
                """
                SELECT player_id, player_name, role, base_price,
                       rating, wicket_keeper
                FROM ipl_players_2025
                WHERE is_sold = FALSE
                ORDER BY base_price ASC
                LIMIT %s
                """,
                (remaining_slots,),
            )

            for (
                p_id,
                p_name,
                p_role,
                p_price,
                p_rating,
                p_wk,
            ) in cursor.fetchall():

                if len(bot_info["players"]) >= team_limit:
                    break

                slots_left = team_limit - len(bot_info["players"])
                actual_price = min(
                    p_price,
                    max(bot_info["budget"] // slots_left, 5),
                )

                bot_info["budget"] = max(
                    0, bot_info["budget"] - actual_price
                )
                bot_info["players"].append(
                    {
                        "name": p_name,
                        "role": p_role,
                        "price": actual_price,
                        "rating": p_rating,
                        "wicket_keeper": p_wk,
                    }
                )

                cursor.execute(
                    """
                    UPDATE ipl_players_2025
                    SET is_sold = TRUE, sold_to = %s, sold_price = %s
                    WHERE player_id = %s
                    """,
                    (bot_name, actual_price, p_id),
                )
                con.commit()

        show_final_results(username, user_team, user_budget, bot_teams)
        save_user_team(username, user_team, cursor, con)

    except myc.Error as exc:
        print(f"❌ Auction database error: {exc}")
    except Exception as exc:
        print(f"❌ Auction error: {exc}")
    finally:
        con.close()


def show_final_results(username, user_team, user_budget, bot_teams):
    print("\n" + "=" * 70)
    print("🏆 MINI AUCTION COMPLETE - FINAL RESULTS")
    print("=" * 70)

    def display_team(team_name, players, budget_left):
        total_spent = 100 - budget_left
        avg_rating = (
            sum(p["rating"] for p in players) / len(players)
            if players
            else 0
        )
        keepers = sum(
            1 for p in players if p.get("wicket_keeper") == "Yes"
        )
        batsmen = sum(1 for p in players if p["role"] == "batsman")
        bowlers = sum(1 for p in players if p["role"] == "bowler")
        allrounders = sum(
            1 for p in players if p["role"] == "allrounder"
        )

        print(f"\n🏏 {team_name.upper()}")
        print("-" * 50)
        print(
            f"Players: {len(players)}/7 | "
            f"Budget Left: ₹{budget_left}cr"
        )
        print(
            f"Composition: {batsmen}B, {bowlers}Bo, "
            f"{allrounders}AR, {keepers}WK"
        )
        print(
            f"Avg Rating: {avg_rating:.1f} | "
            f"Spent: ₹{total_spent}cr"
        )

        for i, player in enumerate(players, start=1):
            wk = (
                " (WK)"
                if player.get("wicket_keeper") == "Yes"
                else ""
            )
            print(
                f"{i:2d}. {player['name']:<25} "
                f"{player['role'][:3].upper()}{wk:<4} "
                f"₹{player['price']:>3}cr "
                f"({player['rating']:.1f})"
            )

    display_team(
        f"YOUR TEAM ({username})",
        user_team,
        user_budget,
    )

    for bot_info in bot_teams.values():
        display_team(
            bot_info["team_name"],
            bot_info["players"],
            bot_info["budget"],
        )

    print("\n🏆 TEAM RANKINGS:")
    print("-" * 50)

    all_teams = [(username, user_team)]
    all_teams.extend(
        (bot_info["team_name"], bot_info["players"])
        for bot_info in bot_teams.values()
    )

    ranked = []
    for team_name, players in all_teams:
        if players:
            avg_rating = sum(p["rating"] for p in players) / len(players)
            ranked.append((team_name, avg_rating, len(players)))

    ranked.sort(key=lambda x: x[1], reverse=True)

    for i, (team_name, avg_rating, count) in enumerate(ranked, start=1):
        medal = (
            "🥇" if i == 1
            else "🥈" if i == 2
            else "🥉" if i == 3
            else f"{i}."
        )
        print(f"{medal} {team_name:<25} {avg_rating:.2f}/10 ({count} players)")


def save_user_team(username, user_team, cursor, con):
    try:
        team_data = [
            f"{p['name']} (₹{p['price']}cr)"
            for p in user_team
        ]
        team_string = " | ".join(team_data)

        cursor.execute(
            "SELECT * FROM user_team WHERE username = %s",
            (username,),
        )

        if cursor.fetchone():
            cursor.execute(
                """
                UPDATE user_team
                SET assembled_team = %s
                WHERE username = %s
                """,
                (team_string, username),
            )
        else:
            cursor.execute(
                """
                INSERT INTO user_team (username, assembled_team)
                VALUES (%s, %s)
                """,
                (username, team_string),
            )

        con.commit()
        print("\n✅ Team saved successfully!")

    except myc.Error as exc:
        print(f"❌ Error saving team: {exc}")


def view_all_users():
    print_header("ALL USERS & THEIR TEAMS")
    con = get_connection()
    if not con:
        return

    cursor = con.cursor()

    try:
        cursor.execute(
            """
            SELECT u.username, u.team, ut.assembled_team
            FROM users u
            LEFT JOIN user_team ut ON u.username = ut.username
            ORDER BY u.username
            """
        )

        users = cursor.fetchall()

        if not users:
            print("No users found.")
            return

        for username, team, assembled_team in users:
            bot_tag = " (BOT)" if "BOT_" in username else ""
            print(f"\n👤 {username:<30} - {team}{bot_tag}")
            print("-" * 70)

            if assembled_team:
                players = assembled_team.split(" | ")
                print(f" Team Size: {len(players)}/7 players")
                for i, player_info in enumerate(players, start=1):
                    print(f" {i:2d}. {player_info}")

            elif "BOT_" in username:
                cursor.execute(
                    """
                    SELECT player_name, sold_price
                    FROM ipl_players_2025
                    WHERE sold_to = %s AND is_sold = TRUE
                    ORDER BY sold_price DESC
                    """,
                    (username,),
                )

                bot_players = cursor.fetchall()

                if bot_players:
                    print(
                        f" Team Size: {len(bot_players)}/7 players "
                        "(Current Auction)"
                    )
                    total_spent = sum(
                        price for _, price in bot_players
                    )
                    remaining_budget = 100 - total_spent
                    print(
                        f" Budget Spent: ₹{total_spent}cr | "
                        f"Remaining: ₹{remaining_budget}cr"
                    )

                    for i, (player_name, price) in enumerate(
                        bot_players, start=1
                    ):
                        print(f" {i:2d}. {player_name} (₹{price}cr)")
                else:
                    print(" ❌ No team assembled yet")
            else:
                print(" ❌ No team assembled yet")

    except myc.Error as exc:
        print(f"❌ Error: {exc}")
    finally:
        con.close()


def view_auction_history():
    print_header("AUCTION HISTORY")
    con = get_connection()
    if not con:
        return

    cursor = con.cursor()

    try:
        cursor.execute(
            """
            SELECT player_name, role, base_price,
                   sold_price, sold_to, rating
            FROM ipl_players_2025
            WHERE is_sold = TRUE
            ORDER BY sold_price DESC
            """
        )

        sold_players = cursor.fetchall()

        if not sold_players:
            print("No auction history found.")
            return

        print(
            f"{'Player':<25} {'Role':<12} "
            f"{'Base':<6} {'Sold':<6} {'Team':<30} {'Rating'}"
        )
        print("-" * 100)

        for player in sold_players:
            name, role, base_price, sold_price, sold_to, rating = player
            team_display = sold_to

            if sold_to.startswith("BOT_"):
                team_display = (
                    sold_to.replace("BOT_", "")
                    .replace("C", "Challengers")
                )

            print(
                f"{name:<25} {role:<12} "
                f"₹{base_price:<5} ₹{sold_price:<5} "
                f"{team_display:<30} {rating:.1f}"
            )

    except myc.Error as exc:
        print(f"❌ Error: {exc}")
    finally:
        con.close()


def view_user_team(username):
    print_header(f"YOUR TEAM - {username.upper()}")
    con = get_connection()
    if not con:
        return

    cursor = con.cursor()

    try:
        cursor.execute(
            "SELECT assembled_team FROM user_team WHERE username = %s",
            (username,),
        )

        result = cursor.fetchone()

        if result and result[0]:
            players = result[0].split(" | ")
            print(f"Team Size: {len(players)} players")
            print("-" * 50)

            for i, player_info in enumerate(players, start=1):
                print(f"{i:2d}. {player_info}")
            return

        cursor.execute(
            """
            SELECT player_name, sold_price, role, rating
            FROM ipl_players_2025
            WHERE sold_to = %s AND is_sold = TRUE
            ORDER BY sold_price DESC
            """,
            (username,),
        )

        current_players = cursor.fetchall()

        if current_players:
            print(
                f"Team Size: {len(current_players)}/7 players "
                "(Current Auction)"
            )
            total_spent = sum(
                price for _, price, _, _ in current_players
            )
            remaining_budget = 100 - total_spent

            print(
                f"Budget Spent: ₹{total_spent}cr | "
                f"Remaining: ₹{remaining_budget}cr"
            )
            print("-" * 50)

            for i, (player_name, price, role, rating) in enumerate(
                current_players, start=1
            ):
                print(
                    f"{i:2d}. {player_name} - {role} "
                    f"(₹{price}cr) - Rating: {rating:.1f}"
                )
        else:
            print("No team found. Please participate in an auction first!")

    except myc.Error as exc:
        print(f"❌ Error: {exc}")
    finally:
        con.close()


def reset_auction():
    print_header("RESET AUCTION")
    confirm = input(
        "⚠️ This will reset all auction data. Are you sure? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("❌ Reset cancelled.")
        return

    con = get_connection()
    if not con:
        return

    cursor = con.cursor()

    try:
        cursor.execute(
            """
            UPDATE ipl_players_2025
            SET is_sold = FALSE,
                sold_to = NULL,
                sold_price = NULL
            """
        )
        cursor.execute("DELETE FROM user_team")
        con.commit()
        print("✅ Auction data reset successfully!")

    except myc.Error as exc:
        print(f"❌ Error resetting auction: {exc}")
    finally:
        con.close()


def main_menu():
    if not setup_database():
        print("❌ Failed to setup database. Exiting...")
        return

    current_user = None

    while True:
        print("\n" + "=" * 60)
        print("🏏 WELCOME TO IPL MINI AUCTION GAME 2025 🏏".center(60))
        print("=" * 60)

        if current_user:
            print(f"👤 Logged in as: {current_user}")
            print("1. 🏆 Start Mini Auction")
            print("2. 👥 View My Team")
            print("3. 📊 View Auction History")
            print("4. 🔄 Reset Auction Data")
            print("5. 👀 View All Users")
            print("6. 🚪 Logout")
            print("7. ❌ Exit")

            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                start_auction(current_user)
            elif choice == "2":
                view_user_team(current_user)
            elif choice == "3":
                view_auction_history()
            elif choice == "4":
                reset_auction()
            elif choice == "5":
                view_all_users()
            elif choice == "6":
                current_user = None
                print("👋 Logged out successfully!")
            elif choice == "7":
                print("🎉 Thank you for playing IPL Mini Auction Game 2025!")
                print("🏏 May the best team win! Goodbye! 🏆")
                break
            else:
                print("❌ Invalid input. Please choose between 1-7.")

        else:
            print("1. 📝 Sign Up")
            print("2. 🔐 Log In")
            print("3. 👥 View All Users")
            print("4. 🚪 Exit")

            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                signup()
            elif choice == "2":
                username = login()
                if username and not username.startswith("BOT_"):
                    current_user = username
                elif username and username.startswith("BOT_"):
                    print("❌ Bot accounts cannot log in!")
            elif choice == "3":
                view_all_users()
            elif choice == "4":
                print("🎉 Thank you for playing IPL Mini Auction Game 2025!")
                print("🏏 May the best team win! Goodbye! 🏆")
                break
            else:
                print("❌ Invalid input. Please choose between 1-4.")


if __name__ == "__main__":
    print("🏏 Starting IPL Mini Auction Game 2025...")
    print("⚡ Setting up database...")
    main_menu()
