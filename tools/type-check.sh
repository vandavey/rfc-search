#!/bin/bash
#
#  type-check.sh
#  -------------
#  Performs static type checking with mypy to detect any potential
#  issues in the specified source code files and directories.
#

# Write an error message to stderr and exit
error() {
    echo "Usage: type-check.sh [PATHS]"
    echo -e "\033[91m[x]\033[0m ${@}" > /dev/stderr
    exit 1
}

ARGS=""
EXE_PATH=$(which mypy)

# Failed to locate the mypy executable file
[ ! -x $EXE_PATH ] && error "Failed to locate executable file: 'mypy'"

# Add the standard command-line arguments
[ $# -gt 0 ] && ARGS+="${@}"

# Add all available pipeline input arguments
[ -p /dev/stdin ] && ARGS+=" $(cat /dev/stdin)"

# The script requires one or more arguments
[[ -z $ARGS ]] && error "One or more argument musty be specified"

# Format the command-line arguments as an array
ARGS="$(echo $ARGS | tr ' ' '\n')"

# Validate the input file paths
for ARG in $ARGS; do
    [ ! -e $ARG ] && error "Invalid file path: '${ARG}'"
done

MYPY_OPTS=(
    "--strict"
    "--warn-incomplete-stub"
    "--warn-redundant-casts"
    "--warn-return-any"
    "--warn-unreachable"
    "--warn-unused-ignores"
)

# Perform static type checking with mypy
$EXE_PATH $ARGS ${MYPY_OPTS[@]}
