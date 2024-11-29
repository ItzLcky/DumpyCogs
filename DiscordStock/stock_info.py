from redbot.core import commands, Config
import requests
import yfinance as yf


class StockInfo(commands.Cog):
    """Stock Market Information Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)
        # Add any default configurations if necessary.

    @commands.command(name="stockprice")
    async def stock_price(self, ctx, symbol: str):
        """Get the current price of a stock."""
        try:
            # Fetch stock data using yfinance
            stock = yf.Ticker(symbol)
            stock_info = stock.info
            price = stock_info.get("regularMarketPrice")
            if price is None:
                await ctx.send(f"Could not retrieve price for symbol: {symbol}")
                return
            await ctx.send(f"The current price of {symbol} is ${price:.2f}")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="stocksummary")
    async def stock_summary(self, ctx, symbol: str):
        """Get a quick summary of a stock."""
        try:
            # Fetch stock data using yfinance
            stock = yf.Ticker(symbol)
            stock_info = stock.info
            name = stock_info.get("longName", "Unknown Company")
            price = stock_info.get("regularMarketPrice", "N/A")
            sector = stock_info.get("sector", "N/A")
            summary = stock_info.get("longBusinessSummary", "N/A")

            message = (
                f"**{name} ({symbol.upper()})**\n"
                f"Price: ${price}\n"
                f"Sector: {sector}\n"
                f"Summary: {summary[:500]}..."  # Limit the length
            )
            await ctx.send(message)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="setapikey")
    async def set_api_key(self, ctx, api_key: str):
        """Set API key for external stock market data sources."""
        await self.config.api_key.set(api_key)
        await ctx.send("API key has been set.")


# Entry point for the cog
def setup(bot):
    bot.add_cog(StockInfo(bot))
