import scipy as sp
import scipy.ndimage as spim
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def show_3D(im):
    r"""
    Rotates a 3D image and creates an angled view for rough 2D visualization.

    Because it rotates the image it can be slow for large image, so is
    mostly meant for rough checking of small prototype images.

    Parameters
    ----------
    im : 3D-array
        The 3D array to be viewed from an angle

    Returns
    -------
    image : 2D-array
        A 2D veiw of the given 3D image

    Notes
    -----
    This function assumes that the image contains ``True`` for void space and
    so inverts the image to show the solid material.

    """
    im = ~sp.copy(im)
    if im.ndim < 3:
        raise Exception('show_3D only applies to 3D images')
    im = spim.rotate(input=im, angle=22.5, axes=[0, 1], order=0)
    im = spim.rotate(input=im, angle=45, axes=[2, 1], order=0)
    im = spim.rotate(input=im, angle=-17, axes=[0, 1], order=0, reshape=False)
    mask = im != 0
    view = sp.where(mask.any(axis=2), mask.argmax(axis=2), 0)
    view = view.max() - view
    f = view.max()/5
    view[view == view.max()] = -f
    view = (view + f)**2
    return view


def show_planes(im):
    r"""
    Create a quick montage showing a 3D image in all three directions

    Parameters
    ----------
    im : ND-array
        A 3D image of the porous material

    Returns
    -------
    image : ND-array
        A 2D array containing the views.  This single image can be viewed using
        ``matplotlib.pyplot.imshow``.

    """
    if sp.squeeze(im.ndim) < 3:
        raise Exception('This view is only necessary for 3D images')
    x, y, z = (sp.array(im.shape)/2).astype(int)
    im_xy = im[:, :, z]
    im_xz = im[:, y, :]
    im_yz = sp.rot90(im[x, :, :])

    new_x = im_xy.shape[0] + im_yz.shape[0] + 10

    new_y = im_xy.shape[1] + im_xz.shape[1] + 10

    new_im = sp.zeros([new_x + 20, new_y + 20], dtype=im.dtype)

    # Add xy image to upper left corner
    new_im[10:im_xy.shape[0]+10,
           10:im_xy.shape[1]+10] = im_xy
    # Add xz image to lower left coner
    x_off = im_xy.shape[0]+20
    y_off = im_xy.shape[1]+20
    new_im[10:10 + im_xz.shape[0],
           y_off:y_off + im_xz.shape[1]] = im_xz
    new_im[x_off:x_off + im_yz.shape[0],
           10:10 + im_yz.shape[1]] = im_yz

    return new_im


def sem(im, direction='X'):
    r"""
    Simulates an SEM photograph looking into the porous material in the
    specified direction.  Features are colored according to their depth into
    the image, so darker features are further away.

    Parameters
    ----------
    im : array_like
        ND-image of the porous material with the solid phase marked as 1 or
        True

    direction : string
        Specify the axis along which the camera will point.  Options are
        'X', 'Y', and 'Z'.

    Returns
    -------
    image : 2D-array
        A 2D greyscale image suitable for use in matplotlib\'s ```imshow```
        function.
    """
    im = sp.array(~im, dtype=int)
    if direction in ['Y', 'y']:
        im = sp.transpose(im, axes=[1, 0, 2])
    if direction in ['Z', 'z']:
        im = sp.transpose(im, axes=[2, 1, 0])
    t = im.shape[0]
    depth = sp.reshape(sp.arange(0, t), [t, 1, 1])
    im = im*depth
    im = sp.amax(im, axis=0)
    return im


def xray(im, direction='X'):
    r"""
    Simulates an X-ray radiograph looking through the porouls material in the
    specfied direction.  The resulting image is colored according to the amount
    of attenuation an X-ray would experience, so regions with more solid will
    appear darker.

    Parameters
    ----------
    im : array_like
        ND-image of the porous material with the solid phase marked as 1 or
        True

    direction : string
        Specify the axis along which the camera will point.  Options are
        'X', 'Y', and 'Z'.

    Returns
    -------
    image : 2D-array
        A 2D greyscale image suitable for use in matplotlib\'s ```imshow```
        function.
    """
    im = sp.array(~im, dtype=int)
    if direction in ['Y', 'y']:
        im = sp.transpose(im, axes=[1, 0, 2])
    if direction in ['Z', 'z']:
        im = sp.transpose(im, axes=[2, 1, 0])
    im = sp.sum(im, axis=0)
    return im
