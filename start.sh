#!/bin/bash

# =============================================================================
# DnD Roller Bot - Startup Script
# =============================================================================
# This script automates the setup and startup of the DnD Roller Discord bot.
# It handles virtual environment creation, dependency installation, and
# launching the bot.
#
# Usage: ./start.sh
# =============================================================================

set -e  # Exit immediately if a command fails

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
REQUIREMENTS_FILE="${SCRIPT_DIR}/requirements.txt"
MAIN_SCRIPT="${SCRIPT_DIR}/dnd_roller.py"
PYTHON_VERSION="python3.12"

# -----------------------------------------------------------------------------
# Colors for output
# -----------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# -----------------------------------------------------------------------------
# Check Python Installation
# -----------------------------------------------------------------------------
check_python() {
    log_info "Checking Python installation..."

    if command -v ${PYTHON_VERSION} &> /dev/null; then
        PYTHON_CMD="${PYTHON_VERSION}"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        log_warning "Python 3.12 not found, using $(python3 --version)"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        log_warning "Using default python: $(python --version)"
    else
        log_error "Python is not installed. Please install Python 3.12 or later."
        exit 1
    fi

    log_success "Using: $(${PYTHON_CMD} --version)"
}

# -----------------------------------------------------------------------------
# Create Virtual Environment
# -----------------------------------------------------------------------------
create_venv() {
    if [ ! -d "${VENV_DIR}" ]; then
        log_info "Creating virtual environment..."
        ${PYTHON_CMD} -m venv "${VENV_DIR}"
        log_success "Virtual environment created at ${VENV_DIR}"
    else
        log_info "Virtual environment already exists."
    fi
}

# -----------------------------------------------------------------------------
# Activate Virtual Environment
# -----------------------------------------------------------------------------
activate_venv() {
    log_info "Activating virtual environment..."
    source "${VENV_DIR}/bin/activate"
    log_success "Virtual environment activated."
}

# -----------------------------------------------------------------------------
# Install Dependencies
# -----------------------------------------------------------------------------
install_dependencies() {
    log_info "Checking and installing dependencies..."

    # Upgrade pip first
    python -m pip install --upgrade pip --quiet

    # Check if requirements.txt exists
    if [ -f "${REQUIREMENTS_FILE}" ]; then
        python -m pip install -r "${REQUIREMENTS_FILE}" --quiet
        log_success "Dependencies installed from requirements.txt"
    else
        # Install minimum required packages
        log_warning "requirements.txt not found. Installing minimum dependencies..."
        python -m pip install discord.py --quiet
        log_success "discord.py installed."
    fi
}

# -----------------------------------------------------------------------------
# Start the Bot
# -----------------------------------------------------------------------------
start_bot() {
    log_info "Starting DnD Roller bot..."
    echo ""
    echo "=============================================="
    echo "🎲 DnD Roller Bot Starting..."
    echo "=============================================="
    echo ""

    python "${MAIN_SCRIPT}"
}

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
main() {
    echo ""
    echo "=============================================="
    echo "🎲 DnD Roller Bot - Setup & Startup Script"
    echo "=============================================="
    echo ""

    # Change to script directory
    cd "${SCRIPT_DIR}"

    # Run setup steps
    check_python
    create_venv
    activate_venv
    install_dependencies

    echo ""

    # Start the bot
    start_bot
}

# Run main function
main
