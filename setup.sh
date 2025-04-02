#!/bin/bash

# Create and activate conda environment
conda create -n talking-machines python=3.10 -y
conda activate talking-machines

# Install packages using conda
conda install -c conda-forge python-dotenv pypdf2 -y

# Install packages using pip
pip install openai==1.12.0 elevenlabs==0.2.27

# Create necessary directories
mkdir -p pdfs

# Copy environment file template
cp .env.example .env

echo "Setup complete! Don't forget to edit .env with your API keys." 