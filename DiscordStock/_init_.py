from .stock_info import StockInfo

async def setup(bot):
    """Setup the StockInfo cog."""
    cog = StockInfo(bot)
    await bot.add_cog(cog)
