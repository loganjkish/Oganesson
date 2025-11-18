import os, shutil
from git import Repo
import register_game

def package():
    Repo.clone_from('https://github.com/R74nCom/sandboxels', './games/temp')
    shutil.copytree('./games/temp', './temp/games/sandboxels')
    shutil.rmtree('./games/temp')
    register_game.register_game("/icons/favicon.ico", "sandboxels")