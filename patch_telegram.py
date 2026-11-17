"""Patch Hermes Telegram TCP keepalive only when Telegram webhook is enabled."""
from importlib.util import find_spec
from pathlib import Path

spec = find_spec("plugins.platforms.telegram.telegram_network")
if spec is None or spec.origin is None:
    raise SystemExit("Telegram network module not found; refusing to deploy")

path = Path(spec.origin)
source = path.read_text()
needle = '    options: list[tuple[int, int, int]] = [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)]'
replacement = ('    import os\n'
               '    if os.getenv("TELEGRAM_WEBHOOK_URL"):\n'
               '        return []\n' + needle)
if source.count(needle) != 1:
    raise SystemExit("Telegram keepalive implementation changed; refusing unsafe patch")
path.write_text(source.replace(needle, replacement, 1))
print(f"Patched Telegram keepalive for webhook mode: {path}")
