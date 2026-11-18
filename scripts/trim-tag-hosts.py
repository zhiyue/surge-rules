"""Remove self-mappings from the upstream TAG DNS module."""

import re
import sys
from pathlib import Path


def trim(source: str) -> str:
    in_host = False
    aliases = []
    removed = 0
    for number, line in enumerate(source.splitlines(), 1):
        if line.strip() == "[Host]" and not in_host:
            in_host = True
            continue
        line = re.split(r"\s+(?:#|//|;)", line.strip(), maxsplit=1)[0].rstrip()
        if not line or line.startswith(("#", "//", ";")):
            continue
        match = re.fullmatch(r"([\w.-]+)\s*=\s*([\w.-]+)", line, flags=re.ASCII)
        if not in_host or not match or any("." not in name for name in match.groups()):
            raise ValueError(f"Unexpected TAG module content on line {number}")
        name, target = match.groups()
        if name.rstrip(".").lower() == target.rstrip(".").lower():
            removed += 1
        else:
            aliases.append(f"{name} = {target}")
    if not aliases:
        raise ValueError("TAG module contains no distinct Host aliases; keeping the current release")
    print(f"TAG Host: removed {removed} self-mappings; kept {len(aliases)} aliases")
    return (
        "#!name=TAG Profile Lite\n"
        "#!desc=TAG node DNS aliases without self-mappings.\n\n"
        "[Host]\n" + "\n".join(aliases) + "\n"
    )


if __name__ == "__main__":
    source, output = map(Path, sys.argv[1:])
    output.write_text(trim(source.read_text(encoding="utf-8-sig")), encoding="utf-8")
