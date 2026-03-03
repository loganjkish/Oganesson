async fetchExtras() {
    const bytes = Uint8Array.from(atob("extras_base64"), c => c.charCodeAt(0));
    return bytes.buffer;
}