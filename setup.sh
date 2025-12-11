#!/bin/bash

# Create conda environment
conda create -n talking-machines python=3.10 -y

# Install packages from requirements.txt
conda run -n talking-machines pip install -r requirements.txt

# Create necessary directories
mkdir -p pdfs

# Copy environment file template
if [ -f .env.example ]; then
    cp .env.example .env
    echo "Created .env file - don't forget to add your API keys!"
else
    echo "Warning: .env.example not found"
fi

echo ""
echo "Setup complete!"
echo "Activate the environment with: conda activate talking-machines"
