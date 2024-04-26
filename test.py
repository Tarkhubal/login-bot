from tools.api import API
from tools.configs import Configs
from tools.database import Database
from tools.pelican_guild import PelicanGuild

configs = Configs("configs.json")
# api = API(configs)
db = Database(configs.db)
guild1 = PelicanGuild(db.get.guild_infos(1))
guild2 = PelicanGuild(db.get.guild_infos(2))

guild1.update(db.get.guild_infos(1))

print(guild1.api.configs.url)