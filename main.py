import os
from datetime import datetime, timezone

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


def get_wow_players(guild: discord.Guild) -> list[str]:
    players = []

    for member in guild.members:
        if member.bot:
            continue

        for activity in member.activities:
            activity_name = getattr(activity, "name", None)

            if not activity_name:
                continue

            activity_name = activity_name.strip()

            if "world of warcraft" in activity_name.lower():
                players.append(
                    f"• **{member.display_name}** — {activity_name}"
                )
                break

    return sorted(players, key=str.lower)


def build_wow_embed(guild: discord.Guild) -> discord.Embed:
    players = get_wow_players(guild)
    now = datetime.now(timezone.utc)

    if players:
        description = "\n".join(players)
        color = discord.Color.green()
        title = f"🟢 Joueurs WoW en ligne — {len(players)}"
    else:
        description = (
            "Aucun membre n'est actuellement détecté sur World of Warcraft.\n\n"
            "Les membres doivent partager leur activité Discord pour apparaître ici."
        )
        color = discord.Color.orange()
        title = "🟠 Joueurs WoW en ligne — 0"

    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=now
    )

    embed.set_footer(text="Clique sur Actualiser pour mettre à jour la liste.")
    return embed


class WowOnlineView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=900)

    @discord.ui.button(
        label="Actualiser",
        emoji="🔄",
        style=discord.ButtonStyle.primary
    )
    async def refresh(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if interaction.guild is None:
            await interaction.response.send_message(
                "Cette action doit être utilisée dans un serveur Discord.",
                ephemeral=True
            )
            return

        button.disabled = True

        await interaction.response.edit_message(
            embed=build_wow_embed(interaction.guild),
            view=self
        )

        button.disabled = False

        await interaction.message.edit(view=self)


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} ({bot.user.id})")


@bot.command(name="ig")
async def in_game(ctx):
    if ctx.guild is None:
        await ctx.send(
            "Cette commande doit être utilisée dans un serveur Discord."
        )
        return

    await ctx.send(
        embed=build_wow_embed(ctx.guild),
        view=WowOnlineView()
    )


@in_game.error
async def in_game_error(ctx, error):
    print(f"Erreur avec !ig : {error}")

    await ctx.send(
        "Une erreur s'est produite pendant la recherche des joueurs WoW."
    )


TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
