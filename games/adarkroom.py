import os, shutil
from git import Repo
import register_game

def package():
    Repo.clone_from('https://github.com/doublespeakgames/adarkroom', './games/temp')
    shutil.copytree('./games/temp', './temp/games/adarkroom')
    shutil.rmtree('./games/temp')
    register_game.register_game("favicon.ico", "adarkroom")