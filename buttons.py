import discord

class SearchAndAddButtonsView(discord.ui.View):

  def __init__(self,
               playlist,
               name_cache,
               url_cache):
    super().__init__()
    self.playlist = playlist
    self.name_cache = name_cache
    self.url_cache = url_cache
  
  async def add(self, index, interaction):
    self.playlist.add(self.name_cache[index], self.url_cache[index])
    await interaction.message.edit(embed=discord.Embed(title=f"Added: {list(self.name_cache)[index]}", color=0x00ff00), view=None)

  @discord.ui.button(label="1", row=0, style=discord.ButtonStyle.primary)
  async def button_1(self, interaction, button):
    await self.add(0, interaction)

  @discord.ui.button(label="2", row=0, style=discord.ButtonStyle.primary)
  async def button_2(self, interaction, button):
    await self.add(1, interaction)

  @discord.ui.button(label="3", row=0, style=discord.ButtonStyle.primary)
  async def button_3(self, interaction, button):
    await self.add(2, interaction)

  @discord.ui.button(label="4", row=0, style=discord.ButtonStyle.primary)
  async def button_4(self, interaction, button):
    await self.add(3, interaction)
  
  @discord.ui.button(label="5", row=0, style=discord.ButtonStyle.primary)
  async def button_5(self, interaction, button):
    await self.add(4, interaction)

  @discord.ui.button(label="Exit", row=1, style=discord.ButtonStyle.primary)
  async def button_exit(self, interaction, button):
    await interaction.message.delete()