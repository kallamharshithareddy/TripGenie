# ✈️ TripGenie AI — Smart Travel Planner

**TripGenie AI** is a web-based travel planning application designed to help users plan personalized trips based on their destination, budget, travel duration, and interests.

It combines a simple user interface with travel recommendations, weather information, and an interactive map to make trip planning easier.

## 🌟 Features

- 🏠 **Home Page** — A welcoming landing page with an overview of TripGenie.
- 🔐 **User Authentication** — Sign up, log in, and log out.
- 👤 **Client Profile** — A dedicated page for user account information and travel preferences.
- 🗺️ **Trip Planner** — Enter your starting location, destination, number of days, travelers, budget, and interests.
- 🧭 **Personalized Itinerary** — Generate a trip itinerary based on the information provided.
- 💰 **Budget Breakdown** — View an estimated distribution of travel expenses.
- 🌦️ **Weather Information** — Get weather details for your destination.
- 📅 **7-Day Forecast** — Check the upcoming weather forecast.
- 🏨 **Hotel Recommendations** — Explore suggested accommodation options.
- 🍽️ **Restaurant Recommendations** — Discover dining suggestions.
- 📍 **Interactive Map** — View destinations and places on a map.
- 🎨 **Responsive Design** — A travel-focused interface designed for convenient browsing.

> Note: Some recommendations or AI-related features may use demo data. Availability depends on the current project configuration and API setup.

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **Weather Data:** Open-Meteo API
- **Maps:** Leaflet and OpenStreetMap
- **Authentication:** Flask sessions and password hashing
- **Version Control:** Git and GitHub

## 📁 Project Structure

```text
TripGenie/
├── app.py
├── database/
├── models/
├── routes/
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── sigup.html
│   ├── profile.html
│   ├── planner.html
│   └── itinerary.html
├── utils/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

*The structure above is illustrative. Your actual files and folders may differ.*

## ⚙️ Installation and Setup

### Prerequisites

Install the following software:

- Python 3.10 or newer
- Visual Studio Code (recommended)
- Git (for version control)

### 1. Clone the repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/kallamharshithareddy/TripGenie.git
cd TripGenie
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python directly:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Install dependencies

With the virtual environment activated, run:

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

If your project uses environment variables, create a local `.env` file in the project root and add the settings required by your code.

For example:

```env
OPENAI_API_KEY=your_api_key_here
```

Replace the placeholder only if you have a valid API key and the feature requires it. Do not commit `.env` to GitHub.

### 6. Run the application

```bash
python app.py
```

Open the local address shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

## 🌦️ Weather Integration

TripGenie uses the Open-Meteo geocoding and forecast services to retrieve location and weather information. Weather data requires an internet connection.

## 🗄️ Database

The application uses SQLite to store user account information and, where implemented, profile preferences.

The database file can be created locally when the application initializes. Do not upload a database containing real user details or passwords.

## 🔒 Security Notes

- Never upload API keys, passwords, or secret environment files.
- Keep `.env`, `venv/`, Python cache files, and local database files out of version control.
- Passwords should be stored as hashes, not plain text.
- Use a strong, private secret key for Flask sessions.
- Before deploying publicly, configure production security settings and review authentication and data handling.

## 🚀 Future Improvements

- Connect a live AI model for itinerary generation.
- Save and manage previous trips.
- Add a trip history dashboard.
- Improve real-time hotel and restaurant data.
- Add additional language support.
- Deploy the application online.

## 🎯 Project Goal

The goal of TripGenie AI is to make travel planning simpler by bringing itinerary generation, budget estimation, weather information, and destination exploration into one application.

## 👩‍💻 Author

**Harshitha Reddy**

Developed as a personal learning project to explore web development, Python, Flask, database integration, and AI-powered travel planning.

## 📄 License

This project is currently available for learning and demonstration. Add a license file if you want to specify the terms under which others may use, modify, or distribute your code.
