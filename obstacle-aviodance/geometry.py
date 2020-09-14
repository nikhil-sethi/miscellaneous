import numpy as np
def confidence_ellipse(x, y, chi = 5.991):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    chi : float
    confidence of enclosing ellipse(from chi square distribution table)
    https://www.itl.nist.gov/div898/handbook/eda/section3/eda3674.htm
    95% confidence: 5.991(2D),7.815(3D)
    95% confidence: 7.378(2D),9.348(3D)
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")
    E, V = np.linalg.eig(np.cov(x, y))  # this might be expensive. replace with above pearson method if possible
    # chi = 5.991  #
    ell_radius_x = np.sqrt(chi * max(E))
    ell_radius_y = np.sqrt(chi * min(E))
    v = V[:, np.argmax(E)]
    angle = np.arctan(v[1]/v[0])
    if angle < 0:
        angle += np.pi
    return (np.mean(x), np.mean(y)), ell_radius_x, ell_radius_y, angle

def rotmat(th):
    return np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])

def unit_vector(vec):
    if np.any(vec):
        return vec/np.linalg.norm(vec)
    return np.zeros(2)
