import os
import discord
from discord.ext import commands, tasks
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready")
    update_online.start()

@bot.command()
async def ig(ctx):
    guild = ctx.guild
    wow_players = []

    for member in guild.members:
        if member.bot:
            continue

        for activity in member.activities:
            if isinstance(activity, discord.Game) and activity.name:
                game_name = activity.name.strip()

                if "world of warcraft" in game_name.lower():
                    wow_players.append(
                        f"{member.display_name} — {game_name}"
                    )
                    break

    if not wow_players:
        await ctx.send(
            "Aucun membre détecté sur World of Warcraft actuellement.\n"
            "Vérifie que les membres partagent leur activité Discord."
        )
        return

    msg = "**Membres jouant à WoW actuellement :**\n" + "\n".join(
        f"• {player}" for player in wow_players
    )
    await ctx.send(msg)

@tasks.loop(seconds=60)
async def update_online():
    # Optionnel : mettre à jour un message épinglé dans un channel dédié
    pass

@ig.error
async def wowonline_error(ctx, error):
    await ctx.send(f"Erreur: {error}")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)