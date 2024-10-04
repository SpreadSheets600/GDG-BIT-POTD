import discord
import aiohttp
from discord.ext import commands
from discord import SlashCommandGroup
from datetime import datetime, timedelta, timezone


class LeetCodeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    leetcode = SlashCommandGroup(name="leetcode", description="LeetCode Commands")
    potd = leetcode.create_subgroup(name="potd", description="Problem Of The Day")

    @potd.command(name="view", description="Get The Problem Of The Day")
    async def view(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://alfa-leetcode-api.onrender.com/daily"
            ) as response:
                if response.status == 200:
                    data = await response.json()

                    next_day_utc = datetime.now(timezone.utc) + timedelta(days=1)
                    next_potd_time_utc = next_day_utc.replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )

                    timestamp = int(next_potd_time_utc.timestamp())

                    embed = discord.Embed(
                        title=data["questionTitle"],
                        url=data["questionLink"],
                        color=0xFBF2EB,
                    )

                    embed.add_field(name="Date", value=data["date"], inline=True)
                    embed.add_field(
                        name="Time Left", value=f"<t:{timestamp}:R>", inline=True
                    )
                    embed.add_field(
                        name="Difficulty", value=data["difficulty"], inline=True
                    )
                    embed.add_field(
                        name="Topic Tags",
                        value=", ".join(tag["name"] for tag in data["topicTags"]),
                        inline=False,
                    )
                    embed.set_footer(
                        text=f"Likes: {data['likes']} | Dislikes: {data['dislikes']}"
                    )

                    await ctx.followup.send(embed=embed)

                else:
                    await ctx.followup.send("API Down .... Try Again Later")

    @potd.command(name="hint", description="Get The Hint For The Problem Of The Day")
    async def hint(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://alfa-leetcode-api.onrender.com/daily"
            ) as response:
                if response.status == 200:
                    data = await response.json()

                    if "hints" in data and data["hints"]:
                        hint_message = "\n".join(data["hints"])
                    else:
                        hint_message = "No Hints Available For This Problem"

                    embed = discord.Embed(
                        title="Hint For The Problem Of The Day",
                        url=data["questionLink"],
                        description=hint_message,
                        color=0xFBF2EB,
                    )

                    await ctx.followup.send(embed=embed)

                else:
                    await ctx.followup.send("API Down .... Try Again Later")

    @leetcode.command(name="profile", description="Get The LeetCode Profile")
    async def profile(self, ctx: discord.ApplicationContext, username: str):
        await ctx.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://alfa-leetcode-api.onrender.com/{username}"
            ) as response:
                if response.status == 200:
                    if response.status == 200:
                        data = await response.json()

                        embed = discord.Embed(
                            title=f"Profile Of {data['name']}",
                            description=data["about"],
                            color=0xFBF2EB,
                        )

                        try:
                            embed.set_thumbnail(url=data["avatar"])
                        except:
                            pass

                        embed.add_field(
                            name="School", value=data["school"], inline=False
                        )
                        embed.add_field(
                            name="Country", value=data["country"], inline=True
                        )
                        embed.add_field(
                            name="Ranking", value=data["ranking"], inline=True
                        )
                        embed.add_field(
                            name="Reputation", value=data["reputation"], inline=True
                        )
                        embed.add_field(
                            name="Skills",
                            value=", ".join(data["skillTags"]),
                            inline=False,
                        )

                        if data["gitHub"]:
                            github = data["gitHub"]
                        else:
                            github = None

                        if data["linkedIN"]:
                            linkedin = data["linkedIN"]
                        else:
                            linkedin = None

                        if data["website"]:
                            website = data["website"][0]
                        else:
                            website = None

                        if data["twitter"]:
                            twitter = data["twitter"]
                        else:
                            twitter = None

                        view = ProfileLinks(github, linkedin, twitter, website)
                        await ctx.followup.send(embed=embed, view=view)

                    else:
                        await ctx.followup.send(
                            "User Not Found .... Check The Username And Try Again"
                        )

    @leetcode.command(name="stats", description="Get LeetCode Stats")
    async def stats(self, ctx: discord.ApplicationContext, username: str):
        await ctx.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://alfa-leetcode-api.onrender.com/userProfile/{username}"
            ) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = discord.Embed(
                        title=f"LeetCode Stats for {username}",
                        color=0xFBF2EB,
                    )

                    embed.add_field(
                        name="Total Solved",
                        value=f"{data['totalSolved']} / {data['totalQuestions']}",
                        inline=False,
                    )

                    embed.add_field(
                        name="Easy Problems Solved",
                        value=f"{data['easySolved']} / {data['totalEasy']}",
                        inline=True,
                    )
                    embed.add_field(
                        name="Medium Problems Solved",
                        value=f"{data['mediumSolved']} / {data['totalMedium']}",
                        inline=True,
                    )
                    embed.add_field(
                        name="Hard Problems Solved",
                        value=f"{data['hardSolved']} / {data['totalHard']}",
                        inline=True,
                    )

                    submissions = data["totalSubmissions"]
                    for submission in submissions:
                        embed.add_field(
                            name=f"{submission['difficulty']} Submissions",
                            value=f"Solved: {submission['count']}\nTotal Submissions: {submission['submissions']}",
                            inline=False,
                        )

                    embed.add_field(name="Ranking", value=data["ranking"], inline=True)
                    embed.add_field(
                        name="Contribution Points",
                        value=data["contributionPoint"],
                        inline=True,
                    )
                    embed.add_field(
                        name="Reputation", value=data["reputation"], inline=True
                    )

                    await ctx.followup.send(embed=embed)

                else:
                    await ctx.followup.send(
                        "User Not Found .... Check The Username And Try Again"
                    )


class ProfileLinks(discord.ui.View):
    def __init__(self, github=None, linkedin=None, twitter=None, website=None):
        super().__init__()
        self.github = github
        self.linkedin = linkedin
        self.website = website
        self.twitter = twitter

        if self.github != None:
            self.add_item(discord.ui.Button(label="GitHub", url=self.github))
        if self.linkedin != None:
            self.add_item(discord.ui.Button(label="LinkedIn", url=self.linkedin))
        if self.website != None:
            self.add_item(discord.ui.Button(label="Website", url=self.website))
        if self.twitter != None:
            self.add_item(discord.ui.Button(label="Twitter", url=self.twitter))


def setup(bot):
    bot.add_cog(LeetCodeCog(bot))
