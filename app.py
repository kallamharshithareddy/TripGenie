from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)

app.secret_key = "tripgenie-secret-key"

#-----------database--------#

def init_db():
    conn = sqlite3.connect("tripgenie.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            travel_style TEXT DEFAULT 'Balanced',
            budget TEXT DEFAULT 'Medium',
            interests TEXT DEFAULT '',
            phone TEXT DEFAULT ''
        )
    """)

    # Add new columns if the table already existed
    columns = [
        ("travel_style", "TEXT DEFAULT 'Balanced'"),
        ("budget", "TEXT DEFAULT 'Medium'"),
        ("interests", "TEXT DEFAULT ''"),
        ("phone", "TEXT DEFAULT ''")
    ]

    existing_columns = [
        row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()
    ]

    for column, definition in columns:
        if column not in existing_columns:
            conn.execute(
                f"ALTER TABLE users ADD COLUMN {column} {definition}"
            )

    conn.commit()
    conn.close()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template(
        "index.html",
        user_name=session.get("user_name")
    )


# =========================================================
# PLANNER PAGE
# =========================================================

@app.route("/planner")
def planner():
    return render_template("planner.html")


# =========================================================
# GENERATE TRIP
# =========================================================

@app.route("/generate-trip", methods=["POST"])
def generate_trip():

    try:

        # -------------------------------------------------
        # Get form data
        # -------------------------------------------------

        start_location = request.form.get(
            "start_location",
            ""
        ).strip()

        destination = request.form.get(
            "destination",
            ""
        ).strip()

        days = int(
            request.form.get(
                "days",
                3
            )
        )

        travelers = int(
            request.form.get(
                "travelers",
                1
            )
        )

        budget = int(
            request.form.get(
                "budget",
                10000
            )
        )

        interests = request.form.getlist(
            "interests"
        )

        travel_style = request.form.get(
            "travel_style",
            "balanced"
        )


        # -------------------------------------------------
        # Basic validation
        # -------------------------------------------------

        if not destination:

            return "Please enter a destination.", 400


        if days < 1:

            return "Number of days must be at least 1.", 400


        if travelers < 1:

            return "Number of travelers must be at least 1.", 400


        if budget < 0:

            return "Budget cannot be negative.", 400


        # =================================================
        # INTEREST ACTIVITIES
        # =================================================

        activity_map = {

            "beaches":
                "Visit beautiful beaches, enjoy the coastline and capture sunset photos.",

            "food":
                "Explore famous local restaurants, street food and traditional dishes.",

            "adventure":
                "Try exciting adventure activities and explore outdoor attractions.",

            "nature":
                "Explore scenic natural places, viewpoints, parks and peaceful surroundings.",

            "culture":
                "Visit historical monuments, museums and experience the local culture.",

            "shopping":
                "Explore popular markets, shopping streets and local handicrafts."

        }


        # =================================================
        # INTEREST TITLES
        # =================================================

        interest_titles = {

            "beaches": [

                "Beach Exploration",

                "Beautiful Beaches & Water Activities",

                "Coastal Adventure & Sunset",

                "Relaxation by the Sea"

            ],

            "food": [

                "Local Food Exploration",

                "Famous Restaurants & Street Food",

                "Traditional Food Experience",

                "Food & Café Hopping"

            ],

            "adventure": [

                "Adventure Activities",

                "Thrilling Outdoor Experiences",

                "Adventure & Exploration",

                "Outdoor Fun & Activities"

            ],

            "nature": [

                "Nature Exploration",

                "Scenic Places & Viewpoints",

                "Greenery & Natural Beauty",

                "Peaceful Nature Experience"

            ],

            "culture": [

                "Local Culture & History",

                "Historical Places",

                "Cultural Experiences",

                "Heritage Exploration"

            ],

            "shopping": [

                "Local Markets",

                "Shopping & Souvenirs",

                "Famous Shopping Streets",

                "Local Market Exploration"

            ]

        }


        # =================================================
        # SELECTED ACTIVITIES
        # =================================================

        selected_activities = []


        for interest in interests:

            if interest in activity_map:

                selected_activities.append(
                    activity_map[interest]
                )


        if not selected_activities:

            selected_activities.append(
                "Explore popular attractions and local experiences."
            )


        # =================================================
        # PERSONALIZED TITLES
        # =================================================

        personalized_titles = []


        for interest in interests:

            if interest in interest_titles:

                personalized_titles.extend(
                    interest_titles[interest]
                )


        if not personalized_titles:

            personalized_titles = [

                "Arrival & Local Exploration",

                "Top Attractions & Sightseeing",

                "Local Experiences",

                "Relaxation & Exploration"

            ]


        # =================================================
        # TRAVEL STYLE
        # =================================================

        style_description = {

            "budget":
                "Focus on affordable attractions, local food and budget-friendly experiences.",

            "balanced":
                "Balance comfort, sightseeing, food and experiences within your budget.",

            "luxury":
                "Focus on premium experiences, comfortable stays and high-quality dining.",

            "adventure":
                "Focus on exciting activities, exploration and outdoor experiences.",

            "relaxed":
                "Keep the trip comfortable with fewer activities and more relaxation."

        }


        travel_style_description = style_description.get(

            travel_style,

            "Enjoy a balanced travel experience."

        )


        # =================================================
        # CREATE ITINERARY
        # =================================================

        itinerary = []


        daily_cost = round(
            budget / days
        )


        for day in range(
            1,
            days + 1
        ):

            title_index = (
                day - 1
            ) % len(
                personalized_titles
            )


            activity_index = (
                day - 1
            ) % len(
                selected_activities
            )


            title = personalized_titles[
                title_index
            ]


            activity = selected_activities[
                activity_index
            ]


            # ---------------------------------------------
            # First day
            # ---------------------------------------------

            if day == 1:

                description = (

                    f"Start your journey from "
                    f"{start_location} and begin exploring "
                    f"{destination}. {activity}"

                )


            # ---------------------------------------------
            # Last day
            # ---------------------------------------------

            elif day == days:

                description = (

                    f"Enjoy your final day in "
                    f"{destination}. {activity} "
                    f"Prepare for your return journey."

                )


            # ---------------------------------------------
            # Middle days
            # ---------------------------------------------

            else:

                description = activity


            itinerary.append({

                "day": day,

                "title":
                    f"Day {day} - {title}",

                "description":
                    description,

                "places":
                    f"Popular attractions and experiences in {destination}",

                "cost":
                    daily_cost

            })


        # =================================================
        # BUDGET BREAKDOWN
        # =================================================

        budget_breakdown = {

            "stay":
                round(
                    budget * 0.40
                ),

            "food":
                round(
                    budget * 0.20
                ),

            "transport":
                round(
                    budget * 0.15
                ),

            "activities":
                round(
                    budget * 0.15
                ),

            "miscellaneous":
                round(
                    budget * 0.10
                )

        }


        # =================================================
        # SEND DATA TO ITINERARY PAGE
        # =================================================

        return render_template(

            "itinerary.html",

            start_location=start_location,

            destination=destination,

            days=days,

            travelers=travelers,

            budget=budget,

            interests=interests,

            travel_style=travel_style,

            travel_style_description=
                travel_style_description,

            itinerary=itinerary,

            total_cost=budget,

            budget_breakdown=
                budget_breakdown

        )


    except ValueError:

        return (

            "Please enter valid numbers for "
            "days, travelers and budget.",

            400

        )


    except Exception as e:

        print(
            "Trip generation error:",
            e
        )

        return (

            "Something went wrong while "
            "generating your trip.",

            500

        )


# =========================================================
# WEATHER API
# =========================================================

@app.route("/weather")
def weather():

    destination = request.args.get(
        "destination"
    )


    # -----------------------------------------------------
    # Check destination
    # -----------------------------------------------------

    if not destination:

        return jsonify({

            "error":
                "Destination is required"

        }), 400


    try:

        # =================================================
        # STEP 1
        # Find latitude and longitude
        # =================================================

        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
        )


        geo_params = {

            "name":
                destination,

            "count":
                1,

            "language":
                "en",

            "format":
                "json"

        }


        geo_response = requests.get(

            geo_url,

            params=geo_params,

            timeout=10

        )


        geo_response.raise_for_status()


        geo_data = (
            geo_response.json()
        )


        # -------------------------------------------------
        # Destination not found
        # -------------------------------------------------

        if not geo_data.get(
            "results"
        ):

            return jsonify({

                "error":
                    "Destination not found"

            }), 404


        location = geo_data[
            "results"
        ][0]


        latitude = location[
            "latitude"
        ]


        longitude = location[
            "longitude"
        ]


        # =================================================
        # STEP 2
        # Get weather
        # =================================================

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
        )


        weather_params = {

            "latitude":
                latitude,

            "longitude":
                longitude,

            "current":
                (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "wind_speed_10m,"
                    "weather_code"
                ),

            "daily":
                (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min"
                ),

            "forecast_days":
                7,

            "timezone":
                "auto"

        }


        weather_response = requests.get(

            weather_url,

            params=weather_params,

            timeout=10

        )


        weather_response.raise_for_status()


        weather_data = (
            weather_response.json()
        )


        current = weather_data[
            "current"
        ]


        daily = weather_data[
            "daily"
        ]


        # =================================================
        # WEATHER CODE DESCRIPTIONS
        # =================================================

        weather_codes = {

            0:
                "Clear Sky",

            1:
                "Mainly Clear",

            2:
                "Partly Cloudy",

            3:
                "Overcast",

            45:
                "Fog",

            48:
                "Fog",

            51:
                "Light Drizzle",

            53:
                "Moderate Drizzle",

            55:
                "Heavy Drizzle",

            61:
                "Slight Rain",

            63:
                "Moderate Rain",

            65:
                "Heavy Rain",

            71:
                "Slight Snow",

            73:
                "Moderate Snow",

            75:
                "Heavy Snow",

            80:
                "Rain Showers",

            81:
                "Rain Showers",

            82:
                "Heavy Rain Showers",

            95:
                "Thunderstorm",

            96:
                "Thunderstorm",

            99:
                "Thunderstorm"

        }


        # =================================================
        # BUILD 7-DAY FORECAST
        # =================================================

        forecast = []


        for i in range(
            len(
                daily["time"]
            )
        ):

            forecast.append({

                "date":
                    daily["time"][i],

                "condition":
                    weather_codes.get(

                        daily[
                            "weather_code"
                        ][i],

                        "Unknown"

                    ),

                "max":
                    daily[
                        "temperature_2m_max"
                    ][i],

                "min":
                    daily[
                        "temperature_2m_min"
                    ][i]

            })


        # =================================================
        # RETURN WEATHER DATA
        # =================================================

        return jsonify({

            "destination":
                location["name"],

            "temperature":
                current[
                    "temperature_2m"
                ],

            "condition":
                weather_codes.get(

                    current[
                        "weather_code"
                    ],

                    "Unknown"

                ),

            "humidity":
                current[
                    "relative_humidity_2m"
                ],

            "wind_speed":
                current[
                    "wind_speed_10m"
                ],

            "forecast":
                forecast

        })


    except requests.exceptions.RequestException as e:

        print(
            "Weather API error:",
            e
        )


        return jsonify({

            "error":
                "Weather service is currently unavailable."

        }), 503


    except Exception as e:

        print(
            "Weather error:",
            e
        )


        return jsonify({

            "error":
                "Unable to fetch weather."

        }), 500
#------sigup-------

@app.route("/sigup", methods=["GET", "POST"])
def sigup():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password:
            return "Please fill all required fields."

        if password != confirm_password:
            return "Passwords do not match."

        if len(password) < 6:
            return "Password must contain at least 6 characters."

        conn = sqlite3.connect("tripgenie.db")

        try:
            hashed_password = generate_password_hash(password)

            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "An account with this email already exists."

        conn.close()

        return redirect(url_for("login"))

    return render_template("sigup.html")


#-----login---- 
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = sqlite3.connect("tripgenie.db")
        conn.row_factory = sqlite3.Row

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            return redirect(url_for("home"))

        return "Invalid email or password."

    return render_template("login.html")  

#--------profile-------#

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("tripgenie.db")
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        travel_style = request.form.get("travel_style", "Balanced")
        budget = request.form.get("budget", "Medium")

        interests = request.form.getlist("interests")
        interests_text = ", ".join(interests)

        conn.execute("""
            UPDATE users
            SET name = ?,
                phone = ?,
                travel_style = ?,
                budget = ?,
                interests = ?
            WHERE id = ?
        """, (
            name,
            phone,
            travel_style,
            budget,
            interests_text,
            session["user_id"]
        ))

        conn.commit()

        session["user_name"] = name

    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template("profile.html", user=user)

#-----logout----

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("sigup"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)