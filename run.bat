@echo off
setlocal enabledelayedexpansion

:: Color codes for Windows console
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

:: Print colored messages
:info
echo %BLUE%[INFO]%NC% %~1
exit /b

:success
echo %GREEN%[SUCCESS]%NC% %~1
exit /b

:warning
echo %YELLOW%[WARNING]%NC% %~1
exit /b

:error
echo %RED%[ERROR]%NC% %~1
exit /b

:: Make sure we're running from the project root
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%" || (call :error "Cannot change to script directory" && exit /b 1)

:: Create data directory if it doesn't exist
if not exist "data" mkdir data

:: Function to check Python version
:check_python
call :info "Checking Python version..."
python --version >nul 2>&1
if errorlevel 1 (
    call :error "Python not found. Please install Python 3.10+"
    exit /b 1
)

for /f "tokens=2 delims= " %%a in ('python --version') do set "PYTHON_VERSION=%%a"
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
)

if %MAJOR% geq 3 if %MINOR% geq 10 (
    call :success "Python %PYTHON_VERSION% detected"
) else (
    call :error "Python 3.10+ is required (found %PYTHON_VERSION%)"
    exit /b 1
)
exit /b 0

:: Function to check for Node.js and npm
:check_node
call :info "Checking if Node.js is available..."
node --version >nul 2>&1
if errorlevel 1 (
    call :warning "Node.js not found. Skipping TypeScript build steps."
    set "SKIP_NODE_STEPS=true"
) else (
    for /f %%a in ('node -v') do set "NODE_VERSION=%%a"
    for /f %%a in ('npm -v') do set "NPM_VERSION=%%a"
    call :success "Node.js %NODE_VERSION% and npm %NPM_VERSION% detected"
    set "SKIP_NODE_STEPS=false"
)
exit /b 0

:: Function to set up Python virtual environment
:setup_venv
call :info "Setting up Python virtual environment..."

:: Get Python version from .python-version file if it exists
if exist ".python-version" (
    set /p PYTHON_VERSION=<.python-version
) else (
    for /f "tokens=2 delims= " %%a in ('python --version') do set "PYTHON_VERSION=%%a"
)

:: Check if venv exists
if not exist ".venv" (
    :: Check if uv is installed
    uv --version >nul 2>&1
    if not errorlevel 1 (
        call :info "Using uv to create virtual environment..."
        uv venv -p "python%PYTHON_VERSION%" .venv
    ) else (
        call :info "Using venv module to create virtual environment..."
        python -m venv .venv
    )
)

:: Activate virtual environment
call .venv\Scripts\activate.bat

:: Check if uv is installed
uv --version >nul 2>&1
if not errorlevel 1 (
    call :info "Using uv for package installation..."
    uv pip install -q -r pyproject.toml
) else (
    call :warning "uv not found. Using pip instead. Consider installing uv for faster package installation."
    if exist "requirements.txt" (
        pip install -q -r requirements.txt
    ) else (
        pip install -q -r pyproject.toml
    )
)

call :success "Python environment set up successfully"
exit /b 0

:: Function to install Node.js dependencies
:setup_node
if "%SKIP_NODE_STEPS%"=="true" (
    call :info "Skipping Node.js setup (not installed)"
    if not exist "src\static\dist\index.js" (
        call :error "Compiled JavaScript not found and Node.js not available to build it"
        call :error "Please install Node.js or add the compiled JavaScript files"
        exit /b 1
    )
    call :info "Using existing compiled JavaScript"
) else (
    call :info "Setting up Node.js dependencies..."
    npm install
    call :success "Node.js dependencies installed"
)
exit /b 0

:: Function to build TypeScript
:build_typescript
if "%SKIP_NODE_STEPS%"=="true" (
    call :info "Skipping TypeScript build (Node.js not installed)"
) else (
    call :info "Building TypeScript..."
    npx tsc
    call :success "TypeScript build complete"
)
exit /b 0

:: Function to start the application
:run_app
call :info "Starting application..."
python .\src\app.py
exit /b 0

:: Main execution
:main
call :info "Starting setup process..."
set "SKIP_NODE_STEPS=false"

call :check_python
call :check_node
call :setup_venv
call :setup_node
call :build_typescript

call :success "Setup complete! Starting application now."
call :run_app

endlocal 