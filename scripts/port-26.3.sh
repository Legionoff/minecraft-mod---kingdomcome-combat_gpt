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

./gradlew -p versions/migration migrateMappings \
  --mappings "net.minecraft:mappings:1.21.11" \
  --input "../../src/main/java" \
  --output "../../build/26.3-remapped/main"

# Loom 1.17.21 exposes the general migration task in this setup; reuse it
# with the client source folder as input to migrate the split client source set.
./gradlew -p versions/migration migrateMappings \
  --mappings "net.minecraft:mappings:1.21.11" \
  --input "../../src/client/java" \
  --output "../../build/26.3-remapped/client"

./gradlew -p versions/26.3 clean build --stacktrace

echo "Build finished. Check versions/26.3/build/libs/ for the mod JAR."
