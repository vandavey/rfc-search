#!/bin/bash
#
#  type-check.sh
#  -------------
#  Performs static type checking with mypy to detect any potential
#  issues in the specified source code files and directories.
#

# Write an error message to stderr and exit
error() {
    echo "Usage: type-check.sh PATHS"
    echo -e "\033[91m[x]\033[0m ${*}" > /dev/stderr
    exit 1
}

if [[ $PWD != *"rfc-search/tools"* ]]; then
    error "Script must be executed in directory '/rfc-search/tools'"
fi

ARGS=""
EXE_PATH=$(which mypy)

# Failed to locate the mypy executable file
if [ ! -x "${EXE_PATH}" ]; then
    error "Failed to locate executable file: 'mypy'"
fi

# Add the standard command-line arguments
if [ $# -gt 0 ]; then
    ARGS+="${*}"
fi

# Add all available pipeline input arguments
if [ -p /dev/stdin ]; then
    ARGS+=" $(cat /dev/stdin)"
fi

# The script requires one or more arguments
if  [[ -z $ARGS ]] && [ ! -f "mypy.ini" ]; then
    error "One or more argument musty be specified"
fi

# Format the command-line arguments as an array
ARGS="$(echo "${ARGS}" | tr ' ' '\n')"

# Validate the input file paths
for ARG in $ARGS; do
    if [ ! -e "${ARG}" ]; then
        error "Invalid file path: '${ARG}'"
    fi
done

MYPY_OPTS=()

# Use default mypy options if no config file exists
if [ ! -f "mypy.ini" ]; then
    MYPY_OPTS+=(
        "--no-implicit-optional"
        "--strict"
        "--warn-incomplete-stub"
        "--warn-no-return"
        "--warn-redundant-casts"
        "--warn-return-any"
        "--warn-unreachable"
        "--warn-unused-ignores"
    )
fi

# Perform static type checking with mypy
$EXE_PATH "${ARGS[@]}" "${MYPY_OPTS[@]}"
