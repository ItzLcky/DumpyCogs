import discord
import openai
import os
from discord.ext import commands

# Load your API keys from environment variables or set them directly
DISCORD_TOKEN = "your_discord_token_here"
OPENAI_API_KEY = None  # API key will be set via command

# Set up Discord bot with command prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def setapikey(ctx, key: str):
    """Set the OpenAI API key dynamically."""
    global OPENAI_API_KEY
    OPENAI_API_KEY = key
    openai.api_key = key
    await ctx.send("API key has been set successfully!")

@bot.command()
async def durstquote(ctx):
    """Fetch a Fred Durst style quote from ChatGPT."""
    if not OPENAI_API_KEY:
        await ctx.send("API key is not set. Use !setapikey <your_key> to set it.")
        return
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are ChatGPT, trained to generate quotes in the style of Fred Durst."},
                {"role": "user", "content": "Give me a classic Fred Durst quote."}
            ]
        )
        quote = response['choices'][0]['message']['content']
        await ctx.send(f'Fred Durst once said: "{quote}"')
    except Exception as e:
        await ctx.send("Oops! Something went wrong. Try again later.")
        print(f'Error: {e}')

# Run the bot
bot.run(DISCORD_TOKEN)
