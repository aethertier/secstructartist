from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING
from matplotlib.path import Path
import numpy as np
from .lineq import intersection

if TYPE_CHECKING:
    from ..helix import HelixContext


GroupedVertices = List[List[Tuple[float, float]]]

GroupedCodes = List[List[int]]


class HelixPathHelper:

    @classmethod
    def make_path(cls, ctx: HelixContext):
        verts = cls.make_vertices(ctx)
        codes = cls.make_codes(verts)
        verts = np.concatenate(verts, axis=0)
        codes = np.concatenate(codes, axis=0)
        return Path(verts, codes)
    
    @staticmethod
    def make_vertices(ctx: HelixContext) -> GroupedVertices:

        y0, y1 = ctx.y - ctx.dy, ctx.y + ctx.dy

        # Generate vertices for downward turns
        dwturns = []
        x0 = ctx.x + .5 * ctx.dx_halfturn + .5 * ctx.dx_ribbon

        for _ in range(1, ctx.num_halfturns, 2):
            x1 = x0 + ctx.dx_halfturn
            x2 = x1 - ctx.dx_ribbon
            x3 = x0 - ctx.dx_ribbon
            dwturns.append([
                [x0, y1], [x1, y0], [x2, y0], [x3, y1], [x0, y1]
            ])
            x0 += 2 * ctx.dx_halfturn

        if ctx.num_halfturns % 2 == 1:
            x1 = ctx.x + ctx.dx
            x2 = x0 - ctx.dx_ribbon
            dwturns.append([
                [x0, y1], [x1, ctx.y], [x2, y1], [x0, y1]
            ])

        # Generate vertices for upward turns
        dwtr = dwturns[0]
        p2 = [ctx.x, ctx.y]
        p0 = dwtr[-2]
        p1 = list(intersection(p2, dwtr[-1], dwtr[-2], dwtr[-3]))
        all_turns = [[p0, p1, p2 ,p0], dwtr]

        for dwtl, dwtr in zip(dwturns, dwturns[1:]):
            p0 = dwtr[-2]
            p1 = list(intersection(dwtl[1], dwtr[-1], dwtr[-2], dwtr[-3]))
            p2 = dwtl[1]
            p3 = list(intersection(dwtl[0], dwtl[1], dwtl[2], dwtr[-2]))
            all_turns.append([p0, p1, p2, p3, p0])
            all_turns.append(dwtr)

        if ctx.num_halfturns % 2 == 0:
            dwtl = dwturns[-1]
            p0 = [ctx.x + ctx.dx, ctx.y]
            p1 = dwtl[1]
            p2 = list(intersection(p0, dwtl[2], dwtl[1], dwtl[0]))
            all_turns.append([p0, p1, p2 ,p0])

        if not ctx.fill_inner_ribbon:
            for i in range(0, len(all_turns), 2):
                inner = all_turns[i]
                all_turns[i] = [*inner[:-1], *inner[::-1]]

        return all_turns
    
    @staticmethod
    def make_codes(vertices: GroupedVertices) -> GroupedCodes:
        codes = []
        for verts in vertices:
            n = len(verts)
            if n < 3:
                raise ValueError('Each segment needs at least 3 points')
            codes.append([Path.MOVETO] + [Path.LINETO] * (n - 1))
        return codes