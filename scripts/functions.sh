# Define Functions.

# Outputs the string passed and returns the number of characters in the string.
function print_count() {

  printf "$1"
  num=${#1}
  return $num

}

# Outputs the process name
function print_process() {

  printf "\033[34m"
  printf -- "-%0.s" {0..2}
  print_count " $1 "
  printf -- "-%0.s" $(seq 1 $((60-$?)))
  printf "\033[m\n"

}

# Outputs message type
function print_message() {

  case $1 in

    "err" )
      printf "\033[41;33m[ ERR]\033[m "
      ;;

    "warn" )
      printf "\033[43;30m[WARN]\033[m "
      ;;

    * )
      printf "\033[47m[INFO]\033[m "
      ;;

  esac

}

# Outputs the result of processing
function print_result() {

  printf " "
  printf ".%0.s" $(seq 1 $((40-$2)))

  if [ "$1" -eq 0 ]; then
    printf "\033[32m Success \033[m\n"
  else
    printf "\033[31m Failed! \033[m\n"
  fi

}

# Check python version
function check_python_version() {

  # get python version
  PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
  # get python major version and minor version
  MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f1)
  MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f2)

  # determine the version
  if [[ $MAJOR_VERSION -eq 3 && $MINOR_VERSION -ge 11 ]]; then
    print_message
    printf "Python version is \033[34m%s\033[m.\n" "$PYTHON_VERSION"
  else
    print_message "error"
    printf "Python version is \033[31m%s\033[m," "$PYTHON_VERSION"
    printf " please use version \033[33m%s\033[m or higher.\n" "3.11"
    exit 1
  fi

}
