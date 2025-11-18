import base64
import os, shutil
from git import Repo
import register_game

def encodeBase64(file):
    with open(f'./games/temp/{file}', 'rb') as binary_file:
        base64EncodedFile = base64.b64encode(binary_file.read()).decode('ascii')
    return base64EncodedFile

def makeFtewebglPatch():
    wasmBase64 = encodeBase64('ftewebgl.wasm')
    with open ('./games/nzp/patch.js', 'r', encoding='utf-8') as patch:
        return  patch.read().replace('{wasm_base64}', wasmBase64)

def ftewbglPatcher():
    with open('./games/temp/ftewebgl.js', 'r', encoding='utf-8', errors='ignore') as f:
        ftewebglScript = f.read()
    moduleStart = ftewebglScript.find('var Module =') + 11
    moduleEnd = ftewebglScript.find('};', moduleStart) + 2
    patchedFtewebglScript = ftewebglScript[:moduleEnd] + '\n' + makeFtewebglPatch() + '\n' + ftewebglScript[moduleEnd:]
    with open('./games/temp/ftewebgl_patched.js', 'w') as patchedScript:
        patchedScript.write(patchedFtewebglScript)

def makeIndexPatch2():
    defailtfmfBase64 = encodeBase64('default.fmf')
    gamepk3Base64 = encodeBase64('nzp/game.pk3')
    progspk3Base64 = encodeBase64('nzp/progs.pk3')
    with open ('./games/nzp/patch2.html', 'r', encoding='utf-8') as patch:
        patch = patch.read()
        patch = patch.replace('{defaultfmf_base64}', defailtfmfBase64)
        patch = patch.replace('{gamepk3_base64}', gamepk3Base64)
        patch = patch.replace('{progspk3_base64}', progspk3Base64)
        return patch

def indexPatcher():
    with open('./games/temp/index.html', 'r', encoding='utf-8', errors='ignore') as f:
        index = f.read()
    with open('./games/nzp/patch.html', 'r', encoding='utf-8', errors='ignore') as f:
        patch = f.read()
    head = index.find('<head>') + 6
    index = index[:head] + '\n' + patch + '\n' + index[head:]
    filesStart = index.find('files:') + 9
    filesEnd = filesStart + 108
    index = index[:filesStart] + makeIndexPatch2() + index[filesEnd:]
    index.replace("Please allow/unblock our javascript to play.", "Please wait, this may take a while to load. Do not switch tabs.")
    with open('./games/temp/index_patched.html', 'w') as f:
        f.write(index)

def package():
    Repo.clone_from('https://github.com/nzp-team/nzp-team.github.io', './games/temp')
    ftewbglPatcher()
    indexPatcher()
    os.makedirs('./temp/games/nzp')
    shutil.copyfile('./games/temp/index_patched.html', './temp/games/nzp/index.html')
    shutil.copyfile('./games/temp/ftewebgl_patched.js', './temp/games/nzp/ftewebgl.js')
    shutil.copyfile('./games/temp/nzportable.ico', './temp/games/nzp/nzportable.ico')
    shutil.rmtree('./games/temp')
    register_game.register_game("nzportable.ico", "nzp")