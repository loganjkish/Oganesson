from util.encode_base64 import encode_base64
from minify_html import minify
from pathlib import Path

def register_game(icon, gameIndex, name):
    index = Path('./temp/index.html').read_text()
    patch = Path('./util/patch.html').read_text()
    icoData = encode_base64(icon)
    icoUrl = f"data:image/x-icon;base64,{icoData}"
    gameHtml = Path(gameIndex).read_text()
    gameHtml = minify(gameHtml, minify_css=True, minify_js=True)
    gamesEnd = index.find('<!--END GAMES-->') - 1
    patch = patch.replace('{name}', name)
    patch = patch.replace('{icoUrl}', icoUrl)
    patch = patch.replace('{gameHtml}', gameHtml)
    index = index[:gamesEnd] + patch + "\n" + index[gamesEnd:]
    Path('./temp/index.html').write_text(index)