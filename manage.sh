#!/bin/bash

source scripts/functions.sh

OPTIONS=("init" "start" "test")

case $1 in

  # Initialization Process
  "${OPTIONS[0]}" )

    print_process "Initializing Application"

    check_python_version
    cd backend || exit

    if [ -f pyproject.toml ]; then
      print_message "info"
      print_count "Installing all dependencies"
      num=$?
      poetry config virtualenvs.in-project true
      poetry install --no-root > /dev/null 2>&1
      print_result $? $num
    else
      print_message "err"
      printf "\033[31mCannot find pyproject.toml.\033[m\n"
      exit 1
    fi

    source .venv/bin/activate

    print_message "info"
    print_count "Installing pre-commit hooks"
    num=$?
    cd .. || exit
    pre-commit install
    print_result $? $num
    ;;

  # Unit Test Process
  "${OPTIONS[2]}" )

    print_process "Testing Application"

    DATETIME="$(date '+%Y%m%d_%H%M%S')"
    LOG_DIR="${PWD}/logs"
    LOG_FILE="${PWD}/logs/${DATETIME}.log"

    rst=0

    cd backend || exit
    source .venv/bin/activate

    print_message "info"
    print_count "Running test cases"
    num=$?
    mkdir -p "$LOG_DIR"
    printf "[Execute pytest]\n" >> "$LOG_FILE"
    coverage run --source=. -m pytest  >> "$LOG_FILE"
    print_result $? $num
    if [ $rst -ne $? ]; then rst=1; fi

    # Output test.log message
    printf "\t\033[37mSee \033[m"
    printf "\e]8;;file://%s\e\\%s\e]8;;\e\\" "$LOG_FILE" "log file"
    printf "\033[37m for more details.\033[m\n"

    print_message "info"
    print_count "Checking coverage of tests"
    num=$?
    printf "\n[Coverage Report]\n" >> "$LOG_FILE"
    cr_rst="$(coverage report --show-missing)"
    echo "$cr_rst" >> "$LOG_FILE"
    printf "\n[Generate Code Coverage HTML Report]\n" >> "$LOG_FILE"
    coverage html --title one-site-api  >> "$LOG_FILE"
    print_result $? $num
    if [ $rst -ne $? ]; then rst=1; fi

    COVERAGE_FILE="${PWD}/htmlcov/index.html"

    # Output the coverage info
    printf "\t\033[37m"
    echo "${cr_rst//$'\n'/$'\n\t'}"
    printf "\n\t\033[37mClick \033[m"
    printf "\e]8;;file://%s\e\\%s\e]8;;\e\\" "$COVERAGE_FILE" "here"
    printf "\033[37m to review the code coverage HTML report.\033[m\n"
    printf "\033[m\n"

    exit $rst
    ;;

  # Options is not specified
  * )

    print_message "err"
    printf "\033[31mMissing necessary command line arguments.\033[m\n"
    exit 1
    ;;

esac
