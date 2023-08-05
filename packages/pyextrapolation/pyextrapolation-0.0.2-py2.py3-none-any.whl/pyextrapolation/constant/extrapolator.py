import numpy as np
from tqdm import tqdm


class CE:
    """
    Class for performing constant extrapolation through the solution of the linear hyperbolic PDE:

        du/dt + H(phi) n . grad(u) = 0,

    where H() is the Heaviside step function, phi is a level set field, and n = grad(phi) / | grad(phi) |. This
    equation is solved to steady-state in pseudo-time with a first order upwind spatial discretisation and first
    order time stepping.

    :param u: array of values to be extrapolated
    :param phi: level set field, negative in the interior and positive in the exterior (where values are extrapolated into)
    """

    def __init__(self, u, phi):

        assert u.shape == phi.shape

        self.u = u.astype(np.float64)
        self.phi_max = np.amax(phi)

        phi_grad = np.array(np.gradient(phi))

        if phi_grad.ndim == 1:
            phi_grad = phi_grad[np.newaxis, :]

        phi_grad_magnitude = np.sqrt(np.sum(np.square(phi_grad), axis=0))
        self.grad_mag_threshold = np.percentile(phi_grad_magnitude, 10)
        self.phi_grad_normalised = np.divide(phi_grad, phi_grad_magnitude + 1e-8)

        # We just need to store the sign of phi and phi_grad
        self.pos_phi = phi > 0.0
        self.pos_phi_grad = phi_grad > 0.0

    def compute_upwind_differences(self):
        """
        Compute first order upwind spatial differences

        :return: difference array, same shape as CE.phi_grad
        """

        ndims = self.u.ndim

        upwind_u_grad = np.zeros(self.phi_grad_normalised.shape)

        for dim in range(ndims):
            # Compute differences of u along this dimension
            u_diffs = np.diff(self.u, n=1, axis=dim)

            # Prepend and append zeros to the differences
            zeroshape = list(u_diffs.shape)
            zeroshape[dim] = 1
            zeroplane = np.zeros(shape=zeroshape)
            u_diffs = np.append(u_diffs, zeroplane, axis=dim)
            u_diffs = np.append(zeroplane, u_diffs, axis=dim)

            # Get forward and backward differences via offset slices
            forwarddiffs = [slice(None) for _ in range(ndims)]
            forwarddiffs[dim] = slice(1, None, 1)
            backwarddiffs = [slice(None) for _ in range(ndims)]
            backwarddiffs[dim] = slice(None, -1, 1)

            neg_phi_grad = np.logical_not(self.pos_phi_grad[dim])
            pos_phi_grad = self.pos_phi_grad[dim]

            upwind_u_grad[dim][neg_phi_grad] = u_diffs[tuple(forwarddiffs)][neg_phi_grad]  # Forward difference
            upwind_u_grad[dim][pos_phi_grad] = u_diffs[tuple(backwarddiffs)][pos_phi_grad]  # Backward difference

        return upwind_u_grad

    def solve(self, N=None):
        """
        Apply first order time stepping and first order upwind spatial differences to solve the constant extrapolation
        PDE via the method of lines.

        :param N: (optional) Number of iterations to run. Estimated automatically if not specified.
        :return: the extrapolated array, same shape as CE.u
        """

        # Estimate number of iterations to run for using max distance and 10th percentile of gradient magnitude
        if not N:
            N = int(self.phi_max * (self.u.ndim + 1) / self.grad_mag_threshold)

        for _ in tqdm(range(N)):
            upwind_u_grad = self.compute_upwind_differences()

            u_n = self.u - (1.0 / self.u.ndim) * np.sum(np.multiply(upwind_u_grad, self.phi_grad_normalised), axis=0)

            self.u[self.pos_phi] = u_n[self.pos_phi]

        return self.u.copy()
