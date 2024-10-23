# refind-palette-builder

## Usage

- Create `config.ini` based on `example.ini` and specify name, font* and colors
- Run script
- Move generated files from `dist/` to `themes/` directory inside your rEFInd location on ESP (probably `/efi/EFI/refind/themes/`)
- Add `include themes/<YOUR_THEME>/theme.conf` at the end of your rEFInd config (probably `/efi/EFI/refind/refind.conf`)

_\*Not supported yet_
