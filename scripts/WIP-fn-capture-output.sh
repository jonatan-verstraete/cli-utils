# # Initialize a temporary file to store command outputs
# SESSION_OUTPUT_FILE=$(mktemp)

# # Initialize an array to hold the captured outputs
# declare -a OUTPUTS

# # Function to capture command output
# capture_output() {
#   # Capture the output of the last command, including stdout and stderr
#   local cmd_output
#   cmd_output=$(history 1 | sed 's/^[ ]*[0-9]\+[ ]*//')  # Get the last command
#   eval "$cmd_output" &> >(tee -a "$SESSION_OUTPUT_FILE" | tail -n 1)
#   OUTPUTS+=("$(tail -n 1 "$SESSION_OUTPUT_FILE")")  # Save the last output to the array
# }

# # Function to get the most recent command's output
# :last() {
#   if [ ${#OUTPUTS[@]} -gt 0 ]; then
#     echo "${OUTPUTS[-1]}"  # Print the most recent output
#   else
#     echo "No output captured yet."
#   fi
# }

# # Function to get the Nth previous output (e.g., last -1, last -2, etc.)
# :lastn() {
#   local n=$1
#   if [ ${#OUTPUTS[@]} -gt "$n" ]; then
#     echo "${OUTPUTS[-(n+1)]}"  # Print the Nth last output
#   else
#     echo "Not enough previous outputs."
#   fi
# }

# # Clear the output file when the session ends
# trap "rm -f $SESSION_OUTPUT_FILE" EXIT

# # Hook into the PROMPT_COMMAND to capture output after each command
# PROMPT_COMMAND="capture_output"
