const embeddedWasm = {
    "filesystem_stdio-Dhq2Sid5.wasm": "Dhq2Sid5_base64",
    "libmenu-B_eE9xQr.wasm": "B_eE9xQr_base64",
    "libref_webgl2-Aafm3Mse.wasm": "Aafm3Mse_base64",
    "hl_emscripten_wasm32-C6FeFK01.wasm": "C6FeFK01_base64",
    "client_emscripten_wasm32-BB4CPMTx.wasm": "BB4CPMTx_base64",
    "client_emscripten_wasm32-D-JUZ5gM.wasm": "D-JUZ5gM_base64",
    "cs_emscripten_wasm32-CWCeX_GV.wasm": "CWCeX_GV_base64"
};

function base64ToUint8Array(base64) {
    const binary = atob(base64);
    const len = binary.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binary.charCodeAt(i);
    }
    return bytes;
}
var readAsync = async (path) => {
    const filename = path.split('/').pop();

    if (embeddedWasm[filename]) {
        return base64ToUint8Array(embeddedWasm[filename]).buffer;
    }

    throw new Error("WASM file not embedded: " + filename);
};