import os
from datetime import datetime, timezone

import discord
from discord.ext import commands

from datetime import datetime
from zoneinfo import ZoneInfo

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
    now = datetime.now()

    last_update = now.strftime("%d/%m/%Y à %H:%M")

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
        color=color
    )

    embed.add_field(
        name="Dernière actualisation",
        value=last_update,
        inline=False
    )

    embed.set_footer(text="Clique sur 🔄 Actualiser pour mettre à jour la liste.")

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


@bot.command(name="release")
async def release(ctx):
    paris = ZoneInfo("Europe/Paris")
    release_date = datetime(2026, 11, 5, 0, 0, tzinfo=paris)
    now = datetime.now(paris)

    remaining = release_date - now

    if remaining.total_seconds() <= 0:
        await ctx.send(
            "🎉 **WoW Forever est officiellement disponible !**\n"
            "La sortie officielle était prévue le 5 novembre 2026 à 00:00, heure de Paris."
        )
        return

    total_seconds = int(remaining.total_seconds())

    days, remainder = divmod(total_seconds, 86_400)
    hours, remainder = divmod(remainder, 3_600)
    minutes, _ = divmod(remainder, 60)

    embed = discord.Embed(
        title="⏳ Sortie officielle de WoW Forever",
        description=(
            f"Il reste **{days} jour(s), {hours} heure(s) et {minutes} minute(s)** "
            f"avant la sortie officielle."
        ),
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Date de sortie",
        value="5 novembre 2026 à 00:00 (heure de Paris)",
        inline=False
    )

    embed.set_footer(
        text="Le compte à rebours est calculé au moment de la commande."
    )

    await ctx.send(embed=embed)

@bot.command(name="beta")
async def beta(ctx):
    paris = ZoneInfo("Europe/Paris")

    # Blizzard indique le 21 octobre comme dernier jour complet de test.
    # L'heure exacte de fermeture n'étant pas officiellement précisée,
    # le compte à rebours va jusqu'à 23:59 heure de Paris.
    beta_end = datetime(2026, 10, 21, 23, 59, tzinfo=paris)
    now = datetime.now(paris)

    remaining = beta_end - now

    if remaining.total_seconds() <= 0:
        embed = discord.Embed(
            title="🏁 Fin de la bêta WoW Forever",
            description=(
                "La période de bêta est terminée.\n\n"
                "La sortie officielle de WoW Forever est prévue "
                "le **5 novembre 2026 à 00:00**, heure de Paris."
            ),
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)
        return

    total_seconds = int(remaining.total_seconds())

    days, remainder = divmod(total_seconds, 86_400)
    hours, remainder = divmod(remainder, 3_600)
    minutes, _ = divmod(remainder, 60)

    embed = discord.Embed(
        title="🧪 Fin de la bêta WoW Forever",
        description=(
            f"Il reste **{days} jour(s), {hours} heure(s) et {minutes} minute(s)** "
            f"avant la fin estimée de la bêta."
        ),
        color=discord.Color.purple()
    )

    embed.add_field(
        name="Fin annoncée par Blizzard",
        value="21 octobre 2026 — dernier jour complet de test",
        inline=False
    )

    embed.add_field(
        name="Référence du compte à rebours",
        value="21 octobre 2026 à 23:59 (heure de Paris)",
        inline=False
    )

    embed.set_footer(
        text="L'heure exacte de fermeture n'a pas été précisée publiquement."
    )

    await ctx.send(embed=embed)

TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
