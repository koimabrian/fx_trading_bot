# Purpose: Defines the Docker container setup for the FX Trading Bot using Windows
FROM mcr.microsoft.com/windows/servercore:ltsc2019

# Install Python 3.10
RUN powershell -Command \
    Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe -OutFile python-installer.exe; \
    Start-Process -Wait -FilePath python-installer.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1'; \
    Remove-Item python-installer.exe

# Install pip and dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
WORKDIR C:\app
COPY . .

# Set up environment variables
ENV PYTHONUNBUFFERED=1
ENV MT5_LOGIN=208711745
ENV MT5_PASSWORD=Brian@2025
ENV MT5_SERVER=Exness-MT5Trial9

# Define entrypoint
ENTRYPOINT ["python", "src\\main.py"]