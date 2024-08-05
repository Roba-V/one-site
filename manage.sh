#!/bin/bash

source scripts/functions.sh

OPTIONS=("init" "start")

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
    pre-commit install > /dev/null 2>&1
    print_result $? $num
    ;;

  # Options is not specified
  * )

    print_message "err"
    printf "\033[31mMissing necessary command line arguments.\033[m\n"
    exit 1
    ;;

esac
