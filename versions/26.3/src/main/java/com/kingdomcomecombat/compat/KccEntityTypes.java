package com.kingdomcomecombat.compat;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityType;

public final class KccEntityTypes {
    public static final EntityType<?> ARMOR_STAND = get("armor_stand");
    public static final EntityType<?> BOGGED = get("bogged");
    public static final EntityType<?> CAMEL = get("camel");
    public static final EntityType<?> CAT = get("cat");
    public static final EntityType<?> CAVE_SPIDER = get("cave_spider");
    public static final EntityType<?> CHICKEN = get("chicken");
    public static final EntityType<?> COW = get("cow");
    public static final EntityType<?> CREEPER = get("creeper");
    public static final EntityType<?> DONKEY = get("donkey");
    public static final EntityType<?> DROWNED = get("drowned");
    public static final EntityType<?> EVOKER = get("evoker");
    public static final EntityType<?> FOX = get("fox");
    public static final EntityType<?> GIANT = get("giant");
    public static final EntityType<?> GOAT = get("goat");
    public static final EntityType<?> HORSE = get("horse");
    public static final EntityType<?> HUSK = get("husk");
    public static final EntityType<?> ILLUSIONER = get("illusioner");
    public static final EntityType<?> LLAMA = get("llama");
    public static final EntityType<?> MOOSHROOM = get("mooshroom");
    public static final EntityType<?> MULE = get("mule");
    public static final EntityType<?> OCELOT = get("ocelot");
    public static final EntityType<?> PANDA = get("panda");
    public static final EntityType<?> PARROT = get("parrot");
    public static final EntityType<?> PHANTOM = get("phantom");
    public static final EntityType<?> PIG = get("pig");
    public static final EntityType<?> PIGLIN = get("piglin");
    public static final EntityType<?> PIGLIN_BRUTE = get("piglin_brute");
    public static final EntityType<?> PILLAGER = get("pillager");
    public static final EntityType<?> POLAR_BEAR = get("polar_bear");
    public static final EntityType<?> RABBIT = get("rabbit");
    public static final EntityType<?> RAVAGER = get("ravager");
    public static final EntityType<?> SHEEP = get("sheep");
    public static final EntityType<?> SKELETON = get("skeleton");
    public static final EntityType<?> SKELETON_HORSE = get("skeleton_horse");
    public static final EntityType<?> SPIDER = get("spider");
    public static final EntityType<?> STRAY = get("stray");
    public static final EntityType<?> TRADER_LLAMA = get("trader_llama");
    public static final EntityType<?> VILLAGER = get("villager");
    public static final EntityType<?> VINDICATOR = get("vindicator");
    public static final EntityType<?> WANDERING_TRADER = get("wandering_trader");
    public static final EntityType<?> WITCH = get("witch");
    public static final EntityType<?> WITHER_SKELETON = get("wither_skeleton");
    public static final EntityType<?> WOLF = get("wolf");
    public static final EntityType<?> ZOMBIE = get("zombie");
    public static final EntityType<?> ZOMBIE_HORSE = get("zombie_horse");
    public static final EntityType<?> ZOMBIE_VILLAGER = get("zombie_villager");
    public static final EntityType<?> ZOMBIFIED_PIGLIN = get("zombified_piglin");

    private KccEntityTypes() {}

    private static EntityType<?> get(String path) {
        ResourceKey<EntityType<?>> key = ResourceKey.create(
                Registries.ENTITY_TYPE,
                Identifier.fromNamespaceAndPath("minecraft", path)
        );
        return BuiltInRegistries.ENTITY_TYPE.getValue(key);
    }
}
