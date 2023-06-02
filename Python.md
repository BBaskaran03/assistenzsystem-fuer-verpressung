# Python Environment

```powershell
# Install "virtualenv" module
pip install "virtualenv"

# Create virtual environment
python -m venv ".venv"
```

```powershell
# Enter virtual environment
.\.venv\Scripts\activate

# Exit virtual environment
deactivate
```

```powershell
# Install requirements
python.exe -m pip install --upgrade pip
python.exe -m pip install -r "requirements.txt"

# Save dependencies
python.exe -m pip freeze > "requirements.txt"
```
