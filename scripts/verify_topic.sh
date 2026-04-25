#!/usr/bin/env sh

set -eu

usage() {
    echo "Usage: $0 <topic-dir> [--benchmarks] [target ...]" >&2
    exit 2
}

if [ "$#" -lt 1 ]; then
    usage
fi

topic_dir="$1"
shift

run_benchmarks=0
explicit_targets=""

while [ "$#" -gt 0 ]; do
    case "$1" in
        --benchmarks)
            run_benchmarks=1
            ;;
        --help)
            usage
            ;;
        *)
            explicit_targets="${explicit_targets}${explicit_targets:+
}$1"
            ;;
    esac
    shift
done

if [ ! -d "$topic_dir" ]; then
    echo "Topic directory not found: $topic_dir" >&2
    exit 1
fi

makefile="$topic_dir/Makefile"
if [ ! -f "$makefile" ]; then
    echo "Topic Makefile not found: $makefile" >&2
    exit 1
fi

expected_output_file="$topic_dir/inputs/expected_output.txt"

has_target() {
    grep -Eq "^$1:" "$makefile"
}

run_target() {
    target="$1"
    printf '\n[verify] %s -> %s\n' "$topic_dir" "$target"
    make -C "$topic_dir" "$target"
}

run_and_compare_target() {
    target="$1"
    actual_output_file="$2"
    printf '\n[verify] %s -> %s\n' "$topic_dir" "$target"
    make -s -C "$topic_dir" "$target" >"$actual_output_file"
    if ! diff -u "$expected_output_file" "$actual_output_file"; then
        echo "[verify] output mismatch for $target" >&2
        exit 1
    fi
}

if [ -n "$explicit_targets" ]; then
    printf '%s\n' "$explicit_targets" | while IFS= read -r target; do
        [ -n "$target" ] || continue
        run_target "$target"
    done
    exit 0
fi

smoke_targets="run_cpp
run_py
run_java
run_rs"

benchmark_targets="benchmark_long
benchmark_challenge
benchmark_long_all
benchmark_challenge_all"

found_any=0

if [ ! -f "$expected_output_file" ]; then
    echo "Expected output file not found: $expected_output_file" >&2
    exit 1
fi

verify_output_tmp=""
cleanup() {
    if [ -n "$verify_output_tmp" ] && [ -f "$verify_output_tmp" ]; then
        rm -f "$verify_output_tmp"
    fi
}
trap cleanup EXIT HUP INT TERM
verify_output_tmp="$(mktemp)"

for target in $smoke_targets; do
    [ -n "$target" ] || continue
    if has_target "$target"; then
        found_any=1
        run_and_compare_target "$target" "$verify_output_tmp"
    fi
done

if [ "$run_benchmarks" -eq 1 ]; then
    for target in $benchmark_targets; do
        [ -n "$target" ] || continue
        if has_target "$target"; then
            found_any=1
            run_target "$target"
        fi
    done
fi

if [ "$found_any" -eq 0 ]; then
    echo "No known standard targets found in $makefile" >&2
    exit 1
fi

printf '\n[verify] completed: %s\n' "$topic_dir"
