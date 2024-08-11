##############################
# Define Functions.
##############################

SCREEN_WIDTH=88
FIRST_CHAR_NUM=7

# Get color code of printf.
# $1 - text of foreground color
# $2 - text of background color
# Return - color code
function get_color_code {
  COLOR_CODE=("BLACK" "RED" "GREEN" "YELLOW" "BLUE" "MAGENTA" "CYAN" "WHITE" "EXT" "DEF")

  for i in "${!COLOR_CODE[@]}"; do
    if [[ "${COLOR_CODE[$i]}" = "$1" ]]; then
      code="${i}"
   fi
  done

  if [ -z "$code" ]; then
    code="9"
  fi

  if [[ $2 -eq 1 ]]; then
    code="4${code}"
  else
    code="3${code}"
  fi

  echo "$code"
}

# Formatted output.
# $1 - text
# $2 - text of foreground color
# $3 - text of background color
# $4 - bold text flag
function print_with_style {
  fg_color=$(get_color_code "$2")
  bg_color=$(get_color_code "$3" 1)

  if [[ $4 -eq 1 ]]; then
    style="1"
  else
    style="0"
  fi

  printf "\033[%s;%s;%sm%b\033[m" "$style" "$fg_color" "$bg_color" "$1"
}

# Output with \n for print_with_style function.
# $1 - text
# $2 - text of foreground color
# $3 - text of background color
# $4 - bold text flag
function print_n_with_style {
  print_with_style "$1" "$2" "$3" "$4"
  printf "\n"
}

# Output the message and return the number of words in message．
# $1 - message
# $2 - text of foreground color
# $3 - text of background color
# $4 - bold text flag
# Return - the number of words in message
function print_count {
  print_with_style "$1" "$2" "$3" "$4"
  return ${#1}
}

# Output the message level label.
# $1 - message level text
function print_msg_level {
  case $1 in
    "FATAL" )
      print_with_style "[FATAL]" "BLACK" "MAGENTA" 1
      ;;
    "ERROR" )
      print_with_style "[ERROR]" "YELLOW" "RED" 1
      ;;
    "WARN" )
      print_with_style "[ WARN]" "BLACK" "YELLOW" 1
      ;;
    * )
      print_with_style "[ INFO]" "BLUE" "WHITE" 1
      ;;
  esac

  printf " "
}

# Output result of the process
# $1 - process name
# $2 - process result
# Return - process result
function print_result {
  DOING_CODE="."
  RST_LIST=("Success" "Failed!")
  step_count=$(count_str "$1 ")

  if [ "$2" -eq 0 ]; then
    result_msg=${RST_LIST[0]}
    rst_format=$(print_with_style "$result_msg" "GREEN")
  else
    result_msg=${RST_LIST[1]}
    rst_format=$(print_with_style "$result_msg" "RED")
  fi

  rst_num=$(count_str "$result_msg")
  doing_char_num=$((SCREEN_WIDTH - FIRST_CHAR_NUM - rst_num - step_count - 2))
  doing=$(get_fix_width_str "$DOING_CODE" $doing_char_num)
  print_n_with_style " $doing $rst_format" "WHITE"

  return "$2"
}

# Output details.
# $1 - detailed information
function print_details {
  str="${1//$'\n'/$'\n\t'}"
  str="${str//\\n/\n\t}"
  print_n_with_style "\t$str" "WHITE"
}

# Get a fixed-width string.
# $1 - character
# $2 - width of string
function get_fix_width_str {
  printf -- "${1}%0.s" $(seq 0 $(($2 - 1)))
}

# Get the length of a string.
# $1 - text
# Return - number of words in the text
function count_str {
  echo ${#1}
}

# Output the title of process.
# $1 - process name
function print_process {
  SECTION_HR_CODE="="
  title=" $1 "
  title_count=$(count_str "$title")
  end_char_num=$((SCREEN_WIDTH - FIRST_CHAR_NUM - title_count))
  section_start=$(get_fix_width_str "$SECTION_HR_CODE" $FIRST_CHAR_NUM)
  section_end=$(get_fix_width_str "$SECTION_HR_CODE" $end_char_num)
  print_n_with_style "$section_start$title$section_end" "BLUE"
}

# Check Python version.
function check_python_version {
  # get Python version.
  PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
  # get major version and minor version.
  MAJOR_VERSION=$(echo "$PYTHON_VERSION" | cut -d. -f1)
  MINOR_VERSION=$(echo "$PYTHON_VERSION" | cut -d. -f2)

  # check version
  if [[ $MAJOR_VERSION -eq 3 && $MINOR_VERSION -ge 11 ]]; then
    version=$(print_with_style "$PYTHON_VERSION" "CYAN")
    print_msg_level "INFO"
    print_n_with_style "Your Python version is $version."
  else
    version=$(print_with_style "$PYTHON_VERSION" "MAGENTA")
    proper_version=$(print_with_style "3.11" "YELLOW")
    print_msg_level "FATAL"
    print_with_style "Your Python version is $version. "
    print_n_with_style "Please use version $proper_version or higher."
    exit 1
  fi

}

# Executes the specified commands.
# $1 - process name
# $2 - commands text
# $3 - detailed information output to
# $4 - string to filter detailed information
# Return - process result
function run_process {
  print_msg_level "INFO"
  print_count "$1"
  detail_str=$(eval "$2")
  rst=$?
  print_result "$1" $rst
  if [ "$detail_str" != "" ]; then
    if [ "$4" != "" ]; then
      refine_str=$(echo "$detail_str" | grep "|")
      print_details "$refine_str"
    else
      print_details  "$detail_str"
    fi
    if [ "$3" != "" ]; then
      echo "$detail_str" >> "$3"
    fi
  fi

  return "$rst"
}
