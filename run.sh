#!/bin/bash

# Color codes for better output visualization
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if Python 3.8+ is installed
info "Checking for Python 3.8+..."
if ! command -v python3 &> /dev/null; then
    error "Python 3.8+ is required but not found. Install Python and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print("".join(map(str, sys.version_info[:2])))')
if [[ $PYTHON_VERSION -lt 38 ]]; then
    error "Python version 3.8+ is required. Found Python $PYTHON_VERSION."
    exit 1
fi

success "Python 3.8+ detected."
info "Setting up virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
if [[ -f "requirements.txt" ]]; then
    info "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    success "Dependencies installed successfully."
else
    error "requirements.txt not found!"
    exit 1
fi

# Check if TypeScript code is compiled (i.e., .js files exist in static/dist)
if ! find static/dist -name "*.js" -type f | grep -q .; then
    warning "Compiled TypeScript files not found. Checking for Node.js and npm..."
    
    # Check if Node.js is installed
    if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
        error "Node.js and npm are required but not found. Install them and try again."
        exit 1
    fi
    
    success "Node.js and npm detected."
    info "Installing Node.js dependencies and compiling TypeScript..."
    npm install
    npm run build || { error "TypeScript compilation failed!"; exit 1; }
    success "TypeScript compiled successfully."
else
    success "Compiled TypeScript files found. Skipping compilation."
fi

# Run the application
info "Starting app.py..."
python3 app.py
