#!/bin/bash

if [ ! -d "$1" ]; then
    echo "Virtual environment directory '$1' not found."
    exit 1
fi

# Check the operating system
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows: Use the Scripts/activate script
    source "$1/Scripts/activate"
else
    # Unix-like systems: Use the bin/activate script
    source "$1/bin/activate"
fi

pip install -r ./app/requirements.txt
