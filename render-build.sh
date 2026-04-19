#!/usr/bin/env bash
# exit on error
set -o errexit

# Build the frontend
cd frontend
npm install
npm run build
cd ..

# Install Python dependencies
pip install -r requirements.txt
