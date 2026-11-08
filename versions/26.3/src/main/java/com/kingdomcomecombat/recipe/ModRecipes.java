package com.kingdomcomecombat.recipe;

import com.kingdomcomecombat.KingdomComeCombat;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.crafting.RecipeSerializer;

public final class ModRecipes {
    public static final RecipeSerializer<CombatManualRecipe> COMBAT_MANUAL = CombatManualRecipe.SERIALIZER;

    private ModRecipes() {}

    public static void register() {
        Registry.register(
                BuiltInRegistries.RECIPE_SERIALIZER,
                Identifier.fromNamespaceAndPath(KingdomComeCombat.MOD_ID, "combat_manual"),
                COMBAT_MANUAL
        );
    }
}
