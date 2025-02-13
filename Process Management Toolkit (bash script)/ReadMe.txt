# Process Management Toolkit

## Overview
The **Process Management Toolkit** is a Bash-based helper script designed for users who are not comfortable using the command line. This tool provides an easy-to-use menu for managing and monitoring system processes.

## Features
- Display detailed information about running processes:
  - Process Name
  - Process ID (PID)
  - Cumulated CPU time
  - Additional details retrieved from the `ps` command
- Interactive menu system for user-friendly navigation
- Continuous execution until the user selects the **quit** option
- View processes:
  - Running under the current user
  - Running under all system users
- Search functionality:
  - Search processes by username
  - Search processes by binary name
- Process signal management:
  - Send signals to processes
  - Log all signal-sending actions
  - Configurable log file location
  - Option to append to an existing log or start a new one
- Confirmation prompts for system-altering actions (e.g., killing or suspending processes)
- Graceful error handling to prevent script crashes

## Usage
### Running the Script
```bash
./process_management_toolkit.sh


```
### Menu Options
1. **View User Processes** – Displays processes owned by the user running the script.
2. **View All Processes** – Shows processes from all system users.
3. **Search Processes** – Allows searching by username or binary name.
4. **Send Signal to Process** – Sends a signal (e.g., kill, stop) to a specified process.
5. **View Process Log** – Displays the log of processes that received signals.
6. **Quit** – Exits the script safely.

## Logging
- Users can specify the location of the process log.
- If the log already exists, the script prompts the user to either **append** to it or **create a new one**.

## Software Engineering Considerations
- The script is modular, with separate functions handling different features.
- Function names are descriptive and self-explanatory.
- The code is well-commented to ensure readability and maintainability.

## Error Handling
- All menu actions that modify the system require user confirmation.
- If an error occurs, the script displays a clean error message and continues execution.

## Dependencies
- The script relies on standard Unix utilities (`ps`, `kill`, `grep`, etc.).
- Ensure Bash is installed on the system.

## Future Improvements
- Implement additional process filters (e.g., memory usage, priority levels).
- Enhance user interface with colored output for better readability.

---

Developed by Herman Dolhyi as part of **UCD HDip in Computer Science** coursework.

