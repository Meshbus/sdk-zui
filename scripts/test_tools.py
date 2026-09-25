# SPDX-FileCopyrightText: 2026 FoBE Studio
# SPDX-License-Identifier: Apache-2.0
"""Exercise standalone west registration, generated C and icon wire encoding."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image
import heatshrink2

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("zui_icon", ROOT / "scripts/zui/assets/icon.py")
icon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(icon)


class ToolsTest(unittest.TestCase):
    def test_icons_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "square.png"
            Image.new("1", (32, 32), 0).save(source)
            raw = icon.file2image(source, False)
            compressed = icon.file2image(source, True)
            self.assertEqual(raw.data[0], 0)
            self.assertEqual(compressed.data[:2], b"\x01\x00")
            self.assertEqual(int.from_bytes(compressed.data[2:4], "little"), len(compressed.data[4:]))
            self.assertEqual(heatshrink2.decompress(compressed.data[4:], window_sz2=8, lookahead_sz2=4), raw.data[1:])

    def test_west_generators_and_generated_c(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            (work / "manifest").mkdir()
            (work / "zui").symlink_to(ROOT, target_is_directory=True)
            (work / "manifest/west.yml").write_text("""manifest:
  projects:
    - name: zui
      url: https://example.invalid/sdk-zui
      path: zui
      west-commands: scripts/west-commands.yml
  self:
    path: manifest
""")
            def run(*args):
                result = subprocess.run(args, cwd=work, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            run("west", "init", "-l", str(work / "manifest"))
            run("west", "zui", "--help")
            source = work / "input"
            source.mkdir()
            Image.new("1", (32, 32), 0).save(source / "square.png")
            frames = [Image.new("1", (16, 16), color) for color in (0, 1)]
            frames[0].save(source / "animation.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
            for mode in ("compressed", "raw"):
                output = work / mode
                args = ("--no-compress",) if mode == "raw" else ()
                run("west", "zui", "icons", str(source), str(output), *args)
                run("cc", "-std=c11", "-Werror", "-fsyntax-only", "-I", str(ROOT / "include"), str(output / "assets_icons.c"))
            output = work / "xbms"
            run("west", "zui", "xbms", str(source), str(output))
            header = next(output.glob("*.h"))
            consumer = output / "consumer.c"
            consumer.write_text(f'#include "{header.name}"\n')
            run("cc", "-std=c11", "-Werror", "-fsyntax-only", "-I", str(ROOT / "include"), str(consumer))

    def test_predictive_generator_relocation(self):
        with tempfile.TemporaryDirectory() as directory:
            for name, source in (("builtin", ROOT / "src/dicts/en_subtlex_words.txt"),
                                 ("fixture", ROOT / "tests/predictive/words.txt")):
                output = Path(directory) / f"{name}.c"
                subprocess.run([sys.executable, str(ROOT / "scripts/zui/gen_predictive_dict.py"),
                                "--input", str(source), "--output", str(output), "--budget", "65536",
                                "--max-candidates", "8", "--max-word-len", "10"], check=True)
                subprocess.run(["cc", "-std=c11", "-Werror", "-fsyntax-only", "-I", str(ROOT / "src"), str(output)], check=True)


if __name__ == "__main__":
    unittest.main()
