# Articurate - Declutter, Summarize, Listen

> A work in progress

## Setup

```
# Create a virtual env
py -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1

# Check if pip is running in venv
pip -V

# Install requirements
pip install -r requirements.txt

# Create database (dev.db) using migration scripts
flask db upgrade

# Generate First Feed (also tests core pipeline)
py .\feed_generator.py

# Run the application
py .\flask_app.py

# Install required nltk corpus
python3 setup_nltk.py
```

---

Storing only password hashes for security
using bcrypt algo to hash
handled by flask-bcrypt

Client side sessions
httponly cookies
handled by flask-login

---

## Team

Team Name : Codesmiths

Lakshay
https://github.com/lkiran5080  
lakshay5080@gmail.com

Sahil
https://github.com/SahilKumar7  
sahil.kumar5729@gmail.com
