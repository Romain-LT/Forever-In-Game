import os
import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True  # nécessaire uniquement pour !wowonline

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} ({bot.user.id})")

    if not update_online.is_running():
        update_online.start()


@bot.command()
async def wowonline(ctx):
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
            "Aucun membre détecté sur World of Warcraft actuellement.\n"
            "Les joueurs doivent autoriser Discord à afficher leur activité."
        )
        return

    message = "**Joueurs WoW détectés actuellement :**\n" + "\n".join(wow_players)
    await ctx.send(message)


@tasks.loop(seconds=60)
async def update_online():
    # On ne fait rien pour le moment.
    # Cette tâche servira si tu veux maintenir un message automatique dans un channel.
    pass


TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
