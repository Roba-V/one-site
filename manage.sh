#!/bin/bash

source scripts/constants.sh
source scripts/functions.sh

case $1 in

  # Initialization Process
  "${OPTIONS[0]}" )

    print_process "Initializing Application"

    check_python_version
    cd backend || exit

    print_message "info"
    if [ ! -e venv ]; then
      print_count "Creating virtual environments"
      num=$?
      python -m venv venv > /dev/null
      print_result $? $num
    else
      printf "Found an existing virtual environments.\n"
    fi

    source venv/bin/activate

    print_message "info"
    print_count "Installing all dependencies"
    num=$?
    python -m pip install --upgrade pip > /dev/null
    python -m pip install poetry > /dev/null
    poetry install --no-root > /dev/null
    print_result $? $num

    print_message "info"
    print_count "Installing pre-commit hooks"
    num=$?
    pre-commit install > /dev/null
    print_result $? $num
    ;;

  # Options is not specified
  * )

    print_message "err"
    printf "Missing necessary command line arguments.\n"
    exit 1
    ;;

esac
