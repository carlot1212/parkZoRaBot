from string import Template
import discord

HARMONIES_QUESTIONS = [Template("How many tree points did $player get?"),
            Template("How many mountain points did $player get?"),
            Template("How many plains points did $player get?"),
            Template("How many building points did $player get?"),
            Template("How many river points did $player get?"),
            Template("How many habitat points did $player get?"),
            Template("How many special habitat points did $player get?"),
            ]

HARMONIES_SCORESHEET = {
    "Tree Points": 0,
    "Mountain Points": 0,
    "Plains Points": 0,
    "Building Points": 0,
    "River Points": 0,
    "Habitat Points": 0,
    "Special Habitat Points": 0,
}

async def harmonies(ctx, bot):
    thread = await ctx.message.create_thread(name="Harmonies Scoring")

    players = await get_players(bot, thread)
    player_scoring = {player: HARMONIES_SCORESHEET.copy() for player in players}
    await get_points(ctx, bot, thread, players, player_scoring)

    scoring_message = await create_scoring_message(players, player_scoring)
    await save_scores(ctx, players, scoring_message)

    await thread.delete()

async def get_players(bot, thread):
    await thread.send("Who is playing?")
    players_response = await bot.wait_for('message', timeout=300.0)
    players = [player.strip() for player in players_response.content.split(',')]
    return players

async def get_points(ctx, bot, thread, players, player_scoring):
    for (scoring, points), question in zip(HARMONIES_SCORESHEET.items(), HARMONIES_QUESTIONS):
        for player in players:
            await thread.send(question.substitute(player=player))
            response = await bot.wait_for('message', timeout=300.0)
            points = int(response.content)
            player_scoring[player][scoring] = points

async def create_scoring_message(players, player_scoring):
    scoring_message = "Final Scores:\n"
    for player in players:
        capitalized_player = player.capitalize()
        player_scoring[player]["Total Points"] = sum(player_scoring[player].values())
        for scoring in player_scoring[player].keys():
            scoring_message += f"{capitalized_player} scored {player_scoring[player][scoring]} {scoring}.\n"

    if len(players) > 1:
        total_points = {player: player_scoring[player]['Total Points'] for player in players}
        if list(total_points.values()).count(max(total_points.values())) == 1:
            scoring_message += f"{max(total_points, key=total_points.get).capitalize()} wins!"
        else:
            scoring_message += "It's a tie!"
    
    return scoring_message

async def save_scores(ctx, players, scoring_message):
    scoring_thread_name = ""
    players.sort()
    for player in players:
        player = player.capitalize()
        scoring_thread_name += f"{player}"
        scoring_thread_name += " vs " if player != players[-1] else " "
    scoring_thread_name += "scoreboard!"
    scoring_thread = discord.utils.get(ctx.channel.threads, name=scoring_thread_name)

    if not scoring_thread:
        scoring_thread = await ctx.channel.create_thread(name=scoring_thread_name)
    await scoring_thread.send(scoring_message)
