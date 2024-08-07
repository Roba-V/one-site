##############################
# Define Functions.
##############################

# Outputs the string passed and returns the number of characters in the string.
function print_count() {

  printf "%s" "$1"
  num=${#1}
  return "$num"

}

# Outputs the process name
function print_process() {

  printf "\033[34m"
  printf -- "=%0.s" {0..5}
  print_count " $1 "
  printf -- "=%0.s" $(seq 1 $((60-$?)))
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
  printf "\033[37m.%0.s\033[m" $(seq 1 $((50-$2)))

  if [ "$1" -eq 0 ]; then
    printf "\033[32m Success \033[m\n"
  else
    printf "\033[31m Failed! \033[m\n"
  fi
  return "$1"

}

# Check python version
function check_python_version() {

  # get python version
  PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
  # get python major version and minor version
  MAJOR_VERSION=$(echo "$PYTHON_VERSION" | cut -d. -f1)
  MINOR_VERSION=$(echo "$PYTHON_VERSION" | cut -d. -f2)

  # determine the version
  if [[ $MAJOR_VERSION -eq 3 && $MINOR_VERSION -ge 11 ]]; then
    print_message
    printf "Python version is \033[36m%s\033[m.\n" "$PYTHON_VERSION"
  else
    print_message "err"
    printf "\033[31mPython version is\033[m"
    printf "\033[33m %s\033[m\033[31m,\033[m" "$PYTHON_VERSION"
    printf "\033[31m please use version \033[m"
    printf "\033[36m%s\033[m \033[31mor higher.\033[m\n" "3.11"
    exit 1
  fi

}
