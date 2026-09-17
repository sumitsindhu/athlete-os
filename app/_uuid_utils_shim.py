import os
import sys
import time
import types
import uuid

# File addded due to uuid_utils not being available in the environment

def _pure_uuid7() -> uuid.UUID:
    unix_ts_ms = int(time.time() * 1000)
    rand_a = int.from_bytes(os.urandom(2), "big") & 0x0FFF
    rand_b = int.from_bytes(os.urandom(8), "big") & 0x3FFFFFFFFFFFFFFF
    value = (unix_ts_ms << 80) | (0x7 << 76) | (rand_a << 64) | (0x2 << 62) | rand_b
    return uuid.UUID(int=value)


def _install_shim() -> None:
    compat = types.ModuleType("uuid_utils.compat")
    compat.uuid7 = _pure_uuid7
    sys.modules["uuid_utils.compat"] = compat
    sys.modules["uuid_utils"] = types.ModuleType("uuid_utils")


def _clear_uuid_utils_modules() -> None:
    for name in list(sys.modules):
        if name == "uuid_utils" or name.startswith("uuid_utils."):
            del sys.modules[name]


def ensure_uuid_utils() -> None:
    if os.environ.get("UUID_UTILS_SHIM", "").lower() in ("1", "true", "yes"):
        _clear_uuid_utils_modules()
        _install_shim()
        return

    try:
        from uuid_utils.compat import uuid7 as _check

        _check()
        return
    except ImportError:
        _clear_uuid_utils_modules()
        _install_shim()


ensure_uuid_utils()
