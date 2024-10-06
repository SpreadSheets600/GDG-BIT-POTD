import discord
import sqlite3
from discord.ext import commands


class Users(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def init_main_database(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY)")
        conn.commit()
        conn.close()

    def init_profiles_database(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Profiles (user_id INTEGER PRIMARY KEY, leetcode_id TEXT, gfg_id TEXT, cf_id TEXT)"
        )
        conn.commit()
        conn.close()

    @commands.slash_command(
        name="register", description="Register Yourself In The Database"
    )
    async def register(self, ctx: commands.Context):
        self.init_database()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (user_id) VALUES (?)", (ctx.author.id,))
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="Registration Successfull",
            description="You Have Been Successfully Registered Into The Database",
            color=0xFF0000,
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="register_leetcode_id", description="Add Your LeetCode ID To The Database"
    )
    async def add_leetcode_id(self, ctx: discord.ApplicationContext, leetcode_id: str):
        self.init_database()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Users SET leetcode_id = ? WHERE user_id = ?",
            (leetcode_id, ctx.author.id),
        )
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="LeetCode ID Added",
            description="Your LeetCode ID Has Been Successfully Added To The Database",
            color=0xFF0000,
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="register_gfg_id", description="Add Your GeeksForGeeks ID To The Database"
    )
    async def add_gfg_id(self, ctx: discord.ApplicationContext, gfg_id: str):
        self.init_database()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Users SET gfg_id = ? WHERE user_id = ?",
            (gfg_id, ctx.author.id),
        )
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="GeeksForGeeks ID Added",
            description="Your GeeksForGeeks ID Has Been Successfully Added To The Database",
            color=0xFF0000,
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="register_cf_id", description="Add Your CodeForces ID To The Database"
    )
    async def add_cf_id(self, ctx: discord.ApplicationContext, cf_id: str):
        self.init_database()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Users SET cf_id = ? WHERE user_id = ?",
            (cf_id, ctx.author.id),
        )
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="CodeForces ID Added",
            description="Your CodeForces ID Has Been Successfully Added To The Database",
            color=0xFF0000,
        )
        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.init_main_database()
            self.init_profiles_database()
        except Exception as e:
            print(f"Failed To Initialize Database\n{e}")


def setup(bot: commands.Bot):
    bot.add_cog(Users(bot))
