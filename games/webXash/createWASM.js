const xashwasmBinary = Uint8Array.from(atob("wasm_base64"), c => c.charCodeAt(0));
async function createWasm() {
    const imports = getWasmImports();
    const { instance, module } = await WebAssembly.instantiate(xashwasmBinary, imports);
    
    wasmExports = instance.exports;
    mergeLibSymbols(wasmExports);
    const dylinkMetadata = getDylinkMetadata(module);
    if (dylinkMetadata.neededDynlibs) {
        dynamicLibraries = dylinkMetadata.neededDynlibs.concat(dynamicLibraries);
    }
    assignWasmExports(wasmExports);
    updateGOT(wasmExports);
    LDSO.init();
    loadDylibs();
    updateMemoryViews();
    return wasmExports;
}