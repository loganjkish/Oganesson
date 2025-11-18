import base64
from minify_html import minify

def register_game(icon, gameIndex, name):
    with open('./temp/index.html', 'r', encoding='utf-8', errors='ignore') as f:
        index = f.read()
    with open('./patch.html', 'r', encoding='utf-8', errors='ignore') as f:
        patch = f.read()
    with open(icon, 'rb') as f:
        icoData = base64.b64encode(f.read()).decode('utf-8')
    icoUrl = f"data:image/x-icon;base64,{icoData}"
    with open(gameIndex, 'r') as f:
        gameHtml = minify(f.read(), minify_css=True, minify_js=True)
        gameBase64 = base64.b64encode(gameHtml.encode('utf-8')).decode('utf-8')
    gamesEnd = index.find('<!--END GAMES-->') - 1
    patch = patch.replace("{name}", name)
    patch = patch.replace("{icoUrl}", icoUrl)
    patch = patch.replace("{gameBase64}", gameBase64)
    index = index[:gamesEnd] + patch + "\n" + index[gamesEnd:]
    with open('./temp/index.html', 'w', encoding='utf-8', errors='ignore') as f:
        f.write(index)