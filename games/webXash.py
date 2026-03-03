import subprocess
import shutil
from git import Repo
import util.register_game as register_game
from util.encode_base64 import encode_base64
from pathlib import Path

def offline_mode():
    index = Path('./games/temp_webXash/dist/index.html').read_text()
    D_PFLE_c = Path('./games/temp_webXash/dist/assets/index-D_PFLE_c.js').read_text()
    b_7h_EiO = Path('./games/temp_webXash/dist/assets/index-b_7h_EiO.css').read_text()
    index = index.replace('<script type="module" crossorigin src="/webXash/assets/index-D_PFLE_c.js"></script>', f'<script type="module">{D_PFLE_c}</script>')
    index = index.replace('<link rel="stylesheet" crossorigin href="/webXash/assets/index-b_7h_EiO.css">', f'<style>{b_7h_EiO}</style>')
    index = index.replace('<link rel="icon" type="image/svg+xml" href="/webXash/assets/hl-bright-BcANNclR.svg" />','')
    Path('./games/temp_webXash/dist/index.html').write_text(index)

def inline_js():
    index = Path('./games/temp_webXash/dist/index.html').read_text()
    c3_RArA = Path('./games/temp_webXash/dist/assets/index-c3_R-ArA.js').read_text()
    exportPatch = Path('./games/webXash/c3_R-ArA_ExportPatch.js').read_text()
    importPatch = Path('./games/webXash/c3_R-ArA_ImportPatch.js').read_text()
    index = index.replace('<script type="module">', f'<script type="module">\n(function(){{{c3_RArA}}})();')
    index = index.replace('export{DEFAULT_CLIENT_LIBRARY,DEFAULT_FILESYSTEM_LIBRARY,DEFAULT_GL4ES_LIBRARY,DEFAULT_GLES3COMPAT_LIBRARY,DEFAULT_MENU_LIBRARY,DEFAULT_SERVER_LIBRARY,DEFAULT_SOFT_LIBRARY,DEFAULT_XASH_LIBRARY,ErrNoLocation,Net,Xash3D};', exportPatch)
    index = index.replace('import("./index-c3_R-ArA.js")', importPatch)
    Path('./games/temp_webXash/dist/index.html').write_text(index)

def replace_createWASM():
    index = Path('./games/temp_webXash/dist/index.html').read_text()
    createWASM = Path('./games/webXash/createWASM.js').read_text()
    createWASM = createWASM.replace('wasm_base64', encode_base64('./games/temp_webXash/dist/assets/xash-CAtKZwSO.wasm'))
    index = index.replace('async function createWasm(){function e(_,l){wasmExports=_.exports;var o=wasmExports;mergeLibSymbols(wasmExports);var c=getDylinkMetadata(l);return c.neededDynlibs&&(dynamicLibraries=c.neededDynlibs.concat(dynamicLibraries)),assignWasmExports(wasmExports),updateGOT(o),LDSO.init(),loadDylibs(),updateMemoryViews(),wasmExports}function r(_){return e(_.instance,_.module)}var t=getWasmImports();if(Module.instantiateWasm)return new Promise((_,l)=>{Module.instantiateWasm(t,(o,c)=>{_(e(o,c))})});wasmBinaryFile??(wasmBinaryFile=findWasmBinary());var n=await instantiateAsync(wasmBinary,wasmBinaryFile,t),a=r(n);return a}', createWASM)
    Path('./games/temp_webXash/dist/index.html').write_text(index)

def replace_fetchExtras():
    index = Path('./games/temp_webXash/dist/index.html').read_text()
    fetchExtras = Path('./games/webXash/fetchExtras.js').read_text()
    fetchExtras = fetchExtras.replace('extras_base64', encode_base64('./games/temp_webXash/dist/assets/extras--X6baQhv.pk3'))
    index = index.replace('async fetchExtras(){const t=await fetch(kc);if(!t.ok)throw new Error(`Failed to fetch extras.pk3: ${t.statusText}`);return await t.arrayBuffer()}', fetchExtras)
    Path('./games/temp_webXash/dist/index.html').write_text(index)

def replace_readAsync():
    index = Path('./games/temp_webXash/dist/index.html').read_text()
    readAysnc = Path('./games/webXash/readAsync.js').read_text()
    readAysnc = readAysnc.replace('Dhq2Sid5_base64', encode_base64('./games/temp_webXash/dist/assets/filesystem_stdio-Dhq2Sid5.wasm'))
    readAysnc = readAysnc.replace('B_eE9xQr_base64', encode_base64('./games/temp_webXash/dist/assets/libmenu-B_eE9xQr.wasm'))
    readAysnc = readAysnc.replace('Aafm3Mse_base64', encode_base64('./games/temp_webXash/dist/assets/libref_webgl2-Aafm3Mse.wasm'))
    readAysnc = readAysnc.replace('C6FeFK01_base64', encode_base64('./games/temp_webXash/dist/assets/hl_emscripten_wasm32-C6FeFK01.wasm'))
    readAysnc = readAysnc.replace('BB4CPMTx_base64', encode_base64('./games/temp_webXash/dist/assets/client_emscripten_wasm32-BB4CPMTx.wasm'))
    readAysnc = readAysnc.replace('D-JUZ5gM_base64', encode_base64('./games/temp_webXash/dist/assets/client_emscripten_wasm32-D-JUZ5gM.wasm'))
    readAysnc = readAysnc.replace('CWCeX_GV_base64', encode_base64('./games/temp_webXash/dist/assets/cs_emscripten_wasm32-CWCeX_GV.wasm'))
    index = index.replace('var readAsync,readBinary;{try{scriptDirectory=new URL(".",_scriptName).href}catch{}readAsync=async e=>{var r=await fetch(e,{credentials:"same-origin"});if(r.ok)return r.arrayBuffer();throw new Error(r.status+" : "+r.url)}}', readAysnc)
    Path('./games/temp_webXash/dist/index.html').write_text(index)

def package():
    repo = Repo.clone_from('https://github.com/x8BitRain/webXash', './games/temp_webXash')
    repo.git.checkout('ff86609dac6f67b52a4731260dd9900e2e6fce65')
    subprocess.run(['npm', 'install', '--save-dev', 'typescript@5.7.3'], cwd='./games/temp_webXash')
    subprocess.run(['npm', 'i'], cwd='./games/temp_webXash')
    subprocess.run(['sh', 'setup-xash.sh'], cwd='./games/temp_webXash')
    subprocess.run(['npm', 'run', 'build'], cwd='./games/temp_webXash')
    offline_mode()
    inline_js()
    replace_createWASM()
    replace_fetchExtras()
    replace_readAsync()
    register_game.register_game('./games/webXash/hl-bright.ico', './games/temp_webXash/dist/index.html', 'webXash')
    shutil.rmtree('./games/temp_webXash')