"""Make every numbered in-text citation a direct link to its source."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "proposal" / "DeepAlign-Bench_研究Proposal.md",
    ROOT / "proposal" / "DeepAlign-Bench_正式Proposal精简版.md",
    ROOT / "proposal" / "DeepAlign-Bench_人话版.md",
    ROOT / "proposal" / "DeepAlign-Bench_汇报精简版.md",
]

FALLBACKS = {
    "OpenCompass": "https://arxiv.org/abs/2605.19276",
    "EvalScope": "https://evalscope.readthedocs.io/en/refact_readme/get_started/introduction.html",
    "PaperBench": "https://openai.com/index/paperbench/",
    "Holistic Evaluation": "https://arxiv.org/abs/2211.09110",
    "HELM": "https://arxiv.org/abs/2211.09110",
    "Beyond Accuracy": "https://aclanthology.org/2020.acl-main.442/",
    "CheckList": "https://aclanthology.org/2020.acl-main.442/",
    "BenchmarkCards": "https://papers.neurips.cc/paper_files/paper/2025/hash/76175f4355e2f67cf91be468c8860070-Abstract-Datasets_and_Benchmarks_Track.html",
}


def reference_urls(reference_text):
    urls = {}
    for line in reference_text.splitlines():
        match = re.match(r"^\[(\d+)\]\s+(.*)$", line.strip())
        if not match:
            continue
        number, entry = int(match.group(1)), match.group(2)
        explicit = re.search(r"https?://\S+", entry)
        if explicit:
            urls[number] = explicit.group(0).rstrip(".,;，。；")
            continue
        arxiv = re.search(r"arXiv:(\d{4}\.\d{4,5})", entry, re.I)
        if arxiv:
            urls[number] = f"https://arxiv.org/abs/{arxiv.group(1)}"
            continue
        for title_fragment, url in FALLBACKS.items():
            if title_fragment in entry:
                urls[number] = url
                break
    return urls


def link_body(body, urls):
    # Normalize citation links created by earlier versions so the visible
    # Markdown label retains conventional square brackets.
    body = re.sub(
        r"(?<!\[)\[(\d+)\]\((https?://[^)\s]+)\)",
        lambda match: f"[[{match.group(1)}]]({match.group(2)})",
        body,
    )

    def expand_range(match):
        start, end = int(match.group(1)), int(match.group(2))
        if start > end or any(number not in urls for number in range(start, end + 1)):
            return match.group(0)
        return "".join(f"[[{number}]]({urls[number]})" for number in range(start, end + 1))

    body = re.sub(r"(?<!\[)\[(\d+)[-–](\d+)\](?![\]\(])", expand_range, body)

    def link_one(match):
        number = int(match.group(1))
        url = urls.get(number)
        return f"[[{number}]]({url})" if url else match.group(0)

    return re.sub(r"(?<!\[)\[(\d+)\](?![\]\(])", link_one, body)


def update(path):
    text = path.read_text(encoding="utf-8")
    marker = "## 参考文献"
    if marker not in text:
        raise ValueError(f"No reference section in {path}")
    body, references = text.split(marker, 1)
    urls = reference_urls(references)
    linked = link_body(body, urls)
    unresolved = re.findall(r"(?<!\[)\[\d+(?:[-–]\d+)?\](?![\]\(])", linked)
    if unresolved:
        raise ValueError(f"Unresolved citations in {path.name}: {sorted(set(unresolved))}")
    path.write_text(linked + marker + references, encoding="utf-8")
    print(f"{path.name}: {len(urls)} reference URLs")


if __name__ == "__main__":
    for source in SOURCES:
        update(source)
