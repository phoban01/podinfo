package assets

import "embed"

// AssetsFS contains assets
//
//go:embed ui
var AssetsFS embed.FS

// StaticFS continas Static
//
//go:embed static
var StaticFS embed.FS
