#!/usr/bin/env python3
"""Regression check for Chapter 23/24 print-figure arrowhead geometry.

Checks both authoritative SVGs and published SVG copies. PNG legibility remains
an independent visual print-size gate; this checker cannot replace that review.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import math
import re

ROOT = Path(__file__).resolve().parents[2]
NS = '{http://www.w3.org/2000/svg}'


def check_one(fid: str) -> None:
    master = ROOT / 'assets/shared-figures/sources' / f'{fid}.svg'
    published = ROOT / 'assets/shared-figures/rendered' / f'{fid}.svg'
    assert master.read_bytes() == published.read_bytes(), f'{fid}: stale published SVG'
    root = ET.fromstring(master.read_bytes())
    assert (ROOT / 'assets/shared-figures/rendered' / f'{fid}.png').stat().st_size > 10_000
    rects = []
    for rect in root.findall(f'.//{NS}rect'):
        x, y = float(rect.get('x', '0')), float(rect.get('y', '0'))
        w, h = float(rect.get('width', '0')), float(rect.get('height', '0'))
        if w < 1000:  # omit the full-canvas background
            rects.append((x, y, x + w, y + h))
    tips = []
    if fid.startswith('F23'):
        markers = root.findall(f'.//{NS}marker')
        assert len(markers) == 1, f'{fid}: missing/repeated marker definitions'
        marker = markers[0]
        assert marker.get('markerUnits') == 'userSpaceOnUse', f'{fid}: scale-dependent marker'
        assert float(marker.get('markerWidth')) <= 16
        for path in root.findall(f'.//{NS}path'):
            if 'marker-end' not in path.attrib:
                continue
            d = path.get('d', '')
            nums = [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?', d)]
            assert len(nums) >= 4 and len(nums) % 2 == 0, f'{fid}: malformed arrow path'
            tips.append((nums[-2], nums[-1]))
    else:
        for p in root.findall(f'.//{NS}polygon'):
            pts = p.get('points', '').split()
            assert len(pts) == 3, f'{fid}: arrow needs three vertices'
            vertices = [tuple(map(float, v.split(','))) for v in pts]
            tips.append(vertices[0])
            side = math.dist(vertices[1], vertices[2])
            length = math.dist(vertices[0], ((vertices[1][0] + vertices[2][0]) / 2,
                                            (vertices[1][1] + vertices[2][1]) / 2))
            assert side <= 13 and length <= 14, f'{fid}: oversized arrowhead'
    assert tips, f'{fid}: no arrowheads found'
    for px, py in tips:
        # The tips must not land inside or on the outline of any receiver box.
        for x1, y1, x2, y2 in rects:
            if x1 - 3 <= px <= x2 + 3 and y1 - 3 <= py <= y2 + 3:
                raise AssertionError(f'{fid}: arrowhead ({px:g},{py:g}) touches node boundary')
    print(f'{fid}: {len(tips)} bounded arrowheads; published master match')


if __name__ == '__main__':
    for ch in (23, 24):
        for i in (1, 2, 3):
            check_one(f'F{ch}-{i:02d}')
    print('Chapter 23–24 arrow geometry PASS (manual print-size review remains required)')
