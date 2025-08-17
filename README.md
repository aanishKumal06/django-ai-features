# Doctor System with AI

A Django-based healthcare platform that leverages AI for medical advice generation and doctor recommendations.

## 🚀 Features

- AI-powered doctor search by symptoms
- Smart doctor recommendation system
- Evidence-based health advice generation

## 📁 Project Structure

```
doctor_system_with_ai/
├── advice/                  # AI advice generation module
│   ├── models/             # Data models
│   ├── services/           # AI integration services
│   └── templates/          # Frontend templates
│       └── advice/
│           ├── all_advice.html
│           └── health_advice.html
├── doctor/                  # Doctor management module
│   ├── models/
│   ├── services/
│   └── templates/
│       └── doctor/
│           └── index.html
└── core/                   # Core application settings
```

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- uv package manager
- Git

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/doctor_system_with_ai.git
cd doctor_system_with_ai
```

2. Create and activate virtual environment

```bash
# Create virtual environment
uv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on Linux/Mac
source venv/bin/activate
```

3. Install dependencies
```bash
uv sync
```


4. Setup database
```bash
python manage.py migrate
```

5. Start development server
```bash
python manage.py runserver
```


