files:
	{
		"default.fmf" : Uint8Array.from(atob("{defaultfmf_base64}"), c => c.charCodeAt(0)),
		"nzp/game.pk3" : Uint8Array.from(atob("{gamepk3_base64}"), c => c.charCodeAt(0)),
		"nzp/progs.pk3" : Uint8Array.from(atob("{progspk3_base64}"), c => c.charCodeAt(0))
	},