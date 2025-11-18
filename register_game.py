def register_game(icon, name):
    with open('./temp/index.html', 'r', encoding='utf-8', errors='ignore') as f:
        index = f.read()
    gamesEnd = index.find('<!--END GAMES-->') - 1
    gameLink = f'<a href="games/{name}/index.html"><img class="game-icon" src="games/{name}/{icon}"></a>'
    index = index[:gamesEnd] + gameLink + "\n" + index[gamesEnd:]
    with open('./temp/index.html', 'w', encoding='utf-8', errors='ignore') as f:
        f.write(index)