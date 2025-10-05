#!/usr/bin/env bash
set -e

# Extract numeric value (in milliseconds)
sync_time=$(python3 -m timeit -n 5 -r 5 -s "import runpy" \
    "runpy.run_path('factorize_sync.py')" 2>/dev/null | \
    awk -F'[: ]+' '/per loop/ {print $(NF-3)}')

thread_time=$(python3 -m timeit -n 5 -r 5 -s "import runpy" \
    "runpy.run_path('factorize_threads.py')" 2>/dev/null | \
    awk -F'[: ]+' '/per loop/ {print $(NF-3)}')

echo "Sync:    ${sync_time} msec"
echo "Threads: ${thread_time} msec"

