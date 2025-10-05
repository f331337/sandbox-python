#!/usr/bin/env bash
set -e

extract_time() {
    python3 -m timeit -n 5 -r 5 -s "import runpy" "runpy.run_path('$1')" 

}

sync_time=$(extract_time "factorize_sync.py")
thread_time=$(extract_time "factorize_threads.py")

echo "Sync:    ${sync_time}"
echo "Threads: ${thread_time}"

