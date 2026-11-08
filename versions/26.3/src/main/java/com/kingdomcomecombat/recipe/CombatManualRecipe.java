package com.kingdomcomecombat.recipe;

import com.kingdomcomecombat.KingdomComeCombat;
import com.mojang.serialization.MapCodec;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.item.crafting.CustomRecipe;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.level.Level;

public final class CombatManualRecipe extends CustomRecipe {
    public static final CombatManualRecipe INSTANCE = new CombatManualRecipe();
    public static final MapCodec<CombatManualRecipe> CODEC = MapCodec.unit(INSTANCE);
    public static final StreamCodec<RegistryFriendlyByteBuf, CombatManualRecipe> STREAM_CODEC = StreamCodec.unit(INSTANCE);
    public static final RecipeSerializer<CombatManualRecipe> SERIALIZER = new RecipeSerializer<>(CODEC, STREAM_CODEC);

    private static final Identifier MODONOMICON_RED_ID = Identifier.fromNamespaceAndPath("modonomicon", "modonomicon_red");
    private static final Identifier MODONOMICON_BOOK_ID_COMPONENT = Identifier.fromNamespaceAndPath("modonomicon", "book_id");
    private static final Identifier COMBAT_MANUAL_ID = Identifier.fromNamespaceAndPath(KingdomComeCombat.MOD_ID, "combat_manual");

    @Override
    public boolean matches(CraftingInput input, Level level) {
        boolean foundBook = false;
        boolean foundSword = false;
        for (ItemStack stack : input.items()) {
            if (stack.isEmpty()) continue;
            if (stack.is(Items.BOOK) && !foundBook) foundBook = true;
            else if (stack.is(Items.IRON_SWORD) && !foundSword) foundSword = true;
            else return false;
        }
        return foundBook && foundSword;
    }

    @Override
    public ItemStack assemble(CraftingInput input) {
        return createManualStack();
    }

    @Override
    public RecipeSerializer<? extends CustomRecipe> getSerializer() {
        return ModRecipes.COMBAT_MANUAL;
    }

    private static ItemStack createManualStack() {
        Item item = BuiltInRegistries.ITEM.getValue(ResourceKey.create(Registries.ITEM, MODONOMICON_RED_ID));
        ItemStack stack = new ItemStack(item);
        DataComponentType<?> componentType = BuiltInRegistries.DATA_COMPONENT_TYPE.getValue(
                ResourceKey.create(Registries.DATA_COMPONENT_TYPE, MODONOMICON_BOOK_ID_COMPONENT)
        );
        setBookIdComponent(stack, componentType);
        return stack;
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static void setBookIdComponent(ItemStack stack, DataComponentType<?> componentType) {
        stack.set((DataComponentType) componentType, COMBAT_MANUAL_ID);
    }
}
