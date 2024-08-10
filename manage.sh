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

source "$APP_DIR/.env"
source "$APP_DIR/scripts/functions.sh"

mkdir -p "$LOG_DIR"

case $1 in
  # Initialization Process
  "${PROCESS[0]}" )
    print_process "Initializing Application"

    # validate options
    if [ "$2" = "${OPTIONS[0]}" ] || [ "$2" = "" ]; then
      if [ "$3" != "" ]; then
        print_msg_level "WARN"
        option=$(print_with_style "$3" "YELLOW")
        print_n_with_style "You don't need to specify Option $option."
      else
        print_msg_level "INFO"
        mode=$(print_with_style "Development" "CYAN")
        print_n_with_style "Initializing Application in $mode Mode."
      fi
    elif [ "$2" = "${OPTIONS[1]}" ]; then
      if [ "$3" = "${OPTIONS[2]}" ] || [ "$3" = "" ]; then
        app=$(print_with_style "Backend" "CYAN")
      elif [ "$3" = "${OPTIONS[3]}" ]; then
        app=$(print_with_style "Frontend" "CYAN")
      else
        print_msg_level "FATAL"
        option=$(print_with_style "$3" "MAGENTA")
        print_n_with_style "Unknown Option $option!"
        exit 1
      fi
      mode=$(print_with_style "Production" "CYAN")
      print_msg_level "INFO"
      print_n_with_style "Initializing $app Application in $mode Mode."
    else
      print_msg_level "FATAL"
      option=$(print_with_style "$2" "MAGENTA")
      print_n_with_style "Unknown Option $option!"
      exit 1
    fi

    # Initialize the backend
    if [ "$3" != "${OPTIONS[3]}" ]; then
      check_python_version
      cd "$APP_DIR/backend" || exit

      # install dependencies
      if [ -f pyproject.toml ]; then
        process="
          poetry config virtualenvs.in-project true;
          poetry install --no-root >> $LOG_FILE"
        run_process "Installing all dependencies" "$process"
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
    if [ "$2" = "${OPTIONS[0]}" ] || [ "$2" = "" ] || [ "$3" = "${OPTIONS[3]}" ]; then
      echo ""
    fi

    exit 0
    ;;

  # Unit Test Process
  "${PROCESS[2]}" )
    print_process "Testing Application"

    rst=0

    # test of backend
    if [ "$2" = "${OPTIONS[2]}" ] || [ "$2" = "" ]; then
      cd "$APP_DIR/backend" || exit

      # run unit test
      process="coverage run --source=. -m pytest >> $LOG_FILE"
      run_process "Running unit tests for backend" "$process"
      if [ $rst -ne $? ]; then rst=1; fi
      detail_str="See flowing log file for more details.\n"
      detail_str="${detail_str}file://$LOG_FILE"
      print_details "$detail_str"

      # run coverage
      process="coverage report --show-missing"
      run_process "Checking coverage of tests" "$process" "$LOG_FILE"
      if [ $rst -ne $? ]; then rst=1; fi

      # create coverage report
      process="coverage html --title ${APP_NAME}API >> $LOG_FILE"
      run_process "Generating Code Coverage HTML Report" "$process"
      if [ $rst -ne $? ]; then rst=1; fi
      detail_str="See flowing file to review the code coverage HTML report.\n"
      detail_str="${detail_str}file://$APP_DIR/backend/htmlcov/index.html"
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
