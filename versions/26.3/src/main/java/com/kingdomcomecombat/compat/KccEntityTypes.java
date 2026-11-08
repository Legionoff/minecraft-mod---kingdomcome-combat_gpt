package com.kingdomcomecombat.compat;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityType;

public final class KccEntityTypes {
    public static final EntityType<?> HORSE = get("horse");
    public static final EntityType<?> CAMEL = get("camel");
    public static final EntityType<?> SKELETON = get("skeleton");
    public static final EntityType<?> STRAY = get("stray");
    public static final EntityType<?> WITHER_SKELETON = get("wither_skeleton");
    public static final EntityType<?> ZOMBIE = get("zombie");
    public static final EntityType<?> HUSK = get("husk");
    public static final EntityType<?> DROWNED = get("drowned");
    public static final EntityType<?> ZOMBIFIED_PIGLIN = get("zombified_piglin");
    public static final EntityType<?> PIGLIN = get("piglin");
    public static final EntityType<?> PIGLIN_BRUTE = get("piglin_brute");
    public static final EntityType<?> PILLAGER = get("pillager");
    public static final EntityType<?> VINDICATOR = get("vindicator");
    public static final EntityType<?> EVOKER = get("evoker");
    public static final EntityType<?> ILLUSIONER = get("illusioner");
    public static final EntityType<?> WITCH = get("witch");
    public static final EntityType<?> VILLAGER = get("villager");
    public static final EntityType<?> WANDERING_TRADER = get("wandering_trader");

    private KccEntityTypes() {}

    private static EntityType<?> get(String path) {
        ResourceKey<EntityType<?>> key = ResourceKey.create(
                Registries.ENTITY_TYPE,
                Identifier.fromNamespaceAndPath("minecraft", path)
        );
        return BuiltInRegistries.ENTITY_TYPE.getValue(key);
    }
}
