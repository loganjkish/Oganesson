import base64
import os, shutil
from git import Repo
import register_game

def encodeBase64(file):
    with open(f'./games/temp_nzp/{file}', 'rb') as binary_file:
        base64EncodedFile = base64.b64encode(binary_file.read()).decode('ascii')
    return base64EncodedFile

def makeFtewebglPatch():
    wasmBase64 = encodeBase64('ftewebgl.wasm')
    with open ('./games/nzp/patch.js', 'r', encoding='utf-8') as patch:
        return  patch.read().replace('{wasm_base64}', wasmBase64)

def ftewbglPatcher():
    with open('./games/temp_nzp/ftewebgl.js', 'r', encoding='utf-8', errors='ignore') as f:
        ftewebglScript = f.read()
    moduleStart = ftewebglScript.find('var Module =') + 11
    moduleEnd = ftewebglScript.find('};', moduleStart) + 2
    patchedFtewebglScript = ftewebglScript[:moduleEnd] + '\n' + makeFtewebglPatch() + '\n' + ftewebglScript[moduleEnd:]
    with open('./games/temp_nzp/ftewebgl_patched.js', 'w') as patchedScript:
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
    with open('./games/temp_nzp/index.html', 'r', encoding='utf-8', errors='ignore') as f:
        index = f.read()
    with open('./games/nzp/patch.html', 'r', encoding='utf-8', errors='ignore') as f:
        patch = f.read()
    head = index.find('<head>') + 6
    index = index[:head] + '\n' + patch + '\n' + index[head:]
    filesStart = index.find('files:') + 9
    filesEnd = filesStart + 108
    index = index[:filesStart] + makeIndexPatch2() + index[filesEnd:]
    with open('./games/temp_nzp/ftewebgl_patched.js', 'r', encoding='utf-8', errors='ignore') as f:
        js = f.read()
    js = js.replace('\\', '\\\\').replace('`', '\\`')
    index = index.replace('s.setAttribute(\'src\',"ftewebgl.js");', f's.textContent=`\n{js}\n`')
    index = index.replace('Please allow/unblock our javascript to play.', 'Please wait, this may take a while to load. Do not switch tabs.')
    index = index.replace('<img src="https://hits.sh/hits.sh/nzp-team.github.io/latest/game.html/hits.svg" style="opacity:0;width:0px;">', '')
    with open('./games/temp_nzp/index_patched.html', 'w') as f:
        f.write(index)

def package():
    Repo.clone_from('https://github.com/nzp-team/nzp-team.github.io', './games/temp_nzp')
    ftewbglPatcher()
    indexPatcher()
    register_game.register_game("./games/temp_nzp/nzportable.ico", './games/temp_nzp/index_patched.html', 'nzp')
    shutil.rmtree('./games/temp_nzp')