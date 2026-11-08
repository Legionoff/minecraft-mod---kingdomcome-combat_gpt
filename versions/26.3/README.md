# Minecraft 26.3 port target

The original 1.21.x Yarn sources remain untouched. The port process uses Fabric
Loom's `migrateMappings` and `migrateClientMappings` tasks to create Mojang-mapped
source copies, then compiles the isolated 26.3 target.

## Toolchain

- Minecraft 26.3
- Java 25
- Fabric Loader 0.19.5
- Fabric Loom 1.17-SNAPSHOT
- Gradle 9.6.0
- Fabric API 0.165.2+26.3
- Cloth Config 26.3.159
- Mod Menu 21.0.0
- Player Animation Library 1.2.9+26.3 (CurseForge file 9443585)

## Build

```bash
bash scripts/port-26.3.sh
```

The same command is wired into `.github/workflows/build-26.3.yml`.

## Status

Mapping conversion is automated, but it is not a substitute for the compile-and-fix
cycle. Minecraft 26.3 changed APIs and renderer internals after 1.21.11. Compiler
diagnostics, stale Mixin selectors and runtime injection failures still need to be
fixed against the actual 26.3 game classes. Do not publish a JAR until CI succeeds
and client/server smoke tests pass.
