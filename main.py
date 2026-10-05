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


@bot.command(name="ig")
async def in_game(ctx):
    if ctx.guild is None:
        await ctx.send("Cette commande doit être utilisée dans un serveur Discord.")
        return

    wow_players = []

    for member in ctx.guild.members:
        if member.bot:
            continue

        for activity in member.activities:
            if isinstance(activity, discord.Game) and activity.name:
                game_name = activity.name.strip()

                if "world of warcraft" in game_name.lower():
                    wow_players.append(
                        f"• {member.display_name} — {game_name}"
                    )
                    break

    if not wow_players:
        await ctx.send(
            "Aucun membre n'est actuellement détecté sur World of Warcraft."
        )
        return

    message = (
        "**Membres actuellement détectés sur WoW :**\n"
        + "\n".join(wow_players)
    )

    await ctx.send(message)


TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
