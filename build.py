import shutil, os
from minify_html import minify

from games import nzp

def version(nmajor, nminor, npatch):
    with open('./version', 'r') as f:
        version = f.read().strip()
    parts = version.split('.')
    major, minor, patch = map(int, parts)
    if nmajor:
        major += 1
        minor = 0
        patch = 0
    if nminor:
        minor += 1
        patch = 0
    if npatch:
        patch += 1
    new_version = f'{major}.{minor}.{patch}'
    with open('./version', 'w') as f:
        f.write(new_version)
    return new_version

def build(nmajor, nminor, npatch):
    shutil.copytree('./static', './temp', dirs_exist_ok=True)
    os.remove('./temp/particles.min.js')
    new_version = version(nmajor, nminor, npatch)
    nzp.package()
    with open('./temp/index.html', 'r') as f:
        index = f.read()
    index = index.replace("{version}", new_version)
    with open('./static/particles.min.js', 'r') as f:
        particlesjs = f.read()
    index = index.replace('<script src="./particles.min.js"></script>', f'<script>{particlesjs}</script>')
    index = minify(index, minify_css=True, minify_js=True)
    with open('./temp/index.html', 'w') as f:
        f.write(index)

build(False, False, False) 