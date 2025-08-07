# will be imported by the index of the utils

SCRIPT_DIR="$PATH_CLI_UTILS/pod-automation"

source $SCRIPT_DIR/cfr.sh


pod-thumbnail() {
    python3 "$SCRIPT_DIR/thumbnail/update-thumbnail.py" "$@"
}
