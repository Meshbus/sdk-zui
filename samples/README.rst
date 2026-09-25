ZUI samples
###########

These applications demonstrate ZUI assets, components, drawing,
host/router state, input, screen lifecycle, and toast animation. Their source
lives under ``samples/``.

The ``sample.yaml`` files select ``mesh_probe_r2/nrf54l15/cpuapp``. Its board
definition is external to this repository. Supply a board package whose root
contains ``boards/`` through ``BOARD_ROOT``, and inspect the selected sample's
configuration and overlays for its display and input requirements. Additional
targets require their own integration and validation.

Activate your Zephyr development environment, then build a sample from the
west workspace root, replacing the board-package path with your own::

   west build -p always -b mesh_probe_r2/nrf54l15/cpuapp \
     modules/lib/zui/samples/draw -d build/sample-zui-draw \
     -- -DBOARD_ROOT=/absolute/path/to/board-package

Replace ``draw`` with ``assets``, ``component``, ``host``, ``input``, ``screen``,
or ``toast`` for the other applications. Each directory contains its own
``sample.yaml``, configuration, and source. Use the target and configuration
declared by the selected scenario. A successful build does not verify rendering,
hardware input, or screen transitions on the device.
