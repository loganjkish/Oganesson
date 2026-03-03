import shutil
from git import Repo
import util.register_game as register_game
from util.encode_base64 import encode_base64
from pathlib import Path

def ftewbgl_patcher():
    index = Path('./games/temp_nzp/index.html').read_text()
    ftewebgl = Path('./games/temp_nzp/ftewebgl.js').read_text()
    patch = Path('./games/nzp/ftewebgl.js').read_text().replace('{wasm_base64}', encode_base64('./games/temp_nzp/ftewebgl.wasm'))
    ftewebgl = ftewebgl.replace('var Module=typeof Module!="undefined"?Module:{};', f'var Module=typeof Module!="undefined"?Module:{{}};\n{patch}')
    ftewebgl = ftewebgl.replace('\\', '\\\\').replace('`', '\\`')
    index = index.replace('s.setAttribute(\'src\',"ftewebgl.js");', f's.textContent=`\n{ftewebgl}\n`')
    Path('./games/temp_nzp/index.html').write_text(index)

def files_patcher():
    index = Path('./games/temp_nzp/index.html').read_text()
    files = Path('./games/nzp/files.js').read_text()
    files = files.replace('{defaultfmf_base64}', encode_base64('./games/temp_nzp/default.fmf').replace('\\', '\\\\'))
    files = files.replace('{gamepk3_base64}', encode_base64('./games/temp_nzp/nzp/game.pk3').replace('\\', '\\\\'))
    files = files.replace('{progspk3_base64}', encode_base64('./games/temp_nzp/nzp/progs.pk3').replace('\\', '\\\\'))
    index = index.replace('''files:
	{
		"default.fmf" : "default.fmf",
		"nzp/game.pk3" : "nzp/game.pk3",
		"nzp/progs.pk3" : "nzp/progs.pk3"
	},''', files)
    Path('./games/temp_nzp/index.html').write_text(index)

def index_patcher():
    index = Path('./games/temp_nzp/index.html').read_text()
    index = index.replace('Please allow/unblock our javascript to play.', 'Please wait, this may take a while to load. Do not switch tabs.')
    index = index.replace('<img src="https://hits.sh/hits.sh/nzp-team.github.io/latest/game.html/hits.svg" style="opacity:0;width:0px;">', '')
    Path('./games/temp_nzp/index.html').write_text(index)

def package():
    Repo.clone_from('https://github.com/nzp-team/nzp-team.github.io', './games/temp_nzp', depth=1)
    ftewbgl_patcher()
    files_patcher()
    index_patcher()
    register_game.register_game("./games/temp_nzp/nzportable.ico", './games/temp_nzp/index.html', 'nzp')
    shutil.rmtree('./games/temp_nzp')