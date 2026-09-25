# sdk-zui

ZUI is a compact Zephyr UI module with host/router/screen lifecycle, drawing,
input, reusable components, toast notifications and optional predictive input.
Public headers use `<zui/*.h>` and configuration uses `CONFIG_ZUI*`.

## Integration

Add a west project named `zui`, with `repo-path: sdk-zui`,
`path: modules/lib/zui`, a reviewed commit SHA, and
`west-commands: scripts/west-commands.yml`. Include `sdk-u8g2` as module `u8g2`.
Enable `CONFIG_DISPLAY`, `CONFIG_U8G2` and `CONFIG_ZUI` in the application.
For local development, pass the checkout through `ZEPHYR_EXTRA_MODULES`.

Compressed common icons additionally need `sdk-heatshrink` as module
`heatshrink`. This module supplies fallback Zephyr integration for that
library. ZUI selects its default U8g2 fonts in `Kconfig`; see the U8g2 font
license inventory for their terms.

## Tools

`west zui icons INPUT OUTPUT` generates icon data from PNG/GIF files.
`west zui xbms INPUT OUTPUT` generates header-only raw XBM data.
Install Pillow for PNG/GIF support and heatshrink2 for compressed icons;
ImageMagick and the heatshrink CLI are fallback tools.
`--no-compress` disables icon compression. Generated headers include
`<zui/zui.h>` by default. The predictive dictionary generator uses Python's
standard library and is invoked automatically by CMake. Custom dictionary
paths are relative to the application source directory.

## Validation

Run `west twister -T modules/lib/zui/tests -p qemu_x86` from the west workspace.
Set `ZEPHYR_MODULES` to the ZUI, U8g2 and Heatshrink checkouts for the
qemu_x86 suite:

```sh
west twister -T modules/lib/zui/tests -p qemu_x86 -O build/zui-tests \
  --extra-args="ZEPHYR_MODULES=$PWD/modules/lib/zui;$PWD/modules/lib/u8g2;$PWD/modules/lib/heatshrink"
python modules/lib/zui/scripts/test_tools.py
```

The Python checks use a temporary local west workspace to verify command
registration without modifying the caller's active manifest or accessing a
remote. They also compile generated resource data with the host C compiler.

The seven applications under `samples/` demonstrate the module's APIs. Their
`sample.yaml` files select `mesh_probe_r2/nrf54l15/cpuapp`, whose board definition
is supplied externally. To build these targets, provide a board package through
`BOARD_ROOT` with the display and input configuration required by the selected
sample. Other targets require their own integration and validation.
See [samples](samples/README.rst) and [licensing](LICENSING.md).
