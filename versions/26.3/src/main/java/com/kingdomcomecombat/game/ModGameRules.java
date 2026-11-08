package com.kingdomcomecombat.game;

import com.kingdomcomecombat.KingdomComeCombat;
import com.kingdomcomecombat.network.HardcoreModeSyncPayload;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.gamerule.v1.GameRuleBuilder;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.gamerules.GameRule;
import net.minecraft.world.level.gamerules.GameRuleCategory;
import net.minecraft.world.level.gamerules.GameRules;

public final class ModGameRules {
    public static final GameRule<Boolean> CLASSIC_MODE = GameRuleBuilder.forBoolean(true)
            .category(GameRuleCategory.MISC)
            .buildAndRegister(id("kcc_classic_mode"));
    public static final GameRule<Boolean> PLAYER_DIRECTIONAL_BLOCKING = GameRuleBuilder.forBoolean(true)
            .category(GameRuleCategory.MISC)
            .buildAndRegister(id("kcc_player_directional_blocking"));
    public static final GameRule<Double> COMBAT_SPEED = GameRuleBuilder.forDouble(1.0)
            .category(GameRuleCategory.MISC)
            .buildAndRegister(id("kcc_combat_speed"));
    public static final GameRule<Boolean> TRAUMA = GameRuleBuilder.forBoolean(true)
            .category(GameRuleCategory.MISC)
            .buildAndRegister(id("kcc_trauma"));
    public static final GameRule<Boolean> HARDCORE_MODE = GameRuleBuilder.forBoolean(false)
            .category(GameRuleCategory.MISC)
            .buildAndRegister(id("kcc_hardcore_mode"));

    private static MinecraftServer lastSyncedServer;
    private static boolean lastSyncedHardcoreMode;

    private ModGameRules() {}

    private static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(KingdomComeCombat.MOD_ID, path);
    }

    public static void register() {
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> syncHardcoreMode(handler.player));
        ServerTickEvents.END_SERVER_TICK.register(server -> {
            boolean current = hardcoreMode(server.getOverworld());
            if (server != lastSyncedServer || current != lastSyncedHardcoreMode) {
                lastSyncedServer = server;
                lastSyncedHardcoreMode = current;
                syncHardcoreMode(server);
            }
        });
    }

    public static void initializeForServer(MinecraftServer server) {
        if (server.isHardcore()) {
            server.getOverworld().getGameRules().set(HARDCORE_MODE, true, server);
        }
        lastSyncedServer = server;
        lastSyncedHardcoreMode = hardcoreMode(server.getOverworld());
        syncHardcoreMode(server);
    }

    public static boolean traumaEnabled(LivingEntity entity) {
        return !(entity instanceof Player) || traumaEnabled(entity.level());
    }

    public static boolean traumaEnabled(Level world) {
        return !(world instanceof ServerLevel serverLevel) || serverLevel.getGameRules().get(TRAUMA);
    }

    public static boolean hardcoreMode(ServerLevel world) {
        return world.getServer().isHardcore() || world.getGameRules().get(HARDCORE_MODE);
    }

    public static boolean hardcoreMode(GameRules rules) {
        return rules.get(HARDCORE_MODE);
    }

    public static void setHardcoreMode(GameRules rules, boolean enabled) {
        rules.set(HARDCORE_MODE, enabled, null);
    }

    private static void syncHardcoreMode(MinecraftServer server) {
        for (ServerPlayer player : server.getPlayerList().getPlayers()) {
            syncHardcoreMode(player);
        }
    }

    private static void syncHardcoreMode(ServerPlayer player) {
        ServerPlayNetworking.send(player, new HardcoreModeSyncPayload(hardcoreMode(player.level())));
    }

    public static boolean classicMode(Level world) {
        return world instanceof ServerLevel serverLevel && serverLevel.getGameRules().get(CLASSIC_MODE);
    }

    public static boolean classicMode(LivingEntity entity) {
        return entity != null && classicMode(entity.level());
    }

    public static boolean playerDirectionalBlocking(Level world) {
        return !(world instanceof ServerLevel serverLevel)
                || serverLevel.getGameRules().get(PLAYER_DIRECTIONAL_BLOCKING);
    }

    public static double combatSpeed(Level world) {
        if (!(world instanceof ServerLevel serverLevel)) return 1.0;
        double value = serverLevel.getGameRules().get(COMBAT_SPEED);
        if (!Double.isFinite(value)) return 1.0;
        return Math.max(0.05, Math.min(10.0, value));
    }

    public static double combatSpeed(LivingEntity entity) {
        return entity == null ? 1.0 : combatSpeed(entity.level());
    }

    public static double combatSpeed(ServerLevel world) {
        return combatSpeed((Level) world);
    }
}
