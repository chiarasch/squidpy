import pytest
import numpy as np
import rasterio.errors
import warnings

from spatial_tools.image.segment import segment
from spatial_tools.image.object import ImageContainer

@pytest.mark.parametrize("shape", [(3,100,200)])


def test_segmentation_blob(shape):
    """\
    Test skimage blob detection.
    """
    import tifffile
    # ignore NotGeoreferencedWarning here
    warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)
    img_orig = np.zerost(shape, dtype=np.uint8)
    # Add blobs
    img_orig[:, :4, :4] = 1.
    img_orig[:, 30:34, 10:16] = 1.

    cont = ImageContainer(img_orig, img_id='image_0')
    segment(img=cont, model_group="skimage_blob", model_instance="log", img_id='image_0', key_added="segment")
    # Check that blobs are in segments:
    assert np.all(cont["segment"][img_orig > 0] > 0)