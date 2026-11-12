"""Build a dedicated server copy of the FunDumCraft Prism instance.

Usage (from the repo root):
    python server-pack/make_server_pack.py <output dir> [--zip]
    python server-pack/make_server_pack.py <output dir> --instance "<path to .../minecraft>"

Copies only what a server needs (mods, config, defaultconfigs, kubejs, datapacks)
and leaves out every jar listed in client-only-mods.txt, because those crash a
dedicated server during startup or do nothing on one.
"""
import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_INSTANCE = HERE.parent / "FunDumCraft- Limitless" / "minecraft"
SERVER_DIRS = ("config", "defaultconfigs", "kubejs", "datapacks")


def load_client_only(list_file: Path) -> set[str]:
    names = set()
    for line in list_file.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            names.add(line)
    return names


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("output_dir", type=Path, help="new or empty folder to write the server files into")
    ap.add_argument("--instance", type=Path, default=DEFAULT_INSTANCE, help="the instance's minecraft folder")
    ap.add_argument("--list", type=Path, default=HERE / "client-only-mods.txt", help="client-only jar list")
    ap.add_argument("--zip", action="store_true", help="also write <output_dir>.zip for uploading")
    args = ap.parse_args()

    src: Path = args.instance
    out: Path = args.output_dir
    if not (src / "mods").is_dir():
        print(f"No mods folder under {src}", file=sys.stderr)
        return 1
    if out.exists() and any(out.iterdir()):
        print(f"{out} already has files in it, pick a new folder", file=sys.stderr)
        return 1

    client_only = load_client_only(args.list)
    (out / "mods").mkdir(parents=True, exist_ok=True)

    kept, skipped = 0, []
    for jar in sorted((src / "mods").glob("*.jar")):
        if jar.name in client_only:
            skipped.append(jar.name)
            continue
        shutil.copy2(jar, out / "mods" / jar.name)
        kept += 1

    for d in SERVER_DIRS:
        if (src / d).is_dir():
            shutil.copytree(src / d, out / d)

    print(f"Copied {kept} mods and left out {len(skipped)} client-only mods.")
    missing = sorted(client_only - set(skipped))
    if missing:
        print("WARNING: these are in client-only-mods.txt but not in the pack. If a mod was")
        print("updated, put its new file name in the list or the server may crash again:")
        for m in missing:
            print(f"  {m}")

    if args.zip:
        archive = shutil.make_archive(str(out), "zip", root_dir=out)
        print(f"Wrote {archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
