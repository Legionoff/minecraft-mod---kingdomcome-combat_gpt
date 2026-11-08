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

def ensure_import(source: str, import_line: str) -> str:
    if import_line not in source:
        source = source.replace("\nimport ", "\n" + import_line + "\nimport ", 1)
    return source

ENTITY_TYPE_CONSTANTS = (
    "HORSE", "CAMEL", "SKELETON", "STRAY", "WITHER_SKELETON", "ZOMBIE", "HUSK",
    "DROWNED", "ZOMBIFIED_PIGLIN", "PIGLIN", "PIGLIN_BRUTE", "PILLAGER", "VINDICATOR",
    "EVOKER", "ILLUSIONER", "WITCH", "VILLAGER", "WANDERING_TRADER",
)

for folder in (MAIN, CLIENT):
    for path in folder.rglob("*.java"):
        s = path.read_text(encoding="utf-8")
        s = s.replace(".getWorld()", ".level()")
        s = s.replace(".getTime()", ".getGameTime()")
        s = s.replace(".getOverworld()", ".overworld()")
        s = s.replace(".getAdvancementLoader()", ".getAdvancements()")
        s = s.replace(".getEntityById(", ".getEntity(")
        s = s.replace(".getVelocity()", ".getDeltaMovement()")
        s = s.replace(".getLightLevel(", ".getMaxLocalRawBrightness(")
        s = re.sub(r"\.getEntitiesByClass\((\w+\.class),", r".getEntities(EntityTypeTest.forClass(\1),", s)
        if ".getEntities(EntityTypeTest.forClass(" in s:
            s = ensure_import(s, "import net.minecraft.world.level.entity.EntityTypeTest;")
        s = s.replace(".getDamageSources()", ".damageSources()")
        s = s.replace(".getOtherEntities(", ".getEntities(")
        s = s.replace(".squaredDistanceTo(", ".distanceToSqr(")
        s = s.replace(".raycast(", ".clip(")
        s = s.replace(".dotProduct(", ".dot(")
        s = s.replace(".displayClientMessage(", ".sendSystemMessage(")
        s = s.replace(".velocityModified", ".needsSync")
        s = s.replace(".hasPermissionLevel(", ".hasPermission(")
        s = s.replace(".isClient()", ".isClientSide()")
        s = re.sub(r"\.isClientSide(?!\()", ".isClientSide()", s)
        s = re.sub(r"\.isClient\b", ".isClientSide()", s)
        s = s.replace("net.minecraft.world.entity.monster.EnderMan", "net.minecraft.world.entity.monster.Enderman")
        s = s.replace("EnderMan", "Enderman")
        s = s.replace("net.minecraft.world.entity.monster.Slime;", "net.minecraft.world.entity.monster.cubemob.Slime;")
        s = s.replace("net.minecraft.server.world.ServerWorld", "net.minecraft.server.level.ServerLevel")
        s = s.replace("ServerWorld", "ServerLevel")
        s = s.replace("net.minecraft.entity.damage.DamageSource", "net.minecraft.world.damagesource.DamageSource")
        s = s.replace("net.minecraft.util.math.Vec3d", "net.minecraft.world.phys.Vec3")
        s = s.replace("Vec3d", "Vec3")
        s = s.replace("player.getServer()", "player.level().getServer()")
        s = s.replace("serverPlayer.getServer()", "serverPlayer.level().getServer()")
        s = s.replace(
            "player.level().getServer().isPvpEnabled()",
            "player.level().getServer().getGlobalGameRules().get(GameRules.PVP)"
        )
        s = s.replace(".getType().is(", ".getType().builtInRegistryHolder().is(")
        for receiver in ("this", "player", "target", "attacker", "mob", "entity", "projectile",
                         "pushed", "livingTarget", "golem", "horse", "passenger", "user",
                         "other", "serverPlayer", "first", "second"):
            s = re.sub(rf"\b{receiver}\.getPos\(\)", f"{receiver}.position()", s)
        s = re.sub(
            r"\.multiply\(([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)\)",
            r".scale(\1)",
            s
        )
        s = re.sub(
            r"\.breakBlock\(([^,\n]+),\s*([^,\n]+),\s*([^)]+)\)",
            r".destroyBlock(\1, \2, \3, Level.MAX_UPDATE_DEPTH)",
            s
        )
        if "Level.MAX_UPDATE_DEPTH" in s:
            s = ensure_import(s, "import net.minecraft.world.level.Level;")
        for constant in ENTITY_TYPE_CONSTANTS:
            s = s.replace(f"EntityType.{constant}", f"KccEntityTypes.{constant}")
        if "KccEntityTypes." in s:
            s = ensure_import(s, "import com.kingdomcomecombat.compat.KccEntityTypes;")
        if "GameRules.PVP" in s:
            s = ensure_import(s, "import net.minecraft.world.level.gamerules.GameRules;")
        if "sendParticles(ParticleTypes.DRAGON_BREATH" in s:
            s = s.replace(
                "sendParticles(ParticleTypes.DRAGON_BREATH",
                "sendParticles(PowerParticleOption.create(ParticleTypes.DRAGON_BREATH, 1.0F)"
            )
        if "PowerParticleOption.create(" in s:
            s = ensure_import(s, "import net.minecraft.core.particles.PowerParticleOption;")
        s = re.sub(r"\b(\w+)\.invulnerableTime\s*=\s*0\s*;", r"\1.setInvulnerableTime(0);", s)
        s = s.replace("sendEquipmentBreakStatus(stack.getItem(),", "sendEquipmentBreakStatus(stack,")
        s = s.replace("onEquippedItemBroken(stack.getItem(),", "onEquippedItemBroken(stack,")
        if path.name == "HandCannonItem.java":
            s = s.replace(
                'user.sendSystemMessage(Component.literal("副手需要火枪弹药"), true);',
                'if (user instanceof ServerPlayer serverPlayer) serverPlayer.sendOverlayMessage(Component.literal("副手需要火枪弹药"));'
            )
            if "serverPlayer.sendOverlayMessage" in s:
                s = ensure_import(s, "import net.minecraft.server.level.ServerPlayer;")
        if re.search(r"\.drop\([^\n,]+,\s*false,\s*true\)", s):
            s = re.sub(r"\.drop\(([^\n,]+),\s*false,\s*true\)", r".drop(\1, false, Prediction.SERVER_ONLY)", s)
            s = ensure_import(s, "import net.minecraft.util.Prediction;")
        if "DamageSource" in s:
            s = ensure_import(s, "import net.minecraft.world.damagesource.DamageSource;")
        if "ServerLevel" in s:
            s = ensure_import(s, "import net.minecraft.server.level.ServerLevel;")
        if "Vec3" in s:
            s = ensure_import(s, "import net.minecraft.world.phys.Vec3;")
        path.write_text(s, encoding="utf-8")

for commands in (next(MAIN.rglob("CombatCommands.java")), next(MAIN.rglob("CombatNetworking.java"))):
    s = commands.read_text(encoding="utf-8")
    s = re.sub(
        r"\b(\w+)\.hasPermission\(2\)",
        r"\1.permissions().hasPermission(new Permission.HasCommandLevel(PermissionLevel.GAMEMASTERS))",
        s
    )
    if "Permission.HasCommandLevel" in s:
        s = ensure_import(s, "import net.minecraft.server.permissions.Permission;")
        s = ensure_import(s, "import net.minecraft.server.permissions.PermissionLevel;")
    commands.write_text(s, encoding="utf-8")

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

recipe = {"type": "kingdom_come_combat:combat_manual"}
recipe_path = GENERATED / "data/kingdom_come_combat/recipe/combat_manual.json"
recipe_path.parent.mkdir(parents=True, exist_ok=True)
recipe_path.write_text(json.dumps(recipe, indent=2) + "\n", encoding="utf-8")

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
