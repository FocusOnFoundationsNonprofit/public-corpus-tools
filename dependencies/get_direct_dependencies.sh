#!/bin/bash

# Run this script from the root folder of the project corpus-tools
# bash dependencies/get_direct_dependencies.sh

# Store the original directory
ORIGINAL_DIR=$(pwd)
echo "Original directory: $ORIGINAL_DIR"

# Create the "code file copies" folder if it doesn't exist
CODE_COPIES_DIR="$ORIGINAL_DIR/dependencies/code file copies"
mkdir -p "$CODE_COPIES_DIR"

# Remove all existing files in the "code file copies" folder
rm -f "$CODE_COPIES_DIR"/*

# List of paths to the files that need to be copied
FILES_TO_COPY=(
  "primary/fileops.py"
  "primary/transcribe.py"
  "primary/llm.py"
  "primary/vectordb.py"
  "primary/rag.py"
  "primary/docwork.py"
  "primary/conversion.py"
  "primary/structured.py"
  "primary/corpuses.py"
  "primary/aws.py"
  "tests/test_fileops.py"
  "tests/test_transcribe.py"
  "tests/test_llm.py"
  "docs/codeindex/create_codeindex.py"
  "docs/vis/codebase_graph_vis.py"
)

# Copy files to the "code file copies" folder
for file in "${FILES_TO_COPY[@]}"; do
  if [ -f "$file" ]; then
    cp "$file" "$CODE_COPIES_DIR/" && echo "Copied $file to code file copies folder" || echo "Error: Could not copy $file"
  else
    echo "Warning: File $file does not exist"
  fi
done

# Generate requirements.txt using pipreqs
echo "Generating requirements.txt..."
if ! command -v pipreqs &> /dev/null; then
    echo "pipreqs could not be found. Please install it using 'pip install pipreqs'"
    exit 1
fi

# Run pipreqs on the dependencies folder
pipreqs "$ORIGINAL_DIR/dependencies" --force

# Get current date in the required format
CURRENT_DATE=$(date +"%Y-%m-%d")

# Check if requirements.txt was created in the dependencies folder
if [ -f "$ORIGINAL_DIR/dependencies/requirements.txt" ]; then
    # Rename requirements.txt with the current date and piprecs in the dependencies folder
    mv "$ORIGINAL_DIR/dependencies/requirements.txt" "$ORIGINAL_DIR/dependencies/requirements_${CURRENT_DATE}_piprecs.txt"
    echo "Created requirements_${CURRENT_DATE}_piprecs.txt in the dependencies folder"
    
    # Add pipreqs to the requirements file
    echo "pipreqs>=0.5.0,<0.6.0" >> "$ORIGINAL_DIR/dependencies/requirements_${CURRENT_DATE}_piprecs.txt"

    # Add the list of copied files to the requirements file
    echo -e "\n\n# Files used to generate these requirements:" >> "$ORIGINAL_DIR/dependencies/requirements_${CURRENT_DATE}_piprecs.txt"
    for file in "${FILES_TO_COPY[@]}"; do
        echo "# $file" >> "$ORIGINAL_DIR/dependencies/requirements_${CURRENT_DATE}_piprecs.txt"
    done

    # Create a copy named requirements_.txt
    cp "$ORIGINAL_DIR/dependencies/requirements_${CURRENT_DATE}_piprecs.txt" "$ORIGINAL_DIR/dependencies/requirements_.txt"
    echo "Also created requirements_.txt in the dependencies folder"
else
    echo "Error: requirements.txt was not created in the dependencies folder. Check the pipreqs output for errors."
fi

echo "Process completed successfully."