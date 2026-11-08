#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! java -version 2>&1 | grep -q '25'; then
  echo "ERROR: Java 25 is required for Minecraft 26.3 and this port." >&2
  exit 2
fi

rm -rf build/26.3-remapped
mkdir -p build/26.3-remapped

# Keep original Yarn sources intact; migrate main and client source folders separately.
# Loom's task can exit successfully even when Mercury reports a type-resolution error.
migrate_sources() {
  local input="$1"
  local output="$2"
  local log_file
  log_file="$(mktemp)"
  if ! ./gradlew -p versions/migration migrateMappings \
    --mappings "net.minecraft:mappings:1.21.11" \
    --input "$input" \
    --output "$output" 2>&1 | tee "$log_file"; then
    rm -f "$log_file"
    return 1
  fi
  if grep -q "Status ERROR:" "$log_file"; then
    echo "ERROR: source mapping reported unresolved types; refusing to compile partially migrated sources." >&2
    rm -f "$log_file"
    return 1
  fi
  rm -f "$log_file"
}

migrate_sources "../../src/main/java" "../../build/26.3-remapped/main"
migrate_sources "../../src/client/java" "../../build/26.3-remapped/client"

python3 scripts/patch-26.3-mapped.py

./gradlew -p versions/26.3 clean build --stacktrace

echo "Build finished. Check versions/26.3/build/libs/ for the mod JAR."
