# Expense Tracker
## Description
A simple python-based command line tool designed to help users track their expenses. Users can add, list, and delete expenses using this tool.
## Installation
### 1. Clone this repository
```
git clone git@github.com:itsme-mario/Expense-Tracker.git
cd Expense-Tracker
```
### 2.a. Run the Python Script
```
python3 expense_tracker.py --help
```
### 2.b. Or use it as a Command-Line Tool
1. Open your .bashrc:
```
nano ~/.bashrc
```
2. Add an alias (you can find your path by entering pwd):
```
alias expense-tracker="python3 /path_to_script/expense_tracker.py"
```
3. Save/ reload your shell config:
```
source ~/.bashrc
```
4. Now you can use expense-tracker from the terminal:
```
expense-tracker --help
```
###
Project inspiration came from [roadmap.sh](https://roadmap.sh/backend). You can find more about how to build this project by visiting [Expense Tracker](https://roadmap.sh/projects/expense-tracker).
