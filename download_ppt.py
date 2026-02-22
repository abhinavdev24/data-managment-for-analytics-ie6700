#!/usr/bin/env python3
"""
Download slide images from a public Google Slides link and generate a PDF.

Usage:
  python download_ppt.py "https://docs.google.com/presentation/d/<ID>/htmlpresent"
  python download_ppt.py "https://docs.google.com/presentation/d/<ID>/htmlpresent" --out pps2
  python download_ppt.py "https://docs.google.com/presentation/d/<ID>/htmlpresent" --out "MySlides.pdf"

Behavior:
  - Downloads slide PNGs into `temp_download_slides/` (configurable).
  - Generates a PDF named after the web page title (sanitized) unless an explicit
    `.pdf` output path is provided.
"""

from __future__ import annotations

import argparse
import html as html_lib
import os
import re
import sys
import time
import urllib.parse
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable


def _extract_presentation_id(url: str) -> str:
    # Common forms:
    #   https://docs.google.com/presentation/d/<ID>/edit
    #   https://docs.google.com/presentation/d/<ID>/htmlpresent
    m = re.search(r"/presentation/d/([a-zA-Z0-9_-]+)", url)
    if m:
        return m.group(1)

    # Fallback: id=<ID>
    parsed = urllib.parse.urlparse(url)
    q = urllib.parse.parse_qs(parsed.query)
    if "id" in q and q["id"]:
        return q["id"][0]

    raise ValueError("Could not extract Google Slides presentation id from URL.")


def _normalize_to_htmlpresent_url(url: str) -> str:
    """
    Convert any Google Slides presentation URL into the corresponding `/htmlpresent` URL.
    Example:
      https://docs.google.com/presentation/d/<ID>/edit?... -> https://docs.google.com/presentation/d/<ID>/htmlpresent
    """
    presentation_id = _extract_presentation_id(url)
    return f"https://docs.google.com/presentation/d/{presentation_id}/htmlpresent"


def _page_key(pageid: str) -> tuple[int, str]:
    m = re.fullmatch(r"p(\d+)", pageid)
    if not m:
        return (10**9, pageid)
    return (int(m.group(1)), pageid)


@dataclass(frozen=True)
class HttpResponse:
    status: int
    content_type: str
    body: bytes


def _http_get(url: str, headers: dict[str, str], timeout_s: int) -> HttpResponse:
    """
    Stateless GET (no cookie jar). Uses `requests` if available, else urllib.
    """
    try:
        import requests  # type: ignore

        r = requests.get(url, headers=headers, timeout=timeout_s)
        return HttpResponse(
            status=int(r.status_code),
            content_type=(r.headers.get("content-type") or "").split(";")[0].strip(),
            body=bytes(r.content),
        )
    except ModuleNotFoundError:
        import urllib.request

        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                ct = resp.headers.get("content-type") or ""
                return HttpResponse(
                    status=int(getattr(resp, "status", 200)),
                    content_type=ct.split(";")[0].strip(),
                    body=resp.read(),
                )
        except urllib.error.HTTPError as e:  # type: ignore[attr-defined]
            ct = (e.headers.get("content-type") if e.headers else "") or ""
            return HttpResponse(
                status=int(e.code),
                content_type=ct.split(";")[0].strip(),
                body=e.read() if hasattr(e, "read") else b"",
            )


def _extract_viewpage_urls(html: str, presentation_id: str) -> list[str]:
    # URLs sometimes appear inside JS snippets and can end with a trailing ');'
    raw = re.findall(
        rf"https://docs\.google\.com/presentation/d/{re.escape(presentation_id)}/viewpage\?[^\"']+",
        html,
    )
    urls: list[str] = []
    for u in raw:
        u2 = html_lib.unescape(u).rstrip(");")
        urls.append(u2)
    return urls


def _with_query_updates(url: str, updates: dict[str, str | None]) -> str:
    parsed = urllib.parse.urlparse(url)
    q = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    for k, v in updates.items():
        if v is None:
            q.pop(k, None)
        else:
            q[k] = [v]
    new_query = urllib.parse.urlencode(q, doseq=True)
    return urllib.parse.urlunparse(parsed._replace(query=new_query))


def _extract_title(html: str) -> str | None:
    m = re.search(r"<title>\s*(.*?)\s*</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    title = html_lib.unescape(m.group(1))
    title = re.sub(r"\s+", " ", title).strip()
    return title or None


def _normalize_title_for_filename(title: str) -> str:
    # Common Google Slides title patterns:
    #   "<Deck Name> - Google Slides"
    # Sometimes the deck name itself includes a file-like suffix such as ".ppt".
    title = re.sub(r"\s*-\s*Google Slides\s*$", "", title, flags=re.IGNORECASE).strip()
    title = re.sub(r"\s*\|\s*Google Slides\s*$", "", title, flags=re.IGNORECASE).strip()
    title = re.sub(r"\.(pptx?|pdf|key)\b", "", title, flags=re.IGNORECASE).strip()
    return title


def _sanitize_filename(name: str, max_len: int = 120) -> str:
    # Keep it simple and cross-platform:
    # - Replace path separators and invalid characters with underscore.
    # - Collapse whitespace.
    name = name.strip()
    name = name.replace("/", "_").replace("\\", "_")
    name = re.sub(r"[\x00-\x1f\x7f]", "_", name)  # control chars
    name = re.sub(r'[<>:"|?*]', "_", name)  # Windows-invalid
    name = re.sub(r"\s+", " ", name).strip()
    name = name.strip(". ")  # avoid hidden/odd names
    if not name:
        name = "slides"
    if len(name) > max_len:
        name = name[:max_len].rstrip()
    return name


def _iter_slide_pngs(slide_paths: Iterable[Path]):
    try:
        from PIL import Image  # type: ignore
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "Pillow is required to generate PDFs. Install it with: pip install pillow"
        ) from e

    for p in slide_paths:
        im = Image.open(p)
        if im.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            yield bg
        else:
            yield im.convert("RGB")


def _write_pdf(slide_paths: list[Path], out_pdf: Path) -> None:
    images = list(_iter_slide_pngs(slide_paths))
    if not images:
        raise RuntimeError("No slide images found to write PDF.")
    first, rest = images[0], images[1:]
    first.save(out_pdf, save_all=True, append_images=rest)


def _download_one_slide(
    *,
    idx: int,
    total: int,
    pageid: str,
    url: str,
    dest_path: Path,
    headers: dict[str, str],
    retries: int,
) -> tuple[int, str, int]:
    out_name = dest_path.name
    last_err = ""
    for attempt in range(1, retries + 1):
        img = _http_get(url, headers=headers, timeout_s=60)
        if img.status == 200 and img.content_type.startswith("image/"):
            dest_path.write_bytes(img.body)
            return (idx, out_name, len(img.body))

        last_err = f"status={img.status} ct={img.content_type} len={len(img.body)}"
        if attempt < retries:
            time.sleep(0.5)

    raise RuntimeError(f"Failed {pageid}: {last_err}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Download slide PNGs from a Google Slides URL.")
    parser.add_argument("url", help="Google Slides URL (any /presentation/d/<id>/... form).")
    parser.add_argument(
        "--out",
        default=".",
        help="Output directory OR output PDF file path (default: current directory).",
    )
    parser.add_argument(
        "--temp-dir",
        default="temp_download_slides",
        help="Temp directory for downloading slide PNGs (default: temp_download_slides).",
    )
    parser.add_argument(
        "--keepimg",
        action="store_true",
        dest="keepimg",
        help="Keep downloaded PNGs in temp dir (default: remove after PDF generation).",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        dest="keepimg",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--images-out",
        default=None,
        help="Optional directory to also save slide PNGs (copied from temp).",
    )
    parser.add_argument(
        "--show-text",
        default="1",
        choices=["0", "1"],
        help="Render slide text layer (default: 1).",
    )
    parser.add_argument("--width", default=None, help="Optional image width (e.g., 1600).")
    parser.add_argument("--height", default=None, help="Optional image height (e.g., 900).")
    parser.add_argument("--sleep", type=float, default=0.15, help="Delay between downloads (seconds).")
    parser.add_argument("--retries", type=int, default=3, help="Retries per slide (default: 3).")
    parser.add_argument(
        "--workers",
        type=int,
        default=(os.cpu_count() or 4),
        help="Parallel download workers (default: number of CPU cores).",
    )
    args = parser.parse_args(argv)

    htmlpresent_url = _normalize_to_htmlpresent_url(args.url)
    presentation_id = _extract_presentation_id(htmlpresent_url)

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": htmlpresent_url,
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*",
    }

    out_path = Path(args.out)
    temp_dir = Path(args.temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    resp = _http_get(htmlpresent_url, headers=headers, timeout_s=30)
    if resp.status != 200:
        print(f"Failed to fetch {htmlpresent_url}: status={resp.status} ct={resp.content_type}", file=sys.stderr)
        return 2

    try:
        html_text = resp.body.decode("utf-8", errors="replace")
    except Exception:
        html_text = str(resp.body)

    title = _extract_title(html_text) or f"slides_{presentation_id}"
    title = _normalize_title_for_filename(title)
    sanitized_title = _sanitize_filename(title).replace(".", " ")
    sanitized_title = _sanitize_filename(sanitized_title)

    urls = _extract_viewpage_urls(html_text, presentation_id)
    if not urls:
        print(
            "No slide image URLs found. The presentation may not be publicly accessible or Google changed the page format.",
            file=sys.stderr,
        )
        return 3

    # Map pageid -> url (unique per slide)
    page_to_url: dict[str, str] = {}
    for u in urls:
        parsed = urllib.parse.urlparse(u)
        q = urllib.parse.parse_qs(parsed.query)
        pageid = (q.get("pageid") or [None])[0]
        if not pageid:
            continue
        updates: dict[str, str | None] = {"showText": args.show_text}
        if args.width:
            updates["w"] = str(args.width)
        if args.height:
            updates["h"] = str(args.height)
        page_to_url[pageid] = _with_query_updates(u, updates)

    pages = sorted(page_to_url.keys(), key=_page_key)
    print(f"Found {len(pages)} slides")

    # Download into temp_dir
    slide_paths: list[Path] = []
    tasks: list[tuple[int, str, str, Path]] = []
    for idx, pageid in enumerate(pages, start=1):
        out_name = f"slide_{idx:02d}_{pageid}.png"
        slide_path = temp_dir / out_name
        slide_paths.append(slide_path)  # preserves PDF order
        tasks.append((idx, pageid, page_to_url[pageid], slide_path))

    workers = max(1, int(args.workers))
    workers = min(workers, len(tasks))

    # Parallel download; keep requests stateless to avoid intermittent auth/cookie issues.
    try:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = [
                ex.submit(
                    _download_one_slide,
                    idx=idx,
                    total=len(tasks),
                    pageid=pageid,
                    url=url,
                    dest_path=dest_path,
                    headers=headers,
                    retries=args.retries,
                )
                for (idx, pageid, url, dest_path) in tasks
            ]

            # Print progress as each finishes (order may be non-sequential)
            for fut in as_completed(futures):
                idx, out_name, nbytes = fut.result()
                print(f"{idx:02d}/{len(pages)} {out_name} ({nbytes} bytes)")
                if args.sleep:
                    time.sleep(args.sleep)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 4

    # Determine output PDF path
    if str(out_path).lower().endswith(".pdf"):
        pdf_path = out_path
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        out_path.mkdir(parents=True, exist_ok=True)
        pdf_path = out_path / f"{sanitized_title}.pdf"

    try:
        _write_pdf(slide_paths, pdf_path)
    except Exception as e:
        print(f"Failed to generate PDF: {e}", file=sys.stderr)
        return 5

    # Optionally copy images
    if args.images_out:
        img_out_dir = Path(args.images_out)
        img_out_dir.mkdir(parents=True, exist_ok=True)
        for p in slide_paths:
            (img_out_dir / p.name).write_bytes(p.read_bytes())

    if not args.keepimg:
        for p in slide_paths:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass

        # Remove temp dir if empty
        try:
            temp_dir.rmdir()
        except Exception:
            pass

    print(f"Wrote PDF: {pdf_path}")
    print("Done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
