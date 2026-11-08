#!/usr/bin/env python3
"""Apply API moves that are not covered by the Yarn -> Mojang mapping migration."""
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "build/26.3-remapped/main"
CLIENT = ROOT / "build/26.3-remapped/client"
GENERATED = ROOT / "build/26.3-generated-resources"

for folder in (MAIN, CLIENT):
    for path in folder.rglob("*.java"):
        s = path.read_text(encoding="utf-8")
        s = s.replace(".getWorld()", ".level()")
        s = s.replace(".displayClientMessage(", ".sendSystemMessage(")
        s = s.replace(".velocityModified", ".needsSync")
        s = s.replace(".hasPermissionLevel(", ".hasPermission(")
        s = s.replace("net.minecraft.world.entity.monster.EnderMan", "net.minecraft.world.entity.monster.Enderman")
        s = s.replace("net.minecraft.world.entity.monster.Slime;", "net.minecraft.world.entity.monster.cubemob.Slime;")
        for receiver in ("player", "target", "attacker", "mob", "entity", "projectile", "pushed", "livingTarget", "golem", "horse", "passenger", "user", "other", "serverPlayer", "first", "second"):
            s = re.sub(rf"\b{receiver}\.getPos\(\)", f"{receiver}.position()", s)
        s = s.replace("player.getServer()", "player.level().getServer()")
        s = s.replace("serverPlayer.getServer()", "serverPlayer.level().getServer()")
        if re.search(r"\.drop\([^\n,]+,\s*false,\s*true\)", s):
            s = re.sub(r"\.drop\(([^\n,]+),\s*false,\s*true\)", r".drop(\1, false, Prediction.SERVER_ONLY)", s)
            if "import net.minecraft.util.Prediction;" not in s:
                s = s.replace("\nimport ", "\nimport net.minecraft.util.Prediction;\nimport ", 1)
        path.write_text(s, encoding="utf-8")

for rel in (
    "com/kingdomcomecombat/game/ModGameRules.java",
    "com/kingdomcomecombat/recipe/CombatManualRecipe.java",
    "com/kingdomcomecombat/recipe/ModRecipes.java",
):
    p = MAIN / rel
    if p.exists():
        p.unlink()

items = next(MAIN.rglob("ModItems.java"))
s = items.read_text(encoding="utf-8")
s = s.replace("import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;\n", "")
s = re.sub(r"^import .*\b(?:ItemGroups|CreativeModeTabs);\n", "", s, flags=re.M)
for imp in (
    "import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;",
    "import net.minecraft.core.Registry;",
    "import net.minecraft.core.registries.BuiltInRegistries;",
    "import net.minecraft.network.chat.Component;",
    "import net.minecraft.resources.ResourceKey;",
    "import net.minecraft.world.item.CreativeModeTab;",
):
    if imp not in s:
        s = s.replace("\nimport ", "\n" + imp + "\nimport ", 1)
pattern = r"ItemGroupEvents\.modifyEntriesEvent\((?:ItemGroups|CreativeModeTabs)\.COMBAT\)\.register\(entries -> \{"
new = """ResourceKey<CreativeModeTab> tabKey = ResourceKey.create(
                BuiltInRegistries.CREATIVE_MODE_TAB.key(),
                Identifier.fromNamespaceAndPath(KingdomComeCombat.MOD_ID, "combat")
        );
        CreativeModeTab tab = FabricCreativeModeTab.builder()
                .icon(() -> new ItemStack(IRON_LONGSWORD))
                .title(Component.literal("Kingdom Come Combat"))
                .displayItems((params, entries) -> {"""
s, count = re.subn(pattern, lambda _: new, s, count=1)
if count != 1:
    raise SystemExit("Legacy ItemGroupEvents registration not found in mapped ModItems.java")
s = s.replace("entries.add(", "entries.accept(")
old_end = "        });\n    }\n\n    private static ItemStack skillBookStack"
new_end = "        }).build();\n        Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, tabKey, tab);\n    }\n\n    private static ItemStack skillBookStack"
if old_end not in s:
    raise SystemExit("End of ModItems creative-tab block not found")
items.write_text(s.replace(old_end, new_end, 1), encoding="utf-8")

trade_java = next(MAIN.rglob("SkillBookAcquisition.java"))
s = trade_java.read_text(encoding="utf-8")
s = re.sub(r"^import net\.fabricmc\.fabric\.api\.object\.builder\.v1\.trade\.TradeOfferHelper;\n", "", s, flags=re.M)
s = s.replace("        registerTrades();\n", "")
marker = "    private static void registerTrades() {"
if marker in s:
    start = s.index(marker)
    brace = s.index("{", start)
    depth = 0
    for end in range(brace, len(s)):
        depth += (s[end] == "{") - (s[end] == "}")
        if depth == 0:
            end += 1
            break
    s = s[:start] + s[end:]
trade_java.write_text(s, encoding="utf-8")

if GENERATED.exists():
    shutil.rmtree(GENERATED)
skill_dir = ROOT / "src/main/resources/data/kingdom_come_combat/kingdom_come_combat/skill_books"
passive_file = ROOT / "src/main/resources/data/kingdom_come_combat/kingdom_come_combat/passive_skills/default.json"
passive = json.loads(passive_file.read_text(encoding="utf-8"))
passive_ids = {k for k, v in passive.get("skills", {}).items() if v.get("source") == "book"}
books = []
for path in sorted(skill_dir.glob("*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    books.append(data.get("id", path.stem))

for level, cost in ((2, 14), (4, 22), (5, 32)):
    values = []
    for book_id in books:
        custom = {"book_id": book_id}
        custom["passive_id" if book_id in passive_ids else "combo_id"] = book_id
        values.append(f"kingdom_come_combat:librarian/{level}/{book_id}")
        offer = {
            "wants": {"id": "minecraft:emerald", "count": cost},
            "gives": {"id": "kingdom_come_combat:skill_book", "count": 1,
                      "components": {"minecraft:custom_data": custom}},
            "max_uses": 3,
            "reputation_discount": 0.08,
            "xp": level * 5,
        }
        out = GENERATED / f"data/kingdom_come_combat/villager_trade/librarian/{level}/{book_id}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(offer, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tag = GENERATED / f"data/minecraft/tags/villager_trade/librarian/level_{level}.json"
    tag.parent.mkdir(parents=True, exist_ok=True)
    tag.write_text(json.dumps({"replace": False, "values": values}, indent=2) + "\n", encoding="utf-8")

print(f"Applied 26.3 source/API patches; generated librarian trade data for {len(books)} books.")
