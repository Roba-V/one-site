#!/bin/bash

# commands of manage.sh
PROCESS=("init" "start" "test")
# options of manage.sh
OPTIONS=("--dev" "--prod" "--back" "--front")
# current date time
DATETIME="$(date '+%Y%m%d%H%M%S')"
# absolute path of the app management script
APP_PATH=$(realpath -- "$0")
# absolute path of the app directory
APP_DIR=$(dirname "$APP_PATH")
# absolute path of log folder
LOG_DIR="$APP_DIR/logs"
# absolute path of log file
LOG_FILE="$APP_DIR/logs/$1_$DATETIME.log"

# check options for Execution Mode
IS_BACK=$(echo "$@" | grep "${OPTIONS[2]:2}")
IS_FRONT=$(echo "$@" | grep "${OPTIONS[3]:2}")
IS_NOT_ALL="${IS_BACK}${IS_FRONT}"
IS_PROD=$(echo "$@" | grep "${OPTIONS[1]:2}")

source "$APP_DIR/.env"
source "$APP_DIR/scripts/functions.sh"

mkdir -p "$LOG_DIR"

case $1 in
  # Initialization Process
  "${PROCESS[0]}" )
    print_process "Initializing Application"

    # set Execution Mode
    if [ "$IS_PROD" = "" ]; then
      # Development Mode
      print_msg_level "INFO"
      mode=$(print_with_style "Development" "CYAN")
    else
      # Production Mode
      print_msg_level "INFO"
      mode=$(print_with_style "Production" "CYAN")
    fi

    if [ "$IS_BACK" != "" ] && [ "$IS_FRONT" = "" ]; then
      side=$(print_with_style " Backend" "CYAN")
    elif [ "$IS_BACK" = "" ] && [ "$IS_FRONT" != "" ]; then
      side=$(print_with_style " Frontend" "CYAN")
    else
      :
    fi
    print_n_with_style "Initializing$side Application in $mode Mode."

    # Initialize the backend
    if [ "$IS_BACK" != "" ] || [ "$IS_NOT_ALL" = "" ]; then
      check_python_version
      cd "$APP_DIR/backend" || exit

      # install dependencies of backend
      if [ -f pyproject.toml ]; then
        process="
          poetry config virtualenvs.in-project true;
          poetry install --no-root >> $LOG_FILE"
        run_process "Installing all dependencies of backend" "$process"
      else
        print_msg_level "FATAL"
        file=$(print_with_style "pyproject.toml" "MAGENTA")
        print_n_with_style "Cannot find file $file."
        exit 1
      fi

      source .venv/bin/activate
      cd .. || exit

      process="pre-commit install >> $LOG_FILE"
      run_process "Installing pre-commit hooks" "$process"
    fi

    # Initialize the frontend
    if [ "$IS_FRONT" != "" ] || [ "$IS_NOT_ALL" = "" ]; then
      cd "$APP_DIR/frontend" || exit
      # install dependencies of frontend
      process="yarn >> $LOG_FILE"
      run_process "Installing all dependencies of frontend" "$process"
    fi

    exit 0
    ;;

  # Unit Test Process
  "${PROCESS[2]}" )
    print_process "Testing Application"

    rst=0

    # test backend
    if [ "$IS_BACK" != "" ] || [ "$IS_NOT_ALL" = "" ]; then
      cd "$APP_DIR/backend" || exit

      source .venv/bin/activate

      # run unit test
      process="coverage run --source=. -m pytest >> $LOG_FILE"
      run_process "Running unit tests for backend" "$process"
      if [ $rst -ne $? ]; then rst=1; fi
      detail_str="See flowing log file for more details.\n"
      detail_str="${detail_str}file://$LOG_FILE"
      print_details "$detail_str"

      # run coverage
      process="coverage report --show-missing"
      run_process "Checking coverage of tests for backend" "$process" "$LOG_FILE"
      if [ $rst -ne $? ]; then rst=1; fi

      # create coverage report
      process="coverage html --title '${APP_NAME} API' >> $LOG_FILE"
      run_process "Generating Code Coverage HTML Report for backend" "$process"
      if [ $rst -ne $? ]; then rst=1; fi
      detail_str="See flowing file to review the code coverage HTML report.\n"
      detail_str="${detail_str}file://$APP_DIR/backend/htmlcov/index.html"
      print_details "$detail_str"
    fi

    # test frontend
    if [ "$IS_FRONT" != "" ] || [ "$IS_NOT_ALL" = "" ]; then
      cd "$APP_DIR/frontend" || exit

      # run unit test
      process="yarn coverage 2>&1"
      run_process "Running unit tests and coverage for frontend" "$process" "$LOG_FILE" "|"
      if [ $rst -ne $? ]; then rst=1; fi
      detail_str="See flowing file to review the code coverage HTML report.\n"
      detail_str="${detail_str}file://$APP_DIR/frontend/coverage/index.html"
      print_details "$detail_str"
    fi

    exit $rst
    ;;

  # Options is not specified
  * )
    print_msg_level "FATAL"
    print_n_with_style "Missing necessary command line arguments." "MAGENTA"
    exit 1
    ;;

esac
