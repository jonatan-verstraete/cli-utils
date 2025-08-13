# will be imported by the index of the utils

SCRIPT_DIR="$PATH_CLI_UTILS/pod-automation"

source $SCRIPT_DIR/fn-pod-cfr.sh
source $SCRIPT_DIR/fn-pod-compress.sh


pod-thumbnail() {
    python3 "$SCRIPT_DIR/thumbnail/update-thumbnail.py" "$@"
}



