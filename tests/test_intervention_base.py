import interfere
import numpy as np


def test_add_gaussian_noise():
    X = np.zeros((10_000, 3))

    seed = 12
    rng = np.random.default_rng(seed)

    stdevs = np.array([0.01, 1.0, 10])
    Xnoise = interfere.add_gaussian_noise(X, stdevs, rng)

    # Check that the standard deviations are correct.
    assert np.allclose(np.std(Xnoise, axis=0), stdevs, atol=0.1)

    rng = np.random.default_rng(seed)
    Xnoise2 = interfere.add_gaussian_noise(X, stdevs, rng)

    # Check that the range gives control over the randomness.
    assert np.all(Xnoise == Xnoise2)

    # Check the default standard deviations.
    Xnoise_default_std = interfere.add_gaussian_noise(X)
    assert np.allclose(np.std(Xnoise_default_std, axis=0), np.ones(3), atol=0.1)