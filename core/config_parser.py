import configparser
from dataclasses import dataclass


@dataclass
class Bot:
    TOKEN: str
    DB_PATH: str


@dataclass
class Config:
    bot: Bot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    bot = config["bot"]

    return Config(
        bot=Bot(
            TOKEN=bot["TOKEN"],
            DB_PATH=bot['DB_PATH']
        )
    )
