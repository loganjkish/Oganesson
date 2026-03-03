(function() {
    const _wasm_base64 = "{wasm_base64}";
    const _bytes = Uint8Array.from(atob(_wasm_base64), c => c.charCodeAt(0));
    Module['wasmBinary'] = _bytes.buffer;
})();
