#!/bin/bash

#sources: Tutorials https://www.youtube.com/playlist?list=PLlrxD0HtieHh9ZhrnEbZKhzk0cetzuX7l

#task completed on Mac OS(Sequoia 15.0.1), using VS Code(1.94.2) editor and embedded bash terminal. Tested on veridian server (user- 24103685)

#1)Pseudocode:
# 1.Set default log file location(user's home directory) and variables
# Create the log directory and log file if they doesn't exist
# Reference: Lab 5 (Creating Scripts and Functions)

# 2.Show a menu with options to:
# Reference: Lab 6 (Backgrounding, Signals, Process Management)

# 3.Process Management Options (inside menu loop)

# option 1 - Show User Processes:
    #Get the current username using `whoami`
# Reference: Lab 3 (Pipes and Redirection) - commands like ps and awk

# option 2 - Show All Processes:
    #Display all running system processes
# Reference: Lab 3 (Pipes and Redirection)

# option 3 - Search for processes:
#Prompt user to choose between searching by:
#     1. Username
#     2. Program name
# If user chooses to search by username:
#     Prompt user for a username
#     Show processes related to that username
# Reference: Lab 5 (Functions and Input/Output)

# If user chooses to search by program name:
#     Prompt user for a program name
#     Show processes matching the program name

#option 4 - Send a signal to a process:
#   Prompt user to input a PID
#   Check if the PID exists
#   If PID exists, prompt user for the type of signal (e.g., TERM, KILL)
#   Confirm with user before sending the signal
#   If confirmed, send the signal and log the action in the log file
# Reference: Lab 6 (Trapping Signals)

# option 5 - Set log file location:
#   Prompt user for a new log directory
#   Check if the directory exists
#   If valid, update the log file location
#  If invalid, show an error message
# Reference: Lab 5 (Creating Scripts and Functions)

# option 6 - View logs:
#Display the contents of the log file

# option 7 - Quit:
#   - Print "Exiting..." and break the loop to terminate the program

# If user inputs an invalid choice:
#   show an error message and return to the menu

# Repeat the menu options until the user selects option 7 (Quit)
# Reference: Lab 5 (Creating Scripts and Functions)




#2)Code
#default log file location
default_log_dir="$HOME"
log_dir="$default_log_dir"
log_file="$log_dir/logs.txt"

mkdir -p "$log_dir"
touch "$log_file"

#show menu
show_menu() {
    echo "*******************************"
    echo " Process Management Toolkit"
    echo "*******************************"
    echo "1. User processes"
    echo "2. All processes"
    echo "3. Search for process by user or binary name"
    echo "4. Send a signal to a process"
    echo "5. Set log location"
    echo "6. View log of sent signals"
    echo "7. Quit"
    echo "*******************************"
    echo -n "Select an option: "
    read choice
}

#show current user's processes
function show_user_processes {
    CURRENT_USER=$(whoami)
    echo "Processes for user: $CURRENT_USER"
    printf "%-10s %-8s %-5s %-5s %-8s %-8s %-7s %-6s %-6s %s\n" \
           "USER" "PID" "%CPU" "%MEM" "VSZ" "RSS" "TTY" "STAT" "STARTED" "TIME CMD"
    ps -eo user,pid,%cpu,%mem,vsz,rss,tty,stat,start,time,cmd --sort=pid | awk -v user="$CURRENT_USER" '$1 == user'
}

#show all processes
show_all_processes() {
    echo "Showing all system processes:"
    printf "%-10s %-8s %-5s %-5s %-8s %-8s %-7s %-6s %-6s %s\n" \
        "USER" "PID" "%CPU" "%MEM" "VSZ" "RSS" "TTY" "STAT" "STARTED" "TIME CMD"
    ps -eo user,pid,%cpu,%mem,vsz,rss,tty,stat,start,time,cmd --sort=pid | awk 'NR > 1'
}

#search for a user's processes
finduser() {
    read -p "Type username or UID: " username
    if id "$username" &>/dev/null; then
        echo "Showing processes for user $username:"
        printf "%-10s %-8s %-5s %-5s %-8s %-8s %-7s %-6s %-6s %s\n" \
            "USER" "PID" "%CPU" "%MEM" "VSZ" "RSS" "TTY" "STAT" "STARTED" "TIME CMD"
        ps -eo user,pid,%cpu,%mem,vsz,rss,tty,stat,start,time,cmd --sort=pid | awk -v user="$username" '$1 == user'
    else
        echo "Error: User $username does not exist."
    fi
    read -p "Hit enter to go back"
}

#search for a binary's processes
findprogram() {
    read -p "Type program name: " program
    echo "Searching for processes matching $program:"
    ps aux | grep "$program" | grep -v grep
    read -p "Hit enter to go back"
}

#send signals to a process
send_signal() {
    echo -n "Enter PID to send signal to: "
    read pid
    if ! ps -p "$pid" > /dev/null 2>&1; then
        echo "Error: PID $pid does not exist."
        return
    fi
    echo -n "Enter signal (e.g., TERM, KILL, STOP): "
    read signal
    echo -n "Are you sure (y/n): "
    read confirm
    if [[ "$confirm" == "y" ]]; then
        if kill -"$signal" "$pid" 2>/dev/null; then
            log_entry="$(date): Signal $signal sent to PID $pid"
            echo "$log_entry" | tee -a "$log_file"
        else
            echo "Error: Failed to send signal."
        fi
    else
        echo "Operation canceled."
    fi
}

#set log file location
set_log_location() {
    echo -n "Enter log directory: "
    read new_log_dir
    if [[ -d "$new_log_dir" ]]; then
        log_dir="$new_log_dir"
        log_file="$log_dir/logs.txt"
        touch "$log_file" || { echo "Error: Unable to create log file."; return; }
        echo "Log directory set to $log_dir"
    else
        echo "Error: Directory does not exist."
    fi
}

#show the log file
view_log() {
    if [[ -f "$log_file" ]]; then
        echo "Log of sent signals:"
        cat "$log_file"
    else
        echo "Log file not found."
    fi
}

#main program
while true; do
    show_menu
    case $choice in
        1) show_user_processes ;;
        2) show_all_processes ;;
        3)
            echo "Choose search option:"
            echo "1 - by username"
            echo "2 - by program name"
            read search_choice
            case $search_choice in
                1) finduser ;;
                2) findprogram ;;
                *) echo "Invalid choice, returning to menu." ;;
            esac
        ;;
        4) send_signal ;;
        5) set_log_location ;;
        6) view_log ;;
        7) echo "Exiting..."; break ;;
        *) echo "Invalid option, please try again." ;;
    esac
done
