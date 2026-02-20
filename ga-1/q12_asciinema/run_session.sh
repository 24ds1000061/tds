#!/bin/bash

# Function to simulate typing
type_command() {
    cmd="$1"
    # Delay before typing
    sleep 0.5
    # Print command with prompt and newline
    echo "$ $cmd"
    sleep 0.2
    # Execute command
    eval "$cmd"
    sleep 0.5
}

# Clear screen for clean recording
clear

# Execute commands
type_command "echo 'SESSION_VFZVSQW4'"
type_command "ls -la"
type_command "cat /etc/os-release | head -5"
type_command "whoami"

# Signal end of recording
echo "exit"
