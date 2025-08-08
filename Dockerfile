# Windows Server Core + Python 3.11
FROM mcr.microsoft.com/windows/python:3.11-windowsservercore-ltsc2022

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

WORKDIR C:\\app

# Install dependencies first for better layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt ; `
    pip install --no-cache-dir waitress

# Copy the rest
COPY . .

# Environment (override at runtime with --env or --env-file)
ENV FLASK_ENV=production `
    SPOT_CLIENT_ID=7cf6017e458346039146bbfaa9189072 `
    SPOT_CLIENT_SECRET=199e28e8eee945b384101cc1eda57b10 `
    SPOT_REDIRECT_URI=https://google.com/ `
    YT_CLIENT_ID=929354734828-ubnkl33es5sjr4ncf1vcpchcotmr4l46.apps.googleusercontent.com `
    YT_CLIENT_SECRET=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

# Flask port
EXPOSE 5000

# Serve the Flask app factory from app/__init__.py
# Equivalent to: from app import create_app; waitress-serve --listen=*:5000 app:create_app()
CMD ["waitress-serve", "--listen=*:5000", "app:create_app()"]