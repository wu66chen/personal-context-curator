"""Exercise an archive reorganization in a synthetic directory. Stdlib only."""

import argparse
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import unquote


MAIN = "profile/闲暇-桌游经历.md"
SOURCE = "sources/赛程.txt"
INITIAL = {
    "INDEX.md": "# 索引\n\n[桌游经历](profile/桌游经历.md)\n",
    "书签.md": "# 书签\n\n[查看计分](profile/纸舟竞渡.md#计分)\n",
    "profile/桌游经历.md": "# 桌游经历\n\n本人在四人局负责读规则。\n",
    "profile/纸舟竞渡.md": (
        "# 纸舟竞渡\n\n## 计分\n\n本人于 2025-04-08 确认只在决赛按三轮计分。"
        "见[赛程原件](../sources/赛程.txt)。\n"
    ),
    SOURCE: "合成赛程原件。练习赛和决赛采用不同规则。\n",
}
LINK = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")
HEAD = re.compile(r"^#{1,6} (.+)$", re.MULTILINE)


def prepare(root):
    root.mkdir(parents=True, exist_ok=False)
    for name, body in INITIAL.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body.encode("utf-8"))


def check(root):
    root = root.resolve(strict=True)

    def local(name):
        path = (root / name).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f"Fixture path escapes its directory: {name}")
        return path

    def destinations(name):
        result = []
        for link in LINK.findall(local(name).read_text(encoding="utf-8")):
            path, _, fragment = link.removeprefix("<").removesuffix(">").partition("#")
            path, fragment = unquote(path), unquote(fragment)
            dest = Path(name).parent / path if path else Path(name)
            target = local(dest)
            if not target.is_file():
                raise ValueError("Fixture link target is missing")
            if fragment and fragment not in HEAD.findall(target.read_text(encoding="utf-8")):
                raise ValueError("Fixture link points to a missing heading")
            result.append((target, fragment))
        return result

    canonical = local(MAIN)
    body = canonical.read_text(encoding="utf-8")
    for detail in ("四人局", "纸舟竞渡", "2025-04-08", "决赛", "三轮"):
        if detail not in body:
            raise ValueError(f"Missing fixture detail: {detail}")
    if canonical not in {path for path, _ in destinations("INDEX.md")}:
        raise ValueError("No index entry for the merged page")
    headings = list(HEAD.finditer(body))
    sections = {}
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
        sections.setdefault(match[1], []).append(body[match.end():end])
    for path, fragment in destinations("书签.md"):
        matches = sections.get(fragment, [])
        if path == canonical and len(matches) == 1 and "三轮" in matches[0]:
            break
    else:
        raise ValueError("Bookmark does not reach the scoring passage")
    if (local(SOURCE), "") not in destinations(MAIN):
        raise ValueError("Merged page lost the reference to the original schedule")
    if local(SOURCE).read_bytes() != INITIAL[SOURCE].encode("utf-8"):
        raise ValueError("Original schedule changed")
    for old, marker in (("profile/桌游经历.md", "四人局"), ("profile/纸舟竞渡.md", "三轮")):
        if local(old).exists() and marker in local(old).read_text(encoding="utf-8"):
            raise ValueError(f"Duplicate authoritative text at {old}")


def selftest():
    with TemporaryDirectory(prefix="curator-reorg-") as temp:
        root = Path(temp) / "example"
        prepare(root)
        base = root / "profile/桌游经历.md"
        game = root / "profile/纸舟竞渡.md"
        body = base.read_text(encoding="utf-8") + "\n## 纸舟竞渡\n\n"
        body += game.read_text(encoding="utf-8").split("## 计分\n", 1)[1]
        base.rename(root / MAIN)
        (root / MAIN).write_text(body, encoding="utf-8")
        game.unlink()
        (root / "INDEX.md").write_text(f"[闲暇]({MAIN})\n", encoding="utf-8")
        bookmark = root / "书签.md"
        bookmark.write_text(f"[查看计分]({MAIN}#纸舟竞渡)\n", encoding="utf-8")
        check(root)
        for name, changed in (
            ("书签.md", f"[查看计分]({MAIN}#桌游经历)\n"),
            ("INDEX.md", f"[主档]({MAIN}) [失效](missing.md)\n"),
            ("INDEX.md", f"[主档]({MAIN}) [错节]({MAIN}#缺失)\n"),
            (MAIN, body.replace("../sources/", "sources/")),
            (SOURCE, "被改写的原件\n"),
        ):
            target = root / name
            saved = target.read_bytes()
            target.write_text(changed, encoding="utf-8")
            try:
                check(root)
            except ValueError:
                pass
            else:
                raise AssertionError(f"Accepted broken migration in {name}")
            target.write_bytes(saved)
        check(root)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    actions = cli.add_subparsers(dest="action", required=True)
    actions.add_parser("selftest")
    for action in ("prepare", "check"):
        actions.add_parser(action).add_argument("fixture_root", type=Path)
    args = cli.parse_args()
    if args.action == "prepare":
        prepare(args.fixture_root)
    elif args.action == "check":
        check(args.fixture_root)
    else:
        selftest()
    print(f"PASS: synthetic reorganization fixture {args.action}")
