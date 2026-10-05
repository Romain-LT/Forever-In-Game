import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} ({bot.user.id})")

    for guild in bot.guilds:
        print(f"Serveur connecté : {guild.name} ({guild.member_count} membres)")


@bot.command(name="ig")
async def in_game(ctx):
    if ctx.guild is None:
        await ctx.send(
            "Cette commande doit être utilisée dans un serveur Discord."
        )
        return

    wow_players = []

    for member in ctx.guild.members:
        if member.bot:
            continue

        for activity in member.activities:
            activity_name = getattr(activity, "name", None)

            if not activity_name:
                continue

            activity_name = activity_name.strip()

            if "world of warcraft" in activity_name.lower():
                wow_players.append(
                    f"• {member.display_name} — {activity_name}"
                )
                break

    if not wow_players:
        await ctx.send(
            "Aucun membre détecté sur World of Warcraft actuellement.\n"
            "Vérifie que les membres partagent leur activité Discord."
        )
        return

    message = (
        "**Membres actuellement détectés sur WoW :**\n"
        + "\n".join(wow_players)
    )

    await ctx.send(message)


@in_game.error
async def in_game_error(ctx, error):
    print(f"Erreur avec !ig : {error}")

    await ctx.send(
        "Une erreur s'est produite pendant la recherche des joueurs WoW."
    )


TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
