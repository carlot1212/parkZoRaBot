import discord
from harmonies import HARMONIES_SCORESHEET, HARMONIES_QUESTIONS

GAME_MAPPING = {
    "Harmonies": {"scoresheet": HARMONIES_SCORESHEET, "questions": HARMONIES_QUESTIONS}
}

async def scoring(ctx, game, bot):
    thread = await ctx.message.create_thread(name=f"{game} Scoring")

    players = await get_players(bot, thread)
    player_scoring = {player: GAME_MAPPING[game]["scoresheet"].copy() for player in players}
    await get_points(game, bot, thread, players, player_scoring)

    scoring_message = await create_scoring_message(players, player_scoring)
    await save_scores(ctx, players, scoring_message)

    await thread.delete()

async def get_players(bot, thread):
    await thread.send("Who is playing?")
    players_response = await bot.wait_for('message', timeout=300.0)
    players = [player.strip() for player in players_response.content.split(',')]
    return list(filter(None, players))

async def get_points(game, bot, thread, players, player_scoring):
    for (scoring, points), question in zip(GAME_MAPPING[game]["scoresheet"].items(),
                                           GAME_MAPPING[game]["questions"]):
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
        capitalized_player = player.capitalize()
        scoring_thread_name += f"{capitalized_player}"
        scoring_thread_name += " vs " if player != players[-1] else " "
    scoring_thread_name += "scoreboard!"
    scoring_thread = discord.utils.get(ctx.channel.threads, name=scoring_thread_name)

    if not scoring_thread:
        scoring_thread = await ctx.channel.create_thread(name=scoring_thread_name)
    await scoring_thread.send(scoring_message)