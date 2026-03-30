#!/usr/bin/env sh

set -u

allow_failure=0

while [ "$#" -gt 0 ]; do
    case "$1" in
        --allow-failure)
            allow_failure=1
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            break
            ;;
    esac
done

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <command> [args...]" >&2
    exit 2
fi

stdout_file="$(mktemp)"
stderr_file="$(mktemp)"

cleanup() {
    rm -f "$stdout_file" "$stderr_file"
}

trap cleanup EXIT HUP INT TERM

"$@" >"$stdout_file" 2>"$stderr_file" &
pid="$!"
peak_rss_kb=0
sampling_available=1

while kill -0 "$pid" 2>/dev/null; do
    ps_output="$(ps -o rss= -p "$pid" 2>/dev/null)"
    ps_status="$?"
    if [ "$ps_status" -ne 0 ]; then
        sampling_available=0
        break
    fi
    rss_value="$(printf '%s\n' "$ps_output" | awk 'NF { print $1; exit }')"
    if [ -n "${rss_value:-}" ] && [ "$rss_value" -gt "$peak_rss_kb" ]; then
        peak_rss_kb="$rss_value"
    fi
    sleep 0.01
done

status=0
wait "$pid" || status=$?

cat "$stdout_file"

if [ "$peak_rss_kb" -gt 0 ]; then
    echo "Peak RSS sampled (kB): $peak_rss_kb"
elif [ "$sampling_available" -eq 0 ]; then
    echo "Peak RSS sampled (kB): unavailable in restricted environment"
fi

if [ "$status" -ne 0 ]; then
    if grep -q 'RecursionError' "$stderr_file" || grep -q 'StackOverflowError' "$stderr_file" || grep -q 'stack overflow' "$stderr_file"; then
        echo "Run failed with exit code $status (likely recursion depth or stack limit)"
    else
        echo "Run failed with exit code $status"
        first_error_line="$(sed -n '1p' "$stderr_file")"
        if [ -n "$first_error_line" ]; then
            echo "Error: $first_error_line"
        fi
    fi
fi

if [ "$status" -ne 0 ] && [ "$allow_failure" -eq 0 ]; then
    exit "$status"
fi

exit 0
