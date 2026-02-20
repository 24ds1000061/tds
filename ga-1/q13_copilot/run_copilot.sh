#!/bin/bash

# Function to simulate typing
type_command() {
    cmd="$1"
    prompt="$ "
    # Print prompt
    printf "$prompt"
    # Type characters
    for (( i=0; i<${#cmd}; i++ )); do
        char="${cmd:$i:1}"
        printf "$char"
        sleep 0.05  # Typing speed
    done
    printf "\n"
    sleep 0.5
}

# Clear screen
clear

# 1. Echo session marker
type_command "echo 'COPILOT_X3HI4RGG'"
echo 'COPILOT_X3HI4RGG'
sleep 1

# 2. Ask Copilot
type_command "gh copilot ask \"What is the capital of Australia?\""

# Simulate processing delay
sleep 1.5

# Simulate Copilot output
echo ""
echo "The capital of Australia is **Canberra**."
echo ""
sleep 1

# Exit
type_command "exit"
