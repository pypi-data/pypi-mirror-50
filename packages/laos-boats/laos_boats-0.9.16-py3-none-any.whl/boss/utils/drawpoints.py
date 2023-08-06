import numpy as np
from . import sobol_seq


class DrawPoints:
    "Utilities for drawing points within specified bounds"

    @staticmethod
    def random(num_pts, bounds):
        "Returns num_pts random points from a uniform distribution."
        dim = len(bounds)
        rands = np.random.random((num_pts, dim))

        bls = [bounds[n][1] - bounds[n][0] for n in range(dim)]

        pts = [[bounds[n][0] + rand[n] * bls[n] for n in range(dim)]
            for rand in rands]

        return pts

    @staticmethod
    def sobol(num_pts, bounds, shift):
        """Returns num_pts points from a Sobol sequence."""
        dim = len(bounds)
        sobs = np.transpose(sobol_seq.i4_sobol_generate(dim, num_pts, 1))

        bls = [bounds[n][1] - bounds[n][0] for n in range(dim)]

        pts = [[bounds[n][0] + (sob[n]*bls[n] + shift[n]) % bls[n]
            for n in range(dim)] for sob in sobs]

        return pts
