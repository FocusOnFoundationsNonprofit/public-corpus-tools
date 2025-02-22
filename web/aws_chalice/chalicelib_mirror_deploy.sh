# ===== START OF FILE chalicelib_mirror_deploy.sh =====
# file_path: web/aws_chalice/chalicelib_mirror_deploy.sh
# contains: bash script to mirror code from primary/ to chalicelib/
#          and replace environment variables in config.json with actual values from .env
#          and deploy the chalice application

#!/bin/bash

# Command to run in terminal from the directory of the Chalice project, e.g., 'hmac-hash'
# ../chalicelib_mirror_deploy.sh

# Enable debug mode (optional for troubleshooting)
#set -x

# Do replacement of environment variable in config.json first so that the used secrets can be updated in the .py module headers.

### LOAD SECRET ENV VARIABLES FROM .ENV INTO CHALICE CONFIG.JSON

# Function to find the repository root
find_repo_root() {
    local current_dir="$PWD"
    while [[ "$current_dir" != "/" ]]; do
        if [[ -d "$current_dir/.git" ]]; then
            echo "$current_dir"
            return 0
        fi
        current_dir="$(dirname "$current_dir")"
    done
    echo "Repository root not found" >&2
    return 1
}

# Find the repository root
REPO_ROOT=$(find_repo_root)
if [[ $? -ne 0 ]]; then
    echo "Error: Unable to locate repository root"
    exit 1
fi

# Path to the .env file
ENV_FILE="$REPO_ROOT/.env"

# Path to the config.json file (relative to the current script location)
CONFIG_JSON=".chalice/config.json"

# Check if the config.json file exists
if [ ! -f "$CONFIG_JSON" ]; then
  echo "config.json file not found at $CONFIG_JSON"
  exit 1
fi

# Create a temporary copy of config.json
cp "$CONFIG_JSON" "${CONFIG_JSON}.temp"

# Function to replace secrets with actual values from .env and create a list of environment variable keys
replace_secrets() {
    local config_file="$1"
    local env_file="$2"
    local in_env_section=false
    local temp_file="${config_file}.tmp"
    ENV_VAR_KEYS=()

    while IFS= read -r line; do
        if [[ $line == *"environment_variables"* ]]; then
            in_env_section=true
            echo "$line" >> "$temp_file"
        elif [[ $in_env_section == true && $line == *"}"* ]]; then
            in_env_section=false
            echo "$line" >> "$temp_file"
        elif [[ $in_env_section == true ]]; then
            key=$(echo "$line" | sed -E 's/.*"([^"]+)": *"([^"]+)".*/\1/')
            env_key=$(echo "$line" | sed -E 's/.*"([^"]+)": *"([^"]+)".*/\2/')
            value=$(grep "^$env_key *=" "$env_file" | sed 's/^[^=]*= *//g' | sed 's/^"//; s/"$//; s/ *#.*$//' | tr -d '"')
            
            if [ -n "$value" ]; then
                replaced_line=$(echo "$line" | sed -E "s/(\"$key\": *)\"[^\"]*\"/\1\"$value\"/")
                echo "$replaced_line" >> "$temp_file"
                value_preview="${value:0:12}..."
                echo "Replaced with actual secret: $line -> first 12 chars: $value_preview" >&2
                ENV_VAR_KEYS+=("$key")
            else
                echo "Error: Value for $env_key not found in $env_file" >&2
                rm "$temp_file"
                exit 1
            fi
        else
            echo "$line" >> "$temp_file"
        fi
    done < "$config_file"

    mv "$temp_file" "$config_file"
}

# Replace secrets
if [ -f "$ENV_FILE" ]; then
    replace_secrets "$CONFIG_JSON" "$ENV_FILE"
else
    echo "Error: $ENV_FILE not found"
    exit 1
fi


### SYNC CODE FILES TO CHALICE LIB

# Define the target Chalice lib folder within the current directory
TARGET_FOLDER="./chalicelib"

# Check if target folder exists - if not, skip module copying
if [ ! -d "$TARGET_FOLDER" ]; then
    echo "Warning: Chalice lib folder '$TARGET_FOLDER' does not exist. Skipping module copying."
else
    # List of paths to the files that have the code you want copied into the chalicelib files
    FILES_TO_COPY=(
        "../../../primary/aws.py"
        "../../../primary/fileops.py"
        "../../../primary/llm.py"
        "../../../primary/rag.py"
        "../../../primary/vectordb.py"
        "../../../primary/rag_prompts_routes.py"
        # Add more file paths as needed
    )

    # Delimiter to indicate where to start syncing code
    DELIMITER="# ---START OF SYNCED CODE---"

    # Iterate over the specified files
    for file in "${FILES_TO_COPY[@]}"; do
        # Get the base name of the file (without directory)
        base_name=$(basename "$file")

        # Find the corresponding file in the chalice lib folder
        target_file="$TARGET_FOLDER/$base_name"

        if [ -f "$target_file" ] && [ -f "$file" ]; then
            echo "Updating '$target_file' with code from '$file'"

            # Extract content from the target file above the delimiter
            awk -v delim="$DELIMITER" '
                $0 ~ delim {exit}
                {print}
            ' "$target_file" > temp_target_header.py

            # Extract content from the source file including and below the delimiter
            awk -v delim="$DELIMITER" '
                $0 ~ delim {p=1}
                p
            ' "$file" > temp_source_code.py

            # Combine the target header and source code
            cat temp_target_header.py temp_source_code.py > "$target_file"

            # Clean up temporary files
            rm temp_target_header.py temp_source_code.py
        else
            echo "Either source file '$file' or target file '$target_file' does not exist. Skipping."
        fi
    done

    # Function to process Python module headers
    process_module_header() {
        local file="$1"
        local temp_file="${file}.tmp"
        local in_secrets_section=false
        local in_synced_code=false

        while IFS= read -r line; do
            if [[ $line == *"# ---API KEYS AND SECRETS---"* ]]; then
                in_secrets_section=true
                echo "$line" >> "$temp_file"
            elif [[ $line == *"# ---START OF SYNCED CODE---"* ]]; then
                in_synced_code=true
                in_secrets_section=false
                echo "$line" >> "$temp_file"
            elif [[ $in_secrets_section == true ]]; then
                if [[ $line == *"from dotenv"* || $line == *"load_dotenv"* ]]; then
                    continue  # Skip these lines
                elif [[ $line == *"="* && ! $line == \#* ]]; then
                    var_name=$(echo "$line" | cut -d'=' -f1 | tr -d ' ')
                    if [[ " ${ENV_VAR_KEYS[@]} " =~ " ${var_name} " ]]; then
                        echo "$var_name = os.environ[\"$var_name\"]" >> "$temp_file"
                    else
                        echo "# $line  # Not in chalice/config.json" >> "$temp_file"
                    fi
                else
                    echo "$line" >> "$temp_file"
                fi
            else
                echo "$line" >> "$temp_file"
            fi
        done < "$file"

        mv "$temp_file" "$file"
    }

    # Process Python module headers
    for file in "${FILES_TO_COPY[@]}"; do
        target_file="$TARGET_FOLDER/$(basename "$file")"
        if [ -f "$target_file" ]; then
            echo "Processing header of $target_file"
            process_module_header "$target_file"
        else
            echo "Target file $target_file not found. Skipping header processing."
        fi
    done

    # Replace "from primary." with "from chalicelib."
    echo "Replacing 'from primary.' with 'from chalicelib.' in Python modules..."
    for py_file in "$TARGET_FOLDER"/*.py; do
        if [ -f "$py_file" ]; then
            echo "Processing $py_file"
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS (BSD) sed
                sed -i '' 's/from primary\./from chalicelib./' "$py_file"
            else
                # GNU sed
                sed -i 's/from primary\./from chalicelib./' "$py_file"
            fi
        fi
    done
fi

# Check API Gateway validation state BEFORE deployment
echo "Checking current API Gateway validation state..."
app_name=$(basename "$PWD")
cd ../../../
VALIDATION_STATE=$(python3 -c "
from primary.aws_valid import check_validation_setup
try:
    api_name = '${app_name}'
    validation_exists = check_validation_setup(api_name)
    print(f'API Gateway validation exists for {api_name}: {validation_exists}')
    print(str(validation_exists).lower())  # Convert to lowercase string
except Exception as e:
    print(f'Error checking validation: {str(e)}', file=sys.stderr)
    print('false')
" | tail -n 1)  # Only capture the last line
cd - > /dev/null

echo "Previous validation state: $VALIDATION_STATE"

# Modified user input section
# read -p "Check chalicelib files and config.json - Press Enter to continue with chalice deploy, or any other key to abort: " user_input

# if [ -z "$user_input" ]; then
# Auto-confirm by setting empty user input
user_input=""
if [ -z "$user_input" ]; then
    # Run chalice deploy
    echo "Running chalice deploy..."
    chalice deploy
    
    # Add a small delay to ensure API Gateway changes are propagated
    echo "Waiting for API Gateway changes to propagate..."
    sleep 5
    
    # Re-apply API Gateway validation only if it was present before
    if [ "$VALIDATION_STATE" = "true" ]; then
        echo "Restoring previous API Gateway validation state..."
        cd ../../../
        python3 -c "
from primary.aws_valid import setup_request_validation
import time
try:
    api_name = '${app_name}'
    print('Re-applying request validation...')
    # Try up to 3 times with delays
    for attempt in range(3):
        try:
            setup_request_validation(api_name)
            print('Successfully re-applied validation')
            break
        except Exception as e:
            if attempt < 2:
                print(f'Attempt {attempt + 1} failed, retrying in 5 seconds...')
                time.sleep(5)
            else:
                raise e
except Exception as e:
    print(f'Error setting up validation: {str(e)}')
"
        cd - > /dev/null
    else
        echo "Skipping API Gateway validation setup (was not present before deployment)"
    fi
else
    echo "Aborting chalice deploy..."
fi

# Restore the original config.json (this will run regardless of user input)
mv "${CONFIG_JSON}.temp" "$CONFIG_JSON"
echo "Restored original config.json"

# Disable debug mode (if enabled)
#set +x

echo "Script completed at $(date '+%Y-%m-%d %H:%M:%S')"

# ===== END OF FILE chalicelib_mirror_deploy.sh =====


