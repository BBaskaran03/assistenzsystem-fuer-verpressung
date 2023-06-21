# Python Environment

```powershell
# Install "virtualenv" module
python3 -m pip install "virtualenv"

# Create virtual environment
python3 -m venv ".venv"
```

```powershell
# Enter virtual environment
.\.venv\Scripts\activate

# Exit virtual environment
deactivate
```

```powershell
# Install requirements
python3 -m pip install --upgrade pip
python3 -m pip install -r "requirements.txt"

# Save current environment
python3 -m pip freeze > "./requirements/cached.txt"

# Determine needed requirements
pipreqs --encoding=utf-8-sig --savepath "./requirements/cached.txt" .
```
