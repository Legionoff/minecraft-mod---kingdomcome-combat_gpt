# Minecraft 26.3 port target

The original 1.21.x Yarn sources remain untouched. The port process runs two
Fabric Loom `migrateMappings` passes (main and client folders), applies API
compatibility patches for Minecraft 26.2+, then compiles the isolated 26.3 target.

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

The same command runs in `.github/workflows/build-26.3.yml`. GitHub Actions
provides Java 25 and network access to the Gradle/Fabric/CurseMaven repositories.

## Porting notes

- The old ItemGroupEvents registration is replaced with a dedicated Fabric creative tab.
- Removed TradeOfferHelper villager offers are generated as data-driven trade definitions
  for all configured skill books at librarian levels 2, 4 and 5.
- Custom game rules use the 26.2+ GameRuleBuilder API and namespaced identifiers.
- The combat manual recipe uses the 26.2+ CustomRecipe codec/stream-codec serializer API.

This is still a compile-and-fix port, not a release claim. Stale Mixin selectors,
API signatures, and runtime injection failures must be fixed against actual 26.3
classes. Do not distribute a JAR until CI succeeds and client/server smoke tests pass.
