# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#       authors:
#         Jerome Carnis, jerome.carnis@esrf.fr

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from scipy.ndimage.measurements import center_of_mass
from scipy.interpolate import RegularGridInterpolator
import xrayutilities as xu
import fabio
import os
import gc
import sys
sys.path.append('//win.desy.de/home/carnisj/My Documents/myscripts/bcdi/')
import bcdi.graph.graph_utils as gu
from bcdi.utils import image_registration as reg



def align_diffpattern(reference_data, data, mask, method='registration', combining_method='rgi'):
    """
    Align two diffraction patterns based on the shift of the center of mass or based on dft registration.

    :param reference_data: the first 3D diffraction intensity array which will serve as a reference.
    :param data: the 3D diffraction intensity array to align.
    :param mask: the 3D mask corresponding to data
    :param method: 'center_of_mass' or 'registration'. For 'registration', see: Opt. Lett. 33, 156-158 (2008).
    :param combining_method: 'rgi' for RegularGridInterpolator or 'subpixel' for subpixel shift
    :return:
     - the shifted data
     - the shifted mask
    """
    if reference_data.ndim != 3:
        raise ValueError('Expect 3D arrays as input')
    nbz, nby, nbx = reference_data.shape
    if reference_data.shape != data.shape:
        raise ValueError('reference_data and data do not have the same shape')

    if method is 'registration':
        shiftz, shifty, shiftx = reg.getimageregistration(abs(reference_data), abs(data), precision=10)
    elif method is 'center_of_mass':
        ref_piz, ref_piy, ref_pix = center_of_mass(abs(reference_data))
        piz, piy, pix = center_of_mass(abs(data))
        shiftz = ref_piz - piz
        shifty = ref_piy - piy
        shiftx = ref_pix - pix
    else:
        raise ValueError("Incorrect value for parameter 'method'")

    print('z shift', str('{:.2f}'.format(shiftz)), ', y shift',
          str('{:.2f}'.format(shifty)), ', x shift', str('{:.2f}'.format(shiftx)))
    if (shiftz == 0) and (shifty == 0) and (shiftx == 0):
        return data, mask

    if combining_method is 'rgi':
        # re-sample data on a new grid based on the shift
        old_z = np.arange(-nbz // 2, nbz // 2)
        old_y = np.arange(-nby // 2, nby // 2)
        old_x = np.arange(-nbx // 2, nbx // 2)
        myz, myy, myx = np.meshgrid(old_z, old_y, old_x, indexing='ij')
        new_z = myz + shiftz
        new_y = myy + shifty
        new_x = myx + shiftx
        del myx, myy, myz
        rgi = RegularGridInterpolator((old_z, old_y, old_x), data, method='linear', bounds_error=False,
                                      fill_value=0)
        data = rgi(np.concatenate((new_z.reshape((1, new_z.size)), new_y.reshape((1, new_z.size)),
                                   new_x.reshape((1, new_z.size)))).transpose())
        data = data.reshape((nbz, nby, nbx)).astype(reference_data.dtype)
        rgi = RegularGridInterpolator((old_z, old_y, old_x), mask, method='linear', bounds_error=False,
                                      fill_value=0)
        mask = rgi(np.concatenate((new_z.reshape((1, new_z.size)), new_y.reshape((1, new_z.size)),
                                   new_x.reshape((1, new_z.size)))).transpose())
        mask = mask.reshape((nbz, nby, nbx)).astype(data.dtype)
        mask = np.rint(mask)  # mask is integer 0 or 1

    elif combining_method is 'subpixel':
        data = abs(reg.subpixel_shift(data, shiftz, shifty, shiftx))  # data is a real number (intensity)
        mask = np.rint(abs(reg.subpixel_shift(mask, shiftz, shifty, shiftx)))  # mask is integer 0 or 1
    else:
        raise ValueError("Incorrect value for parameter 'combining_method'")

    return data, mask


def center_fft(data, mask, frames_logical, centering='max', fft_option='crop_asymmetric_ZYX', **kwargs):
    """
    Center and crop/pad the dataset depending on user parameters

    :param data: the 3D data array
    :param mask: the 3D mask array
    :param frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
     A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.
    :param centering: centering option, 'max' or 'com'. It will be overridden if the kwarg 'fix_bragg' is provided.
    :param fft_option:
     - 'crop_sym_ZYX': crop the array for FFT requirements, Bragg peak centered
     - 'crop_asym_ZYX': crop the array for FFT requirements without centering the Brag peak
     - 'pad_sym_Z_crop_sym_YX': crop detector images (Bragg peak centered) and pad the rocking angle based on
       'pad_size' (Bragg peak centered)
     - 'pad_sym_Z_crop_asym_YX': pad rocking angle based on 'pad_size' (Bragg peak centered) and crop detector
       (Bragg peak non-centered)
     - 'pad_asym_Z_crop_sym_YX': crop detector images (Bragg peak centered), pad the rocking angle
       without centering the Brag peak
     - 'pad_asym_Z_crop_asym_YX': pad rocking angle and crop detector without centering the Bragg peak
     - 'pad_sym_Z': keep detector size and pad/center the rocking angle based on 'pad_size', Bragg peak centered
     - 'pad_asym_Z': keep detector size and pad the rocking angle without centering the Brag peak
     - 'pad_sym_ZYX': pad all dimensions based on 'pad_size', Brag peak centered
     - 'pad_asym_ZYX': pad all dimensions based on 'pad_size' without centering the Brag peak
     - 'do_nothing': keep the full dataset or crop it to the size defined by fix_size
    :param kwargs:
     - 'fix_bragg' = user-defined position in pixels of the Bragg peak [z_bragg, y_bragg, x_bragg]
     - 'fix_size' = user defined output array size [zstart, zstop, ystart, ystop, xstart, xstop]
     - 'pad_size' = user defined output array size [nbz, nby, nbx]
     - 'q_values' = [qx, qz, qy], each component being a 1D array
    :return:
     - updated data, mask (and q_values if provided, [] otherwise)
     - pad_width = [z0, z1, y0, y1, x0, x1] number of pixels added at each end of the original data
     - updated frames_logical
    """
    if data.ndim != 3 or mask.ndim != 3:
        raise ValueError('data and mask should be 3D arrays')

    if data.shape != mask.shape:
        raise ValueError('Data and mask must have the same shape\n data is ', data.shape, ' while mask is ', mask.shape)

    for k in kwargs.keys():
        if k in ['fix_bragg']:
            fix_bragg = kwargs['fix_bragg']
        elif k in ['fix_size']:
            fix_size = kwargs['fix_size']
        elif k in ['pad_size']:
            pad_size = kwargs['pad_size']
        elif k in ['q_values']:
            q_values = kwargs['q_values']
        else:
            raise Exception("unknown keyword argument given: allowed is"
                            "'fix_bragg', 'fix_size', 'pad_size' and 'q_values'")
    try:
        fix_bragg
    except NameError:  # fix_bragg not declared
        fix_bragg = []
    try:
        fix_size
    except NameError:  # fix_size not declared
        fix_size = []
    try:
        pad_size
    except NameError:  # pad_size not declared
        pad_size = []
    try:
        q_values
        qx = q_values[0]  # axis=0, z downstream, qx in reciprocal space
        qz = q_values[1]  # axis=1, y vertical, qz in reciprocal space
        qy = q_values[2]  # axis=2, x outboard, qy in reciprocal space
    except NameError:  # q_values not declared
        q_values = []
        qx = []
        qy = []
        qz = []
    except IndexError:  # q_values empty
        q_values = []
        qx = []
        qy = []
        qz = []

    if centering == 'max':
        z0, y0, x0 = np.unravel_index(abs(data).argmax(), data.shape)
        print("Max at (qx, qz, qy): ", z0, y0, x0)
    elif centering == 'com':
        z0, y0, x0 = center_of_mass(data)
        print("Center of mass at (qx, qz, qy): ", z0, y0, x0)
    else:
        raise ValueError("Incorrect value for 'centering' parameter")

    if len(fix_bragg) != 0:
        if len(fix_bragg) != 3:
            raise ValueError('fix_bragg should be a list of 3 integers')
        z0, y0, x0 = fix_bragg
        print("Bragg peak position defined by user at (qx, qz, qy): ", z0, y0, x0)

    iz0, iy0, ix0 = int(round(z0)), int(round(y0)), int(round(x0))
    print('data at Bragg peak = ', data[iz0, iy0, ix0])

    # Max symmetrical box around center of mass
    nbz, nby, nbx = np.shape(data)
    max_nz = abs(2 * min(iz0, nbz - iz0))
    max_ny = 2 * min(iy0, nby - iy0)
    max_nx = abs(2 * min(ix0, nbx - ix0))
    print("Max symmetrical box (qx, qz, qy): ", max_nz, max_ny, max_nx)
    if max_nz == 0 or max_ny == 0 or max_nx == 0:
        print('Images with no intensity!')
        fft_option = 'do_nothing'

    # Crop/pad data to fulfill FFT size and user requirements
    if fft_option == 'crop_sym_ZYX':
        # crop rocking angle and detector, Bragg peak centered
        nz1, ny1, nx1 = smaller_primes((max_nz, max_ny, max_nx), maxprime=7, required_dividers=(2,))
        pad_width = np.zeros(6, dtype=int)

        data = data[iz0 - nz1 // 2:iz0 + nz1//2, iy0 - ny1//2:iy0 + ny1//2, ix0 - nx1//2:ix0 + nx1//2]
        mask = mask[iz0 - nz1 // 2:iz0 + nz1//2, iy0 - ny1//2:iy0 + ny1//2, ix0 - nx1//2:ix0 + nx1//2]
        print("FFT box (qx, qz, qy): ", data.shape)

        if (iz0 - nz1//2) > 0:  # if 0, the first frame is used
            frames_logical[0:iz0 - nz1 // 2] = 0
        if (iz0 + nz1 // 2) < nbz:  # if nbz, the last frame is used
            frames_logical[iz0 + nz1 // 2:] = 0

        if len(q_values) != 0:
            qx = qx[iz0 - nz1//2:iz0 + nz1//2]
            qy = qy[ix0 - nx1//2:ix0 + nx1//2]
            qz = qz[iy0 - ny1//2:iy0 + ny1//2]

    elif fft_option == 'crop_asym_ZYX':
        # crop rocking angle and detector without centering the Bragg peak
        nz1, ny1, nx1 = smaller_primes((nbz, nby, nbx), maxprime=7, required_dividers=(2,))
        pad_width = np.zeros(6, dtype=int)

        data = data[nbz//2 - nz1//2:nbz//2 + nz1//2, nby//2 - ny1//2:nby//2 + ny1//2,
                    nbx//2 - nx1//2:nbx//2 + nx1//2]
        mask = mask[nbz//2 - nz1//2:nbz//2 + nz1//2, nby//2 - ny1//2:nby//2 + ny1//2,
                    nbx//2 - nx1//2:nbx//2 + nx1//2]
        print("FFT box (qx, qz, qy): ", data.shape)

        if (nbz//2 - nz1//2) > 0:  # if 0, the first frame is used
            frames_logical[0:nbz//2 - nz1//2] = 0
        if (nbz//2 + nz1//2) < nbz:  # if nbz, the last frame is used
            frames_logical[nbz//2 + nz1 // 2:] = 0

        if len(q_values) != 0:
            qx = qx[nbz//2 - nz1//2:nbz//2 + nz1//2]
            qy = qy[nbx//2 - nx1//2:nbx//2 + nx1//2]
            qz = qz[nby//2 - ny1//2:nby//2 + ny1//2]

    elif fft_option == 'pad_sym_Z_crop_sym_YX':
        # pad rocking angle based on 'pad_size' (Bragg peak centered) and crop detector (Bragg peak centered)
        if len(pad_size) != 3:
            raise ValueError('pad_size should be a list of three elements')
        if pad_size[0] != higher_primes(pad_size[0], maxprime=7, required_dividers=(2,)):
            raise ValueError(pad_size[0], 'does not meet FFT requirements')
        ny1, nx1 = smaller_primes((max_ny, max_nx), maxprime=7, required_dividers=(2,))

        data = data[:, iy0 - ny1//2:iy0 + ny1//2, ix0 - nx1//2:ix0 + nx1//2]
        mask = mask[:, iy0 - ny1//2:iy0 + ny1//2, ix0 - nx1//2:ix0 + nx1//2]
        pad_width = np.array([int(min(pad_size[0]/2-iz0, pad_size[0]-nbz)),
                              int(min(pad_size[0]/2-nbz + iz0, pad_size[0]-nbz)),
                              0, 0, 0, 0], dtype=int)
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(mask, padding_width=pad_width, mask_flag=True)  # mask padded pixels
        print("FFT box (qx, qz, qy): ", data.shape)

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0]:pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(pad_size[0])*dqx
            qy = qy[ix0 - nx1 // 2:ix0 + nx1 // 2]
            qz = qz[iy0 - ny1 // 2:iy0 + ny1 // 2]

    elif fft_option == 'pad_sym_Z_crop_asym_YX':
        # pad rocking angle based on 'pad_size' (Bragg peak centered) and crop detector (Bragg peak non-centered)
        if len(pad_size) != 3:
            raise ValueError('pad_size should be a list of three elements')
        if pad_size[0] != higher_primes(pad_size[0], maxprime=7, required_dividers=(2,)):
            raise ValueError(pad_size[0], 'does not meet FFT requirements')
        ny1, nx1 = smaller_primes((max_ny, max_nx), maxprime=7, required_dividers=(2,))

        data = data[:, nby//2 - ny1//2:nby//2 + ny1//2, nbx//2 - nx1//2:nbx//2 + nx1//2]
        mask = mask[:, nby//2 - ny1//2:nby//2 + ny1//2, nbx//2 - nx1//2:nbx//2 + nx1//2]
        pad_width = np.array([int(min(pad_size[0]/2-iz0, pad_size[0]-nbz)),
                              int(min(pad_size[0]/2-nbz + iz0, pad_size[0]-nbz)),
                              0, 0, 0, 0], dtype=int)
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(mask, padding_width=pad_width, mask_flag=True)  # mask padded pixels
        print("FFT box (qx, qz, qy): ", data.shape)

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0]:pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(pad_size[0])*dqx
            qy = qy[nbx//2 - nx1//2:nbx//2 + nx1//2]
            qz = qz[nby//2 - ny1//2:nby//2 + ny1//2]

    elif fft_option == 'pad_asym_Z_crop_sym_YX':
        # pad rocking angle without centering the Bragg peak and crop detector (Bragg peak centered)
        ny1, nx1 = smaller_primes((max_ny, max_nx), maxprime=7, required_dividers=(2,))
        nz1 = higher_primes(nbz, maxprime=7, required_dividers=(2,))

        data = data[:, iy0 - ny1//2:iy0 + ny1//2, ix0 - nx1//2:ix0 + nx1//2]
        mask = mask[:, iy0 - ny1//2:iy0 + ny1//2, ix0 - nx1//2:ix0 + nx1//2]
        pad_width = np.array([int((nz1 - nbz + ((nz1 - nbz) % 2)) / 2), int((nz1 - nbz + 1) / 2 - ((nz1 - nbz) % 2)),
                              0, 0, 0, 0], dtype=int)
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(mask, padding_width=pad_width, mask_flag=True)  # mask padded pixels
        print("FFT box (qx, qz, qy): ", data.shape)

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0]:pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(nz1)*dqx
            qy = qy[ix0 - nx1 // 2:ix0 + nx1 // 2]
            qz = qz[iy0 - ny1 // 2:iy0 + ny1 // 2]

    elif fft_option == 'pad_asym_Z_crop_asym_YX':
        # pad rocking angle and crop detector without centering the Bragg peak
        ny1, nx1 = smaller_primes((nby, nbx), maxprime=7, required_dividers=(2,))
        nz1 = higher_primes(nbz, maxprime=7, required_dividers=(2,))

        data = data[:, nby//2 - ny1//2:nby//2 + ny1//2, nbx//2 - nx1//2:nbx//2 + nx1//2]
        mask = mask[:, nby//2 - ny1//2:nby//2 + ny1//2, nbx//2 - nx1//2:nbx//2 + nx1//2]
        pad_width = np.array([int((nz1 - nbz + ((nz1 - nbz) % 2)) / 2), int((nz1 - nbz + 1) / 2 - ((nz1 - nbz) % 2)),
                              0, 0, 0, 0], dtype=int)
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(mask, padding_width=pad_width, mask_flag=True)  # mask padded pixels
        print("FFT box (qx, qz, qy): ", data.shape)

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0]:pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(nz1)*dqx
            qy = qy[nbx//2 - nx1//2:nbx//2 + nx1//2]
            qz = qz[nby//2 - ny1//2:nby//2 + ny1//2]

    elif fft_option == 'pad_sym_Z':
        # pad rocking angle based on 'pad_size'(Bragg peak centered) and keep detector size
        if len(pad_size) != 3:
            raise ValueError('pad_size should be a list of three elements')
        if pad_size[0] != higher_primes(pad_size[0], maxprime=7, required_dividers=(2,)):
            raise ValueError(pad_size[0], 'does not meet FFT requirements')

        pad_width = np.array([int(min(pad_size[0]/2-iz0, pad_size[0]-nbz)),
                              int(min(pad_size[0]/2-nbz + iz0, pad_size[0]-nbz)),
                              0, 0, 0, 0], dtype=int)
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(mask, padding_width=pad_width, mask_flag=True)  # mask padded pixels
        print("FFT box (qx, qz, qy): ", data.shape)

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0]:pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(pad_size[0])*dqx

    elif fft_option == 'pad_asym_Z':
        # pad rocking angle without centering the Bragg peak, keep detector size
        nz1 = higher_primes(nbz, maxprime=7, required_dividers=(2,))

        pad_width = np.array([int((nz1-nbz+((nz1-nbz) % 2))/2), int((nz1-nbz+1)/2-((nz1-nbz) % 2)),
                              0, 0, 0, 0], dtype=int)
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(mask, padding_width=pad_width, mask_flag=True)  # mask padded pixels
        print("FFT box (qx, qz, qy): ", data.shape)

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0]:pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(nz1)*dqx

    elif fft_option == 'pad_sym_ZYX':
        # pad both dimensions based on 'pad_size' (Bragg peak centered)
        if len(pad_size) != 3:
            raise ValueError('pad_size should be a list of 3 integers')
        if pad_size[0] != higher_primes(pad_size[0], maxprime=7, required_dividers=(2,)):
            raise ValueError(pad_size[0], 'does not meet FFT requirements')
        if pad_size[1] != higher_primes(pad_size[1], maxprime=7, required_dividers=(2,)):
            raise ValueError(pad_size[1], 'does not meet FFT requirements')
        if pad_size[2] != higher_primes(pad_size[2], maxprime=7, required_dividers=(2,)):
            raise ValueError(pad_size[2], 'does not meet FFT requirements')

        pad_width = [int(min(pad_size[0]/2-iz0, pad_size[0]-nbz)), int(min(pad_size[0]/2-nbz + iz0, pad_size[0]-nbz)),
                     int(min(pad_size[1]/2-iy0, pad_size[1]-nby)), int(min(pad_size[1]/2-nby + iy0, pad_size[1]-nby)),
                     int(min(pad_size[2]/2-ix0, pad_size[2]-nbx)), int(min(pad_size[2]/2-nbx + ix0, pad_size[2]-nbx))]
        pad_width = np.array(list((map(lambda value: max(value, 0), pad_width))), dtype=int)  # remove negative numbers
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(mask, padding_width=pad_width, mask_flag=True)  # mask padded pixels
        print("FFT box (qx, qz, qy): ", data.shape)

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0]:pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            dqy = qy[1] - qy[0]
            dqz = qz[1] - qz[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qy0 = qy[0] - pad_width[2] * dqy
            qz0 = qz[0] - pad_width[1] * dqz
            qx = qx0 + np.arange(pad_size[0]) * dqx
            qy = qy0 + np.arange(pad_size[2]) * dqy
            qz = qz0 + np.arange(pad_size[1]) * dqz

    elif fft_option == 'pad_asym_ZYX':
        # pad both dimensions without centering the Bragg peak
        nz1, ny1, nx1 = [higher_primes(nbz, maxprime=7, required_dividers=(2,)),
                         higher_primes(nby, maxprime=7, required_dividers=(2,)),
                         higher_primes(nbx, maxprime=7, required_dividers=(2,))]

        pad_width = np.array(
            [int((nz1-nbz+((nz1-nbz) % 2))/2), int((nz1-nbz+1)/2-((nz1-nbz) % 2)),
             int((ny1-nby+((pad_size[1]-nby) % 2))/2), int((ny1-nby+1)/2-((ny1-nby) % 2)),
             int((nx1-nbx+((nx1-nbx) % 2))/2), int((nx1-nbx+1)/2-((nx1-nbx) % 2))])
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(mask, padding_width=pad_width, mask_flag=True)  # mask padded pixels

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0]:pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            dqy = qy[1] - qy[0]
            dqz = qz[1] - qz[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qy0 = qy[0] - pad_width[2] * dqy
            qz0 = qz[0] - pad_width[1] * dqz
            qx = qx0 + np.arange(nz1) * dqx
            qy = qy0 + np.arange(nx1) * dqy
            qz = qz0 + np.arange(ny1) * dqz

    elif fft_option == 'do_nothing':
        # keep the full dataset or use 'fix_size' parameter
        pad_width = np.zeros(6, dtype=int)  # do nothing or crop the data, starting_frame should be 0
        if len(fix_size) == 6:
            # size of output array defined
            nbz, nby, nbx = np.shape(data)
            z_pan = fix_size[1] - fix_size[0]
            y_pan = fix_size[3] - fix_size[2]
            x_pan = fix_size[5] - fix_size[4]
            if z_pan > nbz or y_pan > nby or x_pan > nbx or fix_size[1] > nbz or fix_size[3] > nby or fix_size[5] > nbx:
                raise ValueError("Predefined fix_size uncorrect")
            else:
                data = data[fix_size[0]:fix_size[1], fix_size[2]:fix_size[3], fix_size[4]:fix_size[5]]
                mask = mask[fix_size[0]:fix_size[1], fix_size[2]:fix_size[3], fix_size[4]:fix_size[5]]

                if fix_size[0] > 0:  # if 0, the first frame is used
                    frames_logical[0:fix_size[0]] = 0
                if fix_size[1] < nbz:  # if nbz, the last frame is used
                    frames_logical[fix_size[1]:] = 0

                if len(q_values) != 0:
                    qx = qx[fix_size[0]:fix_size[1]]
                    qy = qy[fix_size[4]:fix_size[5]]
                    qz = qz[fix_size[2]:fix_size[3]]
    else:
        raise ValueError("Incorrect value for 'fft_option'")

    if len(q_values) != 0:
        q_values[0] = qx
        q_values[1] = qz
        q_values[2] = qy
    return data, mask, pad_width, q_values, frames_logical


def check_pixels(data, mask, debugging=False):
    """
    Check for hot pixels in the data using the mean value and the variance.

    :param data: 3D diffraction data
    :param mask: 2D or 3D mask. Mask will summed along the first axis if a 3D array.
    :param debugging: set to True to see plots
    :type debugging: bool
    :return: the filtered 3D data and the updated 2D mask.
    """
    if data.ndim != 3:
        raise ValueError('Data should be a 3D array')

    nbz, nby, nbx = data.shape

    if mask.ndim == 3:  # 3D array
        print("Mask is a 3D array, summing it along axis 0")
        mask = mask.sum(axis=0)
        mask[np.nonzero(mask)] = 1

    if data[0, :, :].shape != mask.shape:
        raise ValueError('Data and mask must have the same shape\n data slice is ',
                         data[0, :, :].shape, ' while mask is ', mask.shape)

    meandata = data.mean(axis=0)  # 2D
    vardata = 1 / data.var(axis=0)  # 2D
    var_mean = vardata[vardata != np.inf].mean()
    vardata[meandata == 0] = var_mean  # pixels were data=0 (hence 1/variance=inf) are set to the mean of 1/var
    if debugging:
        gu.combined_plots(tuple_array=(meandata, vardata), tuple_sum_frames=(False, False), tuple_sum_axis=(0, 0),
                          tuple_width_v=(np.nan, np.nan), tuple_width_h=(np.nan, np.nan), tuple_colorbar=(True, True),
                          tuple_vmin=(0, 0), tuple_vmax=(1, np.nan), tuple_scale=('linear', 'linear'),
                          tuple_title=('mean(data) before masking', '1/var(data) before masking'),
                          reciprocal_space=True)
    # calculate the mean and 1/variance for a single photon event along the rocking curve
    min_count = 0.99  # pixels with only 1 photon count along the rocking curve.

    mean_threshold = min_count / nbz
    var_threshold = ((nbz - 1) * mean_threshold ** 2 + (min_count - mean_threshold) ** 2) * 1 / nbz

    temp_mask = np.zeros((nby, nbx))
    temp_mask[vardata == np.inf] = 1  # this includes hotpixels but also zero intensity pixels
    #  along the whole rocking curve
    temp_mask[data.mean(axis=0) == 0] = 0  # remove zero intensity pixels from the mask

    vardata[vardata == np.inf] = 0
    indices_badpixels = np.nonzero(vardata > 1 / var_threshold)
    mask[indices_badpixels] = 1  # mask is 2D
    mask[np.nonzero(temp_mask)] = 1  # update mask

    indices_badpixels = np.nonzero(mask)  # update indices
    for index in range(nbz):
        tempdata = data[index, :, :]
        tempdata[indices_badpixels] = 0  # numpy array is mutable hence data will be modified

    if debugging:
        meandata = data.mean(axis=0)
        vardata = 1 / data.var(axis=0)
        gu.combined_plots(tuple_array=(meandata, vardata), tuple_sum_frames=(False, False), tuple_sum_axis=(0, 0),
                          tuple_width_v=(np.nan, np.nan), tuple_width_h=(np.nan, np.nan), tuple_colorbar=(True, True),
                          tuple_vmin=(0, 0), tuple_vmax=(1, np.nan), tuple_scale=('linear', 'linear'),
                          tuple_title=('mean(data) after masking', '1/var(data) after masking'), reciprocal_space=True)
    print("check_pixels():", str(indices_badpixels[0].shape[0]), "badpixels were masked on a total of", str(nbx * nby))
    return data, mask


def create_logfile(beamline, detector, scan_number, root_folder, filename):
    """
    Create the logfile used in gridmap().

    :param beamline: 'ID01' or 'SIXS' or 'CRISTAL' or 'P10'
    :param detector: the detector object: Class experiment_utils.Detector()
    :param scan_number: the scan number to load
    :param root_folder: the root directory of the experiment, where is the specfile/.fio file
    :param filename: the file name to load, or the path of 'alias_dict.txt' for SIXS
    :return: logfile
    """
    if beamline == 'CRISTAL':  # no specfile, load directly the dataset
        import h5py
        ccdfiletmp = os.path.join(detector.datadir + detector.template_imagefile % scan_number)
        logfile = h5py.File(ccdfiletmp, 'r')

    elif beamline == 'P10':  # load .fio file
        logfile = root_folder + filename + '\\' + filename + '.fio'

    elif beamline == 'SIXS_2018':  # no specfile, load directly the dataset
        import bcdi.preprocessing.nxsReady as nxsReady

        logfile = nxsReady.DataSet(longname=detector.datadir + detector.template_imagefile % scan_number,
                                   shortname=detector.template_imagefile % scan_number, alias_dict=filename,
                                   scan="SBS")
    elif beamline == 'SIXS_2019':  # no specfile, load directly the dataset
        import bcdi.preprocessing.ReadNxs3 as ReadNxs3

        logfile = ReadNxs3.DataSet(directory=detector.datadir, filename=detector.template_imagefile % scan_number,alias_dict=filename)

    elif beamline == 'ID01':  # load spec file
        from silx.io.specfile import SpecFile
        logfile = SpecFile(root_folder + filename + '.spec')
    else:
        raise ValueError('Incorrect value for beamline parameter')

    return logfile


def find_bragg(data, peak_method):
    """
    Find the Bragg peak position in data based on the centering method.

    :param data: 2D or 3D array. If complex, Bragg peak position is calculated for abs(array)
    :param peak_method: 'max', 'com' or 'maxcom'. For 'maxcom', it uses method 'max' for the first axis and 'com'
     for the other axes.
    :return: the centered data
    """
    if peak_method != 'max' and peak_method != 'com' and peak_method != 'maxcom':
        raise ValueError('Incorrect value for "centering_method" parameter')

    if data.ndim == 2:
        z0 = 0
        if peak_method == 'max':
            y0, x0 = np.unravel_index(abs(data).argmax(), data.shape)
            print("Max at (y, x): ", y0, x0, ' Max = ', int(data[y0, x0]))
        else:  # 'com'
            y0, x0 = center_of_mass(data)
            print("Center of mass at (y, x): ", y0, x0, ' COM = ', int(data[int(y0), int(x0)]))
    elif data.ndim == 3:
        if peak_method == 'max':
            z0, y0, x0 = np.unravel_index(abs(data).argmax(), data.shape)
            print("Max at (z, y, x): ", z0, y0, x0, ' Max = ', int(data[z0, y0, x0]))
        elif peak_method == 'com':
            z0, y0, x0 = center_of_mass(data)
            print("Center of mass at (z, y, x): ", z0, y0, x0, ' COM = ', int(data[int(z0), int(y0), int(x0)]))
        else:
            z0, _, _ = np.unravel_index(abs(data).argmax(), data.shape)
            y0, x0 = center_of_mass(data[z0, :, :])
            print("MaxCom at (z, y, x): ", z0, y0, x0, ' Max = ', int(data[int(z0), int(y0), int(x0)]))
    else:
        raise ValueError('Data should be 2D or 3D')

    return z0, y0, x0


def grid_cdi(data, mask, setup):
    """

    :param data: the 3D data
    :param mask: the corresponding 3D mask
    :param setup: the experimental setup: Class SetupPreprocessing()
    :return: the data and mask interpolated in the laboratory frame
    """
    if data.ndim != 3:
        raise ValueError('data is expected to be a 3D array')
    if mask.ndim != 3:
        raise ValueError('mask is expected to be a 3D array')
    nbz, nby, nbx = data.shape
    rocking_angle = setup.rocking_angle
    angular_step = setup.angular_step * np.pi / 180  # switch to radians
    rotation_matrix = np.zeros((3, 3))
    myz, myy, myx = np.meshgrid(np.arange(-nbz // 2, nbz // 2, 1),
                                np.arange(-nby // 2, nby // 2, 1),
                                np.arange(-nbx // 2, nbx // 2, 1), indexing='ij')
    new_x = np.zeros(data.shape)
    new_y = np.zeros(data.shape)
    new_z = np.zeros(data.shape)
    frames = np.arange(-nbz//2, nbz//2)
    for idx in range(len(frames)):
        angle = frames[idx] * angular_step
        if rocking_angle == 'inplane':
            rotation_matrix[:, 0] = np.array([np.cos(angle), 0, -np.sin(angle)])  # x
            rotation_matrix[:, 1] = np.array([0, 1, 0])                                         # y
            rotation_matrix[:, 2] = np.array([np.sin(angle), 0, np.cos(angle)])   # z
        elif rocking_angle == 'outofplane':
            rotation_matrix[:, 0] = np.array([1, 0, 0])                                         # x
            rotation_matrix[:, 1] = np.array([0, np.cos(angle), np.sin(angle)])   # y
            rotation_matrix[:, 2] = np.array([0, -np.sin(angle), np.cos(angle)])  # z
        else:
            raise ValueError('Wrong value for "rotation_angle" parameter')

        rotation_imatrix = np.linalg.inv(rotation_matrix)
        new_x[idx, :, :] = rotation_imatrix[0, 0] * myx[idx, :, :] + rotation_imatrix[0, 1] * myy[idx, :, :] +\
                           rotation_imatrix[0, 2] * myz[idx, :, :]
        new_y[idx, :, :] = rotation_imatrix[1, 0] * myx[idx, :, :] + rotation_imatrix[1, 1] * myy[idx, :, :] +\
                           rotation_imatrix[1, 2] * myz[idx, :, :]
        new_z[idx, :, :] = rotation_imatrix[2, 0] * myx[idx, :, :] + rotation_imatrix[2, 1] * myy[idx, :, :] +\
                           rotation_imatrix[2, 2] * myz[idx, :, :]
    del myx, myy, myz
    gc.collect()

    rgi = RegularGridInterpolator((np.arange(-nbz // 2, nbz // 2), np.arange(-nby // 2, nby // 2),
                                   np.arange(-nbx // 2, nbx // 2)), data, method='linear',
                                  bounds_error=False, fill_value=0)
    newdata = rgi(np.concatenate((new_z.reshape((1, new_z.size)), new_y.reshape((1, new_z.size)),
                                  new_x.reshape((1, new_z.size)))).transpose())
    newdata = newdata.reshape((nbz, nby, nbx)).astype(data.dtype)

    rgi = RegularGridInterpolator((np.arange(-nbz // 2, nbz // 2), np.arange(-nby // 2, nby // 2),
                                   np.arange(-nbx // 2, nbx // 2)), data, method='linear',
                                  bounds_error=False, fill_value=0)
    newmask = rgi(np.concatenate((new_z.reshape((1, new_z.size)), new_y.reshape((1, new_z.size)),
                                  new_x.reshape((1, new_z.size)))).transpose())
    newmask = newmask.reshape((nbz, nby, nbx)).astype(mask.dtype)
    newmask[np.nonzero(newmask)] = 1

    return newdata, newmask


def gridmap(logfile, scan_number, detector, setup, flatfield=None, hotpixels=None, orthogonalize=False, hxrd=None,
            regrid_cdi=False, debugging=False, **kwargs):
    """
    Load the data, apply filters and concatenate it for phasing.

    :param logfile: file containing the information about the scan and image numbers (specfile, .fio...)
    :param scan_number: the scan number to load
    :param detector: the detector object: Class experiment_utils.Detector()
    :param setup: the experimental setup: Class SetupPreprocessing()
    :param flatfield: the 2D flatfield array
    :param hotpixels: the 2D hotpixels array. 1 for a hotpixel, 0 for normal pixels.
    :param orthogonalize: if True will interpolate the data and the mask on an orthogonal grid using xrayutilities
    :param hxrd: an initialized xrayutilities HXRD object used for the orthogonalization of the dataset
    :param regrid_cdi: set to True to interpolate forward scattering CDI data into the loaboratory frame
    :param debugging: set to True to see plots
    :param kwargs:
     - follow_bragg (bool): True when for energy scans the detector was also scanned to follow the Bragg peak
    :return:
     - the 3D data array in the detector frame and the 3D mask array
     - frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
       A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.
     - the monitor values for normalization
    """
    for k in kwargs.keys():
        if k in ['follow_bragg']:
            follow_bragg = kwargs['follow_bragg']
        else:
            raise Exception("unknown keyword argument given: allowed is 'follow_bragg'")
    if setup.rocking_angle == 'energy':
        try:
            follow_bragg
        except NameError:
            raise TypeError("Parameter 'follow_bragg' not provided, defaulting to False")
    rawdata, rawmask, monitor, frames_logical = load_data(logfile=logfile, scan_number=scan_number, detector=detector,
                                                          beamline=setup.beamline, flatfield=flatfield,
                                                          hotpixels=hotpixels, debugging=debugging)
    
    if not orthogonalize:
        if regrid_cdi:
            rawdata, rawmask = grid_cdi(rawdata, rawmask, setup=setup)
        return [], rawdata, [], rawmask, [], frames_logical, monitor
    else:
        nbz, nby, nbx = rawdata.shape
        qx, qz, qy, frames_logical = \
            regrid(logfile=logfile, nb_frames=rawdata.shape[0], scan_number=scan_number, detector=detector,
                   setup=setup, hxrd=hxrd, frames_logical=frames_logical, follow_bragg=follow_bragg)

        if setup.beamline == 'ID01':
            # below is specific to ID01 energy scans where frames are duplicated for undulator gap change
            if setup.rocking_angle == 'energy':  # frames need to be removed
                tempdata = np.zeros(((frames_logical != 0).sum(), nby, nbx))
                offset_frame = 0
                for idx in range(nbz):
                    if frames_logical[idx] != 0:  # use frame
                        tempdata[idx-offset_frame, :, :] = rawdata[idx, :, :]
                    else:  # average with the precedent frame
                        offset_frame = offset_frame + 1
                        tempdata[idx-offset_frame, :, :] = (tempdata[idx-offset_frame, :, :] + rawdata[idx, :, :])/2
                rawdata = tempdata
                rawmask = rawmask[0:rawdata.shape[0], :, :]  # truncate the mask to have the correct size

        gridder = xu.Gridder3D(nbz, nby, nbx)
        # convert mask to rectangular grid in reciprocal space
        gridder(qx, qz, qy, rawmask)
        mask = np.copy(gridder.data)
        # convert data to rectangular grid in reciprocal space
        gridder(qx, qz, qy, rawdata)

        q_values = [gridder.xaxis, gridder.yaxis, gridder.zaxis]

        return q_values, rawdata, gridder.data, rawmask, mask, frames_logical, monitor


def higher_primes(number, maxprime=13, required_dividers=(4,)):
    """
    Find the closest integer >=n (or list/array of integers), for which the largest prime divider is <=maxprime,
    and has to include some dividers. The default values for maxprime is the largest integer accepted
    by the clFFT library for OpenCL GPU FFT. Adapted from PyNX.

    :param number: the integer number
    :param maxprime: the largest prime factor acceptable
    :param required_dividers: a list of required dividers for the returned integer.
    :return: the integer (or list/array of integers) fulfilling the requirements
    """
    if (type(number) is list) or (type(number) is tuple) or (type(number) is np.ndarray):
        vn = []
        for i in number:
            limit = i
            assert (i > 1 and maxprime <= i)
            while try_smaller_primes(i, maxprime=maxprime, required_dividers=required_dividers) is False:
                i = i + 1
                if i == limit:
                    return limit
            vn.append(i)
        if type(number) is np.ndarray:
            return np.array(vn)
        return vn
    else:
        limit = number
        assert (number > 1 and maxprime <= number)
        while try_smaller_primes(number, maxprime=maxprime, required_dividers=required_dividers) is False:
            number = number + 1
            if number == limit:
                return limit
        return number


def init_qconversion(setup):
    """
    Initialize the qconv object from xrayutilities depending on the setup parameters

    :param setup: the experimental setup: Class SetupPreprocessing()
    :return: qconv object and offsets for motors
    """
    beamline = setup.beamline
    offset_inplane = setup.offset_inplane
    beam_direction = setup.beam_direction

    if beamline == 'ID01':
        offsets = (0, 0, 0, offset_inplane, 0)  # eta chi phi nu del
        qconv = xu.experiment.QConversion(['y-', 'x+', 'z-'], ['z-', 'y-'], r_i=beam_direction)  # for ID01
        # 2S+2D goniometer (ID01 goniometer, sample: eta, phi      detector: nu,del
        # the vector beam_direction is giving the direction of the primary beam
        # convention for coordinate system: x downstream; z upwards; y to the "outside" (right-handed)
    elif beamline == 'SIXS_2018' or beamline == 'SIXS_2019':
        offsets = (0, 0, 0, offset_inplane, 0)  # beta, mu, beta, gamma del
        qconv = xu.experiment.QConversion(['y-', 'z+'], ['y-', 'z+', 'y-'], r_i=beam_direction)  # for SIXS
        # 2S+3D goniometer (SIXS goniometer, sample: beta, mu     detector: beta, gamma, del
        # beta is below both sample and detector circles
        # the vector is giving the direction of the primary beam
        # convention for coordinate system: x downstream; z upwards; y to the "outside" (right-handed)
    elif beamline == 'CRISTAL':
        offsets = (0, offset_inplane, 0)  # komega, gamma, delta
        qconv = xu.experiment.QConversion(['y-'], ['z+', 'y-'], r_i=beam_direction)  # for CRISTAL
        # 1S+2D goniometer (CRISTAL goniometer, sample: mgomega    detector: gamma, delta
        # the vector is giving the direction of the primary beam
        # convention for coordinate system: x downstream; z upwards; y to the "outside" (right-handed)
    elif beamline == 'P10':
        offsets = (0, 0, 0, 0, offset_inplane, 0)  # mu, omega, chi, phi, gamma del
        qconv = xu.experiment.QConversion(['z+', 'y-', 'x+', 'z-'], ['z+', 'y-'], r_i=beam_direction)  # for CRISTAL
        # 4S+2D goniometer (P10 goniometer, sample: mu, omega, chi,phi   detector: gamma, delta
        # the vector is giving the direction of the primary beam
        # convention for coordinate system: x downstream; z upwards; y to the "outside" (right-handed)
    else:
        raise ValueError("Incorrect value for parameter 'beamline'")

    return qconv, offsets


def load_cristal_data(logfile, detector, flatfield, hotpixels, debugging=False):
    """
    Load CRISTAL data, apply filters and concatenate it for phasing. The address of dataset and monitor in the h5 file
     may have to be modified.

    :param logfile: h5py File object of CRISTAL .nxs scan file
    :param detector: the detector object: Class experiment_utils.Detector()
    :param flatfield: the 2D flatfield array
    :param hotpixels: the 2D hotpixels array
    :param debugging: set to True to see plots
    :return:
     - the 3D data array in the detector frame and the 3D mask array
     - a logical array of length = initial frames number. A frame used will be set to True, a frame unused to False.
     - the monitor values for normalization
    """
    mask_2d = np.zeros((detector.nb_pixel_y, detector.nb_pixel_x))

    group_key = list(logfile.keys())[0]
    tmp_data = logfile['/' + group_key + '/scan_data/data_06'][:]

    nb_img = tmp_data.shape[0]
    data = np.zeros((nb_img, detector.roi[1] - detector.roi[0], detector.roi[3] - detector.roi[2]))

    for idx in range(nb_img):
        ccdraw = tmp_data[idx, :, :]
        ccdraw, mask_2d = remove_hotpixels(data=ccdraw, mask=mask_2d, hotpixels=hotpixels)
        if detector.name == "Maxipix":
            ccdraw, mask_2d = mask_maxipix(ccdraw, mask_2d)
        else:
            raise ValueError('Detector ', detector.name, 'not supported for CRISTAL')
        ccdraw = flatfield * ccdraw
        ccdraw = ccdraw[detector.roi[0]:detector.roi[1], detector.roi[2]:detector.roi[3]]
        data[idx, :, :] = ccdraw

    mask_2d = mask_2d[detector.roi[0]:detector.roi[1], detector.roi[2]:detector.roi[3]]
    data, mask_2d = check_pixels(data=data, mask=mask_2d, debugging=debugging)
    mask3d = np.repeat(mask_2d[np.newaxis, :, :], nb_img, axis=0)
    mask3d[np.isnan(data)] = 1
    data[np.isnan(data)] = 0

    frames_logical = np.ones(nb_img)

    monitor = logfile['/' + group_key + '/scan_data/data_04'][:]

    return data, mask3d, monitor, frames_logical


def load_data(logfile, scan_number, detector, beamline, flatfield=None, hotpixels=None, debugging=False):
    """
    Load ID01 data, apply filters and concatenate it for phasing.

    :param logfile: file containing the information about the scan and image numbers (specfile, .fio...)
    :param scan_number: the scan number to load
    :param detector: the detector object: Class experiment_utils.Detector()
    :param beamline: 'ID01', 'SIXS_2018', 'SIXS_2019', '34ID', 'P10', 'CRISTAL'
    :param flatfield: the 2D flatfield array
    :param hotpixels: the 2D hotpixels array. 1 for a hotpixel, 0 for normal pixels.
    :param debugging: set to True to see plots
    :return:
     - the 3D data array in the detector frame and the 3D mask array
     - the monitor values for normalization
     - frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
       A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.
    """
    if flatfield is None:
        flatfield = np.ones((detector.nb_pixel_y, detector.nb_pixel_x))
    if hotpixels is None:
        hotpixels = np.zeros((detector.nb_pixel_y, detector.nb_pixel_x))

    if beamline == 'ID01':
        data, mask3d, monitor, frames_logical = load_id01_data(logfile, scan_number, detector, flatfield, hotpixels,
                                                               debugging=debugging)
    elif beamline == 'SIXS_2018' or beamline == 'SIXS_2019':
        data, mask3d, monitor, frames_logical = load_sixs_data(logfile, beamline, detector, flatfield, hotpixels,
                                                               debugging=debugging)
    elif beamline == 'CRISTAL':
        data, mask3d, monitor, frames_logical = load_cristal_data(logfile, detector, flatfield, hotpixels,
                                                                  debugging=debugging)
    elif beamline == 'P10':
        data, mask3d, monitor, frames_logical = load_p10_data(logfile, detector, flatfield, hotpixels,
                                                              debugging=debugging)
    else:
        raise ValueError('Wrong value for "rocking_angle" parameter')

    # remove indices where frames_logical=0
    nbz, nby, nbx = data.shape
    nb_frames = (frames_logical != 0).sum()

    newdata = np.zeros((nb_frames, nby, nbx))
    newmask = np.zeros((nb_frames, nby, nbx))
    # do not process the monitor here, it is done in normalize_dataset()

    nb_overlap = 0
    for idx in range(len(frames_logical)):
        if frames_logical[idx]:
            newdata[idx - nb_overlap, :, :] = data[idx, :, :]
            newmask[idx - nb_overlap, :, :] = mask3d[idx, :, :]
        else:
            nb_overlap = nb_overlap + 1

    return newdata, newmask, monitor, frames_logical


def load_flatfield(flatfield_file):
    """
    Load a flatfield file.

    :param flatfield_file: the path of the flatfield file
    :return: a 2D flatfield
    """
    if flatfield_file != "":
        flatfield = np.load(flatfield_file)
        npz_key = flatfield.files
        flatfield = flatfield[npz_key[0]]
        if flatfield.ndim != 2:
            raise ValueError('flatfield should be a 2D array')
    else:
        flatfield = None
    return flatfield


def load_hotpixels(hotpixels_file):
    """
    Load a hotpixels file.

    :param hotpixels_file: the path of the hotpixels file
    :return: a 2D array of hotpixels (1 for hotpixel, 0 for normal pixel)
    """
    if hotpixels_file != "":
        hotpixels = np.load(hotpixels_file)
        npz_key = hotpixels.files
        hotpixels = hotpixels[npz_key[0]]
        if hotpixels.ndim == 3:
            hotpixels = hotpixels.sum(axis=0)
        if hotpixels.ndim != 2:
            raise ValueError('hotpixels should be a 2D array')
        hotpixels[np.nonzero(hotpixels)] = 1
    else:
        hotpixels = None
    return hotpixels


def load_id01_data(logfile, scan_number, detector, flatfield, hotpixels, debugging=False):
    """
    Load ID01 data, apply filters and concatenate it for phasing.

    :param logfile: Silx SpecFile object containing the information about the scan and image numbers
    :param scan_number: the scan number to load
    :param detector: the detector object: Class experiment_utils.Detector()
    :param flatfield: the 2D flatfield array
    :param hotpixels: the 2D hotpixels array
    :param debugging: set to True to see plots
    :return:
     - the 3D data array in the detector frame and the 3D mask array
     - the monitor values for normalization
     - frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
       A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.
    """
    mask_2d = np.zeros((detector.nb_pixel_y, detector.nb_pixel_x))

    labels = logfile[str(scan_number) + '.1'].labels  # motor scanned
    labels_data = logfile[str(scan_number) + '.1'].data  # motor scanned

    ccdfiletmp = os.path.join(detector.datadir, detector.template_imagefile)

    try:
        monitor = labels_data[labels.index('exp1'), :]  # mon2 monitor at ID01
    except ValueError:
        monitor = labels_data[labels.index('mon2'), :]  # exp1 for old data at ID01

    try:
        ccdn = labels_data[labels.index(detector.counter), :]
    except ValueError:
        raise ValueError(detector.counter, 'not in the list, the detector name may be wrong')

    nb_img = len(ccdn)
    data = np.zeros((nb_img, detector.roi[1] - detector.roi[0], detector.roi[3] - detector.roi[2]))
    for idx in range(nb_img):
        i = int(ccdn[idx])
        e = fabio.open(ccdfiletmp % i)
        ccdraw = e.data
        ccdraw, mask_2d = remove_hotpixels(data=ccdraw, mask=mask_2d, hotpixels=hotpixels)
        if detector.name == "Eiger2M":
            ccdraw, mask_2d = mask_eiger(data=ccdraw, mask=mask_2d)
        elif detector.name == "Maxipix":
            ccdraw, mask_2d = mask_maxipix(data=ccdraw, mask=mask_2d)
        else:
            raise ValueError('Detector ', detector.name, 'not supported for ID01')
        ccdraw = flatfield * ccdraw
        ccdraw = ccdraw[detector.roi[0]:detector.roi[1], detector.roi[2]:detector.roi[3]]
        data[idx, :, :] = ccdraw

    mask_2d = mask_2d[detector.roi[0]:detector.roi[1], detector.roi[2]:detector.roi[3]]
    data, mask_2d = check_pixels(data=data, mask=mask_2d, debugging=debugging)
    mask3d = np.repeat(mask_2d[np.newaxis, :, :], nb_img, axis=0)
    mask3d[np.isnan(data)] = 1
    data[np.isnan(data)] = 0

    frames_logical = np.ones(nb_img)

    return data, mask3d, monitor, frames_logical


def load_p10_data(logfile, detector, flatfield, hotpixels, debugging=False):
    """
    Load P10 data, apply filters and concatenate it for phasing.

    :param logfile: path of the . fio file containing the information about the scan
    :param detector: the detector object: Class experiment_utils.Detector()
    :param flatfield: the 2D flatfield array
    :param hotpixels: the 2D hotpixels array
    :param debugging: set to True to see plots
    :return:
     - the 3D data array in the detector frame and the 3D mask array
     - the monitor values for normalization
     - frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
       A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.

    """
    import hdf5plugin  # should be imported before h5py
    import h5py
    mask_2d = np.zeros((detector.nb_pixel_y, detector.nb_pixel_x))

    ccdfiletmp = os.path.join(detector.datadir, detector.template_imagefile % 1)
    h5file = h5py.File(ccdfiletmp, 'r')

    try:
        tmp_data = h5file['entry']['data']['data'][:]
    except OSError:
        raise OSError('hdf5plugin is not installed')
    nb_img = tmp_data.shape[0]
    data = np.zeros((nb_img, detector.roi[1] - detector.roi[0], detector.roi[3] - detector.roi[2]))

    for idx in range(nb_img):

        ccdraw, mask2d = remove_hotpixels(data=tmp_data[idx, :, :], mask=mask_2d, hotpixels=hotpixels)
        if detector.name == "Eiger4M":
            ccdraw, mask_2d = mask_eiger4m(data=ccdraw, mask=mask_2d)
        else:
            raise ValueError('Detector ', detector.name, 'not supported for ID01')
        ccdraw = flatfield * ccdraw
        ccdraw = ccdraw[detector.roi[0]:detector.roi[1], detector.roi[2]:detector.roi[3]]
        data[idx, :, :] = ccdraw

    mask_2d = mask_2d[detector.roi[0]:detector.roi[1], detector.roi[2]:detector.roi[3]]
    data, mask_2d = check_pixels(data=data, mask=mask_2d, debugging=debugging)
    mask3d = np.repeat(mask_2d[np.newaxis, :, :], nb_img, axis=0)
    mask3d[np.isnan(data)] = 1
    data[np.isnan(data)] = 0

    frames_logical = np.ones(nb_img)
    fio = open(logfile, 'r')

    monitor = []
    fio_lines = fio.readlines()
    for line in fio_lines:
        this_line = line.strip()
        words = this_line.split()
        if 'Col' in words and ('ipetra' in words or 'curpetra' in words):
            # template = ' Col 6 ipetra DOUBLE\n' (2018) or ' Col 6 curpetra DOUBLE\n' (2019)
            index_monitor = int(words[1])-1  # python index starts at 0
        try:
            float(words[0])  # if this does not fail, we are reading data
            monitor.append(float(words[index_monitor]))
        except ValueError:  # first word is not a number, skip this line
            continue

    fio.close()
    monitor = np.asarray(monitor, dtype=float)
    return data, mask3d, monitor, frames_logical


def load_sixs_data(logfile, beamline, detector, flatfield, hotpixels, debugging=False):
    """
    Load SIXS data, apply filters and concatenate it for phasing.

    :param logfile: nxsReady Dataset object of SIXS .nxs scan file
    :param beamline: SIXS_2019 or SIXS_2018
    :param detector: the detector object: Class experiment_utils.Detector()
    :param flatfield: the 2D flatfield array
    :param hotpixels: the 2D hotpixels array
    :param debugging: set to True to see plots
    :return:
     - the 3D data array in the detector frame and the 3D mask array
     - the monitor values for normalization
     - frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
       A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.
    """

    if beamline == 'SIXS_2018':
        data = logfile.mfilm[:]
        monitor = logfile.imon1[:]
    else:
        try:
            data = logfile.mpx_image[:]
        except:
            data = logfile.maxpix[:]
            monitor = logfile.imon0[:]
    
    if detector.roiUser:
        # apply roi
        slice0 = slice(detector.roi[0],detector.roi[1],1)
        slice1 = slice(detector.roi[2],detector.roi[3],1)
        
        data = data[:,slice0,slice1]
        hotpixels = hotpixels[slice0,slice1]
        flatfield = flatfield[slice0,slice1]
        mask_2d = np.zeros_like(data[0,:,:])
        
    else: 
        mask_2d = np.zeros((detector.nb_pixel_y, detector.nb_pixel_x)) 
        # load data as usual

    frames_logical = np.ones(data.shape[0])
    #frames_logical[0] = 0  # first frame is duplicated

    nb_img = data.shape[0]
    for idx in range(nb_img):
        ccdraw = data[idx, :, :]
        ccdraw, mask_2d = remove_hotpixels(data=ccdraw, mask=mask_2d, hotpixels=hotpixels)
        if detector.name == "Maxipix":
            ccdraw, mask_2d = mask_maxipix(data=ccdraw, mask=mask_2d)
        else:
            raise ValueError('Detector ', detector.name, 'not supported for SIXS')
        ccdraw = flatfield * ccdraw
        #ccdraw = ccdraw[detector.roi[0]:detector.roi[1], detector.roi[2]:detector.roi[3]]
        data[idx, :, :] = ccdraw

    #mask_2d = mask_2d[detector.roi[0]:detector.roi[1], detector.roi[2]:detector.roi[3]]
    data, mask_2d = check_pixels(data=data, mask=mask_2d, debugging=debugging)
    mask3d = np.repeat(mask_2d[np.newaxis, :, :], nb_img, axis=0)
    mask3d[np.isnan(data)] = 1
    data[np.isnan(data)] = 0
    return data, mask3d, monitor, frames_logical


def mask_eiger(data, mask):
    """
    Mask data measured with an Eiger2M detector

    :param data: the 2D data to mask
    :param mask: the 2D mask to be updated
    :return: the masked data and the updated mask
    """
    if data.ndim != 2 or mask.ndim != 2:
        raise ValueError('Data and mask should be 2D arrays')

    if data.shape != mask.shape:
        raise ValueError('Data and mask must have the same shape\n data is ', data.shape, ' while mask is ', mask.shape)

    data[:, 255: 259] = 0
    data[:, 513: 517] = 0
    data[:, 771: 775] = 0
    data[0: 257, 72: 80] = 0
    data[255: 259, :] = 0
    data[511: 552, :0] = 0
    data[804: 809, :] = 0
    data[1061: 1102, :] = 0
    data[1355: 1359, :] = 0
    data[1611: 1652, :] = 0
    data[1905: 1909, :] = 0
    data[1248:1290, 478] = 0
    data[1214:1298, 481] = 0
    data[1649:1910, 620:628] = 0

    mask[:, 255: 259] = 1
    mask[:, 513: 517] = 1
    mask[:, 771: 775] = 1
    mask[0: 257, 72: 80] = 1
    mask[255: 259, :] = 1
    mask[511: 552, :] = 1
    mask[804: 809, :] = 1
    mask[1061: 1102, :] = 1
    mask[1355: 1359, :] = 1
    mask[1611: 1652, :] = 1
    mask[1905: 1909, :] = 1
    mask[1248:1290, 478] = 1
    mask[1214:1298, 481] = 1
    mask[1649:1910, 620:628] = 1
    return data, mask


def mask_eiger4m(data, mask):
    """
    Mask data measured with an Eiger4M detector

    :param data: the 2D data to mask
    :param mask: the 2D mask to be updated
    :return: the masked data and the updated mask
    """
    if data.ndim != 2 or mask.ndim != 2:
        raise ValueError('Data and mask should be 2D arrays')

    if data.shape != mask.shape:
        raise ValueError('Data and mask must have the same shape\n data is ', data.shape, ' while mask is ', mask.shape)

    data[:, 1029:1041] = 0
    data[513:552, :] = 0
    data[1064:1103, :] = 0
    data[1614:1654, :] = 0

    mask[:, 1029:1041] = 1
    mask[513:552, :] = 1
    mask[1064:1103, :] = 1
    mask[1614:1654, :] = 1
    return data, mask


def mask_maxipix(data, mask):
    """
    Mask data measured with a Maxipix detector

    :param data: the 2D data to mask
    :param mask: the 2D mask to be updated
    :return: the masked data and the updated mask
    """
    if data.ndim != 2 or mask.ndim != 2:
        raise ValueError('Data and mask should be 2D arrays')

    if data.shape != mask.shape:
        raise ValueError('Data and mask must have the same shape\n data is ', data.shape, ' while mask is ', mask.shape)

    data[:, 255:261] = 0
    data[255:261, :] = 0

    mask[:, 255:261] = 1
    mask[255:261, :] = 1
    return data, mask


def mean_filter(data, nb_neighbours, mask, interpolate=False, debugging=False):
    """
    Apply a mean filter if the empty pixel is surrounded by nb_neighbours or more pixels

    :param data: 2D array to be filtered
    :param nb_neighbours: minimum number of non-zero neighboring pixels for median filtering
    :param mask: 2D mask array
    :param interpolate: if False will mask isolated pixels based on 'nb_neighbours',
      if True will interpolate isolated pixels based on 'nb_neighbours'
    :type interpolate: bool
    :param debugging: set to True to see plots
    :type debugging: bool
    :return: updated data and mask, number of pixels treated
    """

    if data.ndim != 2 or mask.ndim != 2:
        raise ValueError('Data and mask should be 2D arrays')

    if debugging:
        gu.combined_plots(tuple_array=(data, mask), tuple_sum_frames=(False, False), tuple_sum_axis=(0, 0),
                          tuple_width_v=(np.nan, np.nan), tuple_width_h=(np.nan, np.nan), tuple_colorbar=(True, True),
                          tuple_vmin=(-1, 0), tuple_vmax=(np.nan, 1), tuple_scale=('log', 'linear'),
                          tuple_title=('Data before filtering', 'Mask before filtering'), reciprocal_space=True)
    zero_pixels = np.argwhere(data == 0)
    nb_pixels = 0
    for indx in range(zero_pixels.shape[0]):
        pixrow = zero_pixels[indx, 0]
        pixcol = zero_pixels[indx, 1]
        temp = data[pixrow-1:pixrow+2, pixcol-1:pixcol+2]
        if temp.size != 0 and temp.sum() > 24 and sum(sum(temp != 0)) >= nb_neighbours:
            # mask/interpolate if at least 3 photons in each neighboring pixels
            nb_pixels = nb_pixels + 1
            if interpolate:
                value = temp.sum() / sum(sum(temp != 0))
                data[pixrow, pixcol] = value
                mask[pixrow, pixcol] = 0
            else:
                mask[pixrow, pixcol] = 1
    if interpolate:
        print("Nb of filtered pixel: ", nb_pixels)
    else:
        print("Nb of masked pixel: ", nb_pixels)

    if debugging:
        gu.combined_plots(tuple_array=(data, mask), tuple_sum_frames=(False, False), tuple_sum_axis=(0, 0),
                          tuple_width_v=(np.nan, np.nan), tuple_width_h=(np.nan, np.nan), tuple_colorbar=(True, True),
                          tuple_vmin=(-1, 0), tuple_vmax=(np.nan, 1), tuple_scale=('log', 'linear'),
                          tuple_title=('Data after filtering', 'Mask after filtering'), reciprocal_space=True)
    return data, nb_pixels, mask


def motor_positions_cristal(logfile, setup):
    """
    Load the scan data and extract motor positions.

    :param logfile: h5py File object of CRISTAL .nxs scan file
    :param setup: the experimental setup: Class SetupPreprocessing()
    :return: (mgomega, gamma, delta) motor positions
    """
    if setup.rocking_angle != 'outofplane':
        raise ValueError('Only out of plane rocking curve implemented for CRISTAL')

    group_key = list(logfile.keys())[0]

    mgomega = logfile['/' + group_key + '/scan_data/actuator_1_1'][:] / 1e6  # mgomega is scanned

    delta = logfile['/' + group_key + '/CRISTAL/Diffractometer/I06-C-C07-EX-DIF-DELTA/position'][:]

    gamma = logfile['/' + group_key + '/CRISTAL/Diffractometer/I06-C-C07-EX-DIF-GAMMA/position'][:]

    return mgomega, gamma, delta


def motor_positions_id01(frames_logical, logfile, scan_number, setup, follow_bragg=False):
    """
    Load the scan data and extract motor positions.

    :param follow_bragg: True when for energy scans the detector was also scanned to follow the Bragg peak
    :param frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
     A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.
    :param logfile: Silx SpecFile object containing the information about the scan and image numbers
    :param scan_number: the scan number to load
    :param setup: the experimental setup: Class SetupPreprocessing()
    :return: (eta, chi, phi, nu, delta, energy) motor positions
    """
    motor_names = logfile[str(scan_number) + '.1'].motor_names  # positioners
    motor_positions = logfile[str(scan_number) + '.1'].motor_positions  # positioners
    labels = logfile[str(scan_number) + '.1'].labels  # motor scanned
    labels_data = logfile[str(scan_number) + '.1'].data  # motor scanned

    energy = setup.energy  # will be overridden if setup.rocking_angle is 'energy'

    if follow_bragg:
        delta = list(labels_data[labels.index('del'), :])  # scanned
    else:
        delta = motor_positions[motor_names.index('del')]  # positioner
    nu = motor_positions[motor_names.index('nu')]  # positioner
    chi = 0

    if setup.rocking_angle == "outofplane":
        eta = labels_data[labels.index('eta'), :]
        phi = motor_positions[motor_names.index('phi')]
    elif setup.rocking_angle == "inplane":
        phi = labels_data[labels.index('phi'), :]
        eta = motor_positions[motor_names.index('eta')]
    elif setup.rocking_angle == "energy":
        raw_energy = list(labels_data[labels.index('energy'), :])  # in kev, scanned
        phi = motor_positions[motor_names.index('phi')]  # positioner
        eta = motor_positions[motor_names.index('eta')]  # positioner
        if follow_bragg == 1:
            delta = list(labels_data[labels.index('del'), :])  # scanned

        nb_overlap = 0
        energy = raw_energy[:]
        for idx in range(len(raw_energy) - 1):
            if raw_energy[idx + 1] == raw_energy[idx]:  # duplicate energy when undulator gap is changed
                frames_logical[idx + 1] = 0
                energy.pop(idx - nb_overlap)
                if follow_bragg == 1:
                    delta.pop(idx - nb_overlap)
                nb_overlap = nb_overlap + 1
        energy = np.array(energy) * 1000.0 - 6  # switch to eV, 6 eV of difference at ID01

    else:
        raise ValueError('Invalid rocking angle ', setup.rocking_angle, 'for ID01')

    return eta, chi, phi, nu, delta, energy, frames_logical


def motor_positions_p10(logfile, setup):
    """
    Load the .fio file from the scan and extract motor positions.

    :param logfile: path of the . fio file containing the information about the scan
    :param setup: the experimental setup: Class SetupPreprocessing()
    :return: (om, phi, chi, mu, gamma, delta) motor positions
    """

    fio = open(logfile, 'r')
    if setup.rocking_angle == "outofplane":
        om = []
    elif setup.rocking_angle == "inplane":
        phi = []
    else:
        raise ValueError('Wrong value for "rocking_angle" parameter')

    fio_lines = fio.readlines()
    for line in fio_lines:
        this_line = line.strip()
        words = this_line.split()

        if 'Col' in words and 'om' in words:  # om is scanned, template = ' Col 0 om DOUBLE\n'
            index_om = int(words[1]) - 1  # python index starts at 0
        if 'om' in words and '=' in words and setup.rocking_angle == "inplane":  # om is a positioner
            om = float(words[2])

        if 'Col' in words and 'phi' in words:  # phi is scanned, template = ' Col 0 phi DOUBLE\n'
            index_phi = int(words[1]) - 1  # python index starts at 0
        if 'phi' in words and '=' in words and setup.rocking_angle == "outofplane":  # phi is a positioner
            phi = float(words[2])

        if 'chi' in words and '=' in words:  # template for positioners: 'chi = 90.0\n'
            chi = float(words[2])
        if 'del' in words and '=' in words:  # template for positioners: 'del = 30.05\n'
            delta = float(words[2])
        if 'gam' in words and '=' in words:  # template for positioners: 'gam = 4.05\n'
            gamma = float(words[2])
        if 'mu' in words and '=' in words:  # template for positioners: 'mu = 0.0\n'
            mu = float(words[2])

        try:
            float(words[0])  # if this does not fail, we are reading data
            if setup.rocking_angle == "outofplane":
                om.append(float(words[index_om]))
            else:  # phi
                phi.append(float(words[index_phi]))
        except ValueError:  # first word is not a number, skip this line
            continue

    if setup.rocking_angle == "outofplane":
        om = np.asarray(om, dtype=float)
    else:  # phi
        phi = np.asarray(phi, dtype=float)

    fio.close()
    return om, phi, chi, mu, gamma, delta


def motor_positions_sixs(logfile, frames_logical, setup):
    """
    Load the scan data and extract motor positions.

    :param logfile: nxsReady Dataset object of SIXS .nxs scan file
    :param frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
     A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.
    :param setup: the experimental setup: Class SetupPreprocessing()
    :return: (beta, mgomega, gamma, delta) motor positions and updated frames_logical
    """
    delta = logfile.delta[0]  # not scanned
    gamma = logfile.gamma[0]  # not scanned
    if setup.beamline == 'SIXS_2018':
        beta = logfile.basepitch[0]  # not scanned
    elif setup.beamline == 'SIXS_2019':  # data recorder changed after 11/03/2019
        beta = logfile.beta[0]  # not scanned
    else:
        raise ValueError('Wrong value for "beamline" parameter: beamline not supported')
    temp_mu = logfile.mu[:]

    mu = np.zeros((frames_logical != 0).sum())  # first frame is duplicated for SIXS_2018
    nb_overlap = 0
    for idx in range(len(frames_logical)):
        if frames_logical[idx]:
            mu[idx - nb_overlap] = temp_mu[idx]
        else:
            nb_overlap = nb_overlap + 1

    return beta, mu, gamma, delta, frames_logical


def motor_values(frames_logical, logfile, scan_number, setup, follow_bragg=False):
    """
    Load the scan data and extract motor positions.

    :param follow_bragg: True when for energy scans the detector was also scanned to follow the Bragg peak
    :param frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
     A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.
    :param logfile: file containing the information about the scan and image numbers (specfile, .fio...)
    :param scan_number: the scan number to load
    :param setup: the experimental setup: Class SetupPreprocessing()
    :return: (rocking angular step, grazing incidence angle, inplane detector angle, outofplane detector angle)
     corrected values
    """
    if setup.beamline == 'ID01':
        if setup.rocking_angle == 'outofplane':  # eta rocking curve
            tilt, _, _, inplane, outofplane, _, _ = \
                motor_positions_id01(frames_logical, logfile, scan_number, setup, follow_bragg=follow_bragg)
            grazing = 0
        elif setup.rocking_angle == 'inplane':  # phi rocking curve
            grazing, _, tilt, inplane, outofplane, _, _ = \
                motor_positions_id01(frames_logical, logfile, scan_number, setup, follow_bragg=follow_bragg)
        else:
            raise ValueError('Wrong value for "rocking_angle" parameter')

    elif setup.beamline == 'SIXS_2018' or setup.beamline == 'SIXS_2019':
        if setup.rocking_angle == 'inplane':  # mu rocking curve
            grazing, tilt, inplane, outofplane, _ = motor_positions_sixs(logfile, frames_logical, setup)
        else:
            raise ValueError('Out-of-plane rocking curve not implemented for SIXS')

    elif setup.beamline == 'CRISTAL':
        if setup.rocking_angle == 'outofplane':  # mgomega rocking curve
            tilt, inplane, outofplane = motor_positions_cristal(logfile, setup)
            grazing = 0
            inplane = inplane[0]
            outofplane = outofplane[0]
        else:
            raise ValueError('Inplane rocking curve not implemented for CRISTAL')

    elif setup.beamline == 'P10':
        if setup.rocking_angle == 'outofplane':  # om rocking curve
            tilt, _, _, _, inplane, outofplane = motor_positions_p10(logfile, setup)
            grazing = 0
        elif setup.rocking_angle == 'inplane':  # phi rocking curve
            grazing, tilt, _, _, inplane, outofplane = motor_positions_p10(logfile, setup)
        else:
            raise ValueError('Wrong value for "rocking_angle" parameter')
    else:
        raise ValueError('Wrong value for "beamline" parameter: beamline not supported')

    return tilt, grazing, inplane, outofplane


def normalize_dataset(array, raw_monitor, frames_logical, norm_to_min=False, debugging=False):
    """
    Normalize array using the monitor values.

    :param array: the 3D array to be normalized
    :param raw_monitor: the monitor values
    :param frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
     A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.
    :param norm_to_min: normalize to min(monitor) instead of max(monitor)
    :type norm_to_min: bool
    :param debugging: set to True to see plots
    :type debugging: bool
    :return:
     - normalized dataset
     - updated monitor
     - a title for plotting
    """
    ndim = array.ndim
    if ndim != 3:
        raise ValueError('Array should be 3D')

    if debugging:
        gu.imshow_plot(array=array, sum_frames=True, sum_axis=1, vmin=0, scale='log', title='Data before normalization')

    # crop/pad monitor depending on frames_logical array
    monitor = np.zeros((frames_logical != 0).sum())
    print(frames_logical,frames_logical.shape)
    nb_overlap = 0
    nb_padded = 0
    for idx in range(len(frames_logical)):
        if frames_logical[idx] == -1:  # padded frame, no monitor value for this
            if norm_to_min:
                monitor[idx - nb_overlap] = raw_monitor.min()
            else:  # norm to max
                monitor[idx - nb_overlap] = raw_monitor.max()
            nb_padded = nb_padded + 1
        elif frames_logical[idx] == 1:
            monitor[idx - nb_overlap] = raw_monitor[idx-nb_padded]
        else:
            nb_overlap = nb_overlap + 1
    print(monitor.shape,monitor)
    if nb_padded != 0:
        print('Monitor value set to 1 for ', nb_padded, ' frames padded')

    if norm_to_min:
        monitor = monitor.min() / monitor
        title = 'monitor.min() / monitor'
    else:  # norm to max
        monitor = monitor / monitor.max()
        title = 'monitor / monitor.max()'

    nbz = array.shape[0]
    if len(monitor) != nbz:
        raise ValueError('The frame number and the monitor data length are different:'
                         ' Got ', nbz, 'frames but ', len(monitor), ' monitor values')

    for idx in range(nbz):
        array[idx, :, :] = array[idx, :, :] * monitor[idx]

    return array, monitor, title


def primes(number):
    """
    Returns the prime decomposition of n as a list. Adapted from PyNX.

    :param number: the integer to be decomposed
    :return: the list of prime dividers of number
    """
    if not isinstance(number, int):
        raise TypeError('Number should be an integer')

    list_primes = [1]
    assert (number > 0)
    i = 2
    while i * i <= number:
        while number % i == 0:
            list_primes.append(i)
            number //= i
        i += 1
    if number > 1:
        list_primes.append(number)
    return list_primes


def regrid(logfile, nb_frames, scan_number, detector, setup, hxrd, frames_logical=None, follow_bragg=False):
    """
    Load beamline motor positions and calculate q positions for orthogonalization.

    :param logfile: file containing the information about the scan and image numbers (specfile, .fio...)
    :param nb_frames: length of axis 0 in the 3D dataset. If the data was cropped or padded, it may be different
     from the length of frames_logical.
    :param scan_number: the scan number to load
    :param detector: the detector object: Class experiment_utils.Detector()
    :param setup: the experimental setup: Class SetupPreprocessing()
    :param hxrd: an initialized xrayutilities HXRD object used for the orthogonalization of the dataset
    :param frames_logical: array of initial length the number of measured frames. In case of padding the length changes.
     A frame whose index is set to 1 means that it is used, 0 means not used, -1 means padded (added) frame.
    :param follow_bragg: True when in energy scans the detector was also scanned to follow the Bragg peak
    :return:
     - qx, qz, qy components for the dataset
     - updated frames_logical
    """
    if frames_logical is None:  # retrieve the raw data length, then len(frames_logical) may be different from nb_frames
        # TODO: create a function which does not loda the data but use the specfile
        _, _, _, frames_logical = load_data(logfile=logfile, scan_number=scan_number, detector=detector,
                                            beamline=setup.beamline)

    if follow_bragg and setup.beamline != 'ID01':
        raise ValueError('Energy scan implemented only for ID01 beamline')

    if setup.beamline == 'ID01':
        eta, chi, phi, nu, delta, energy, frames_logical = \
            motor_positions_id01(frames_logical, logfile, scan_number, setup, follow_bragg=follow_bragg)

        if setup.rocking_angle == 'outofplane':  # eta rocking curve
            nb_steps = len(eta)
            tilt_angle = eta[1] - eta[0]

            if nb_steps < nb_frames:  # data has been padded, we suppose it is centered in z dimension
                pad_low = int((nb_frames - nb_steps + ((nb_frames - nb_steps) % 2)) / 2)
                pad_high = int((nb_frames - nb_steps + 1) / 2 - ((nb_frames - nb_steps) % 2))
                eta = np.concatenate((eta[0] + np.arange(-pad_low, 0, 1) * tilt_angle,
                                      eta,
                                      eta[-1] + np.arange(1, pad_high + 1, 1) * tilt_angle), axis=0)
            if nb_steps > nb_frames:  # data has been cropped, we suppose it is centered in z dimension
                eta = eta[(nb_steps - nb_frames) // 2: (nb_steps + nb_frames) // 2]

        elif setup.rocking_angle == 'inplane':  # phi rocking curve
            nb_steps = len(phi)
            tilt_angle = phi[1] - phi[0]

            if nb_steps < nb_frames:  # data has been padded, we suppose it is centered in z dimension
                pad_low = int((nb_frames - nb_steps + ((nb_frames - nb_steps) % 2)) / 2)
                pad_high = int((nb_frames - nb_steps + 1) / 2 - ((nb_frames - nb_steps) % 2))
                phi = np.concatenate((phi[0] + np.arange(-pad_low, 0, 1) * tilt_angle,
                                      phi,
                                      phi[-1] + np.arange(1, pad_high + 1, 1) * tilt_angle), axis=0)
            if nb_steps > nb_frames:  # data has been cropped, we suppose it is centered in z dimension
                phi = phi[(nb_steps - nb_frames) // 2: (nb_steps + nb_frames) // 2]

        else:
            raise ValueError('Wrong value for "rocking_angle" parameter')
        qx, qy, qz = hxrd.Ang2Q.area(eta, chi, phi, nu, delta, en=energy, delta=detector.offsets)

    elif setup.beamline == 'SIXS_2018' or setup.beamline == 'SIXS_2019':
        beta, mu, gamma, delta, frames_logical = motor_positions_sixs(logfile, frames_logical, setup)
        if setup.rocking_angle == 'inplane':  # mu rocking curve
            nb_steps = len(mu)
            tilt_angle = mu[1] - mu[0]

            if nb_steps < nb_frames:  # data has been padded, we suppose it is centered in z dimension
                pad_low = int((nb_frames - nb_steps + ((nb_frames - nb_steps) % 2)) / 2)
                pad_high = int((nb_frames - nb_steps + 1) / 2 - ((nb_frames - nb_steps) % 2))
                mu = np.concatenate((mu[0] + np.arange(-pad_low, 0, 1) * tilt_angle,
                                     mu,
                                     mu[-1] + np.arange(1, pad_high + 1, 1) * tilt_angle), axis=0)
            if nb_steps > nb_frames:  # data has been cropped, we suppose it is centered in z dimension
                mu = mu[(nb_steps - nb_frames) // 2: (nb_steps + nb_frames) // 2]

        else:
            raise ValueError('Out-of-plane rocking curve not implemented for SIXS')

        qx, qy, qz = hxrd.Ang2Q.area(beta, mu, beta, gamma, delta, en=setup.energy, delta=detector.offsets)

    elif setup.beamline == 'CRISTAL':
        mgomega, gamma, delta = motor_positions_cristal(logfile, setup)
        if setup.rocking_angle == 'outofplane':  # mgomega rocking curve
            nb_steps = len(mgomega)
            tilt_angle = mgomega[1] - mgomega[0]

            if nb_steps < nb_frames:  # data has been padded, we suppose it is centered in z dimension
                pad_low = int((nb_frames - nb_steps + ((nb_frames - nb_steps) % 2)) / 2)
                pad_high = int((nb_frames - nb_steps + 1) / 2 - ((nb_frames - nb_steps) % 2))
                mgomega = np.concatenate((mgomega[0] + np.arange(-pad_low, 0, 1) * tilt_angle,
                                          mgomega,
                                          mgomega[-1] + np.arange(1, pad_high + 1, 1) * tilt_angle), axis=0)
            if nb_steps > nb_frames:  # data has been cropped, we suppose it is centered in z dimension
                mgomega = mgomega[(nb_steps - nb_frames) // 2: (nb_steps + nb_frames) // 2]

        else:
            raise ValueError('Inplane rocking curve not implemented for CRISTAL')

        qx, qy, qz = hxrd.Ang2Q.area(mgomega, gamma, delta, en=setup.energy, delta=detector.offsets)

    elif setup.beamline == 'P10':
        om, phi, chi, mu, gamma, delta = motor_positions_p10(logfile, setup)
        if setup.rocking_angle == 'outofplane':  # om rocking curve
            nb_steps = len(om)
            tilt_angle = om[1] - om[0]

            if nb_steps < nb_frames:  # data has been padded, we suppose it is centered in z dimension
                pad_low = int((nb_frames - nb_steps + ((nb_frames - nb_steps) % 2)) / 2)
                pad_high = int((nb_frames - nb_steps + 1) / 2 - ((nb_frames - nb_steps) % 2))
                om = np.concatenate((om[0] + np.arange(-pad_low, 0, 1) * tilt_angle,
                                     om,
                                     om[-1] + np.arange(1, pad_high + 1, 1) * tilt_angle), axis=0)
            if nb_steps > nb_frames:  # data has been cropped, we suppose it is centered in z dimension
                om = om[(nb_steps - nb_frames) // 2: (nb_steps + nb_frames) // 2]

        elif setup.rocking_angle == 'inplane':  # phi rocking curve
            nb_steps = len(phi)
            tilt_angle = phi[1] - phi[0]

            if nb_steps < nb_frames:  # data has been padded, we suppose it is centered in z dimension
                pad_low = int((nb_frames - nb_steps + ((nb_frames - nb_steps) % 2)) / 2)
                pad_high = int((nb_frames - nb_steps + 1) / 2 - ((nb_frames - nb_steps) % 2))
                phi = np.concatenate((phi[0] + np.arange(-pad_low, 0, 1) * tilt_angle,
                                      phi,
                                      phi[-1] + np.arange(1, pad_high + 1, 1) * tilt_angle), axis=0)
            if nb_steps > nb_frames:  # data has been cropped, we suppose it is centered in z dimension
                phi = phi[(nb_steps - nb_frames) // 2: (nb_steps + nb_frames) // 2]

        else:
            raise ValueError('Wrong value for "rocking_angle" parameter')

        qx, qy, qz = hxrd.Ang2Q.area(mu, om, chi, phi, gamma, delta, en=setup.energy, delta=detector.offsets)

    else:
        raise ValueError('Wrong value for "beamline" parameter: beamline not supported')

    return qx, qz, qy, frames_logical


def remove_hotpixels(data, mask, hotpixels=None):
    """
    Remove hot pixels from CCD frames and update the mask

    :param data: 2D or 3D array
    :param hotpixels: 2D array of hotpixels. 1 for a hotpixel, 0 for normal pixels.
    :param mask: array of the same shape as data
    :return: the data without hotpixels and the updated mask
    """
    if hotpixels is None:
        hotpixels = np.zeros(data.shape)
    if hotpixels.ndim == 3:  # 3D array
        print('Hotpixels is a 3D array, summing along the first axis')
        hotpixels = hotpixels.sum(axis=0)
        hotpixels[np.nonzero(hotpixels)] = 1  # hotpixels should be a binary array

    if data.shape != mask.shape:
        raise ValueError('Data and mask must have the same shape\n data is ', data.shape, ' while mask is ', mask.shape)

    if data.ndim == 3:  # 3D array
        if data[0, :, :].shape != hotpixels.shape:
            raise ValueError('Data and hotpixels must have the same shape\n data is ',
                             data.shape, ' while hotpixels is ', hotpixels.shape)
        for idx in range(data.shape[0]):
            temp_data = data[idx, :, :]
            temp_mask = mask[idx, :, :]
            temp_data[hotpixels == 1] = 0  # numpy array is mutable hence data will be modified
            temp_mask[hotpixels == 1] = 1  # numpy array is mutable hence mask will be modified
    elif data.ndim == 2:  # 2D array
        if data.shape != hotpixels.shape:
            raise ValueError('Data and hotpixels must have the same shape\n data is ',
                             data.shape, ' while hotpixels is ', hotpixels.shape)
        data[hotpixels == 1] = 0
        mask[hotpixels == 1] = 1
    else:
        raise ValueError('2D or 3D data array expected, got ', data.ndim, 'D')
    return data, mask


def smaller_primes(number, maxprime=13, required_dividers=(4,)):
    """
    Find the closest integer <=n (or list/array of integers), for which the largest prime divider is <=maxprime,
    and has to include some dividers. The default values for maxprime is the largest integer accepted
    by the clFFT library for OpenCL GPU FFT. Adapted from PyNX.

    :param number: the integer number
    :param maxprime: the largest prime factor acceptable
    :param required_dividers: a list of required dividers for the returned integer.
    :return: the integer (or list/array of integers) fulfilling the requirements
    """
    if (type(number) is list) or (type(number) is tuple) or (type(number) is np.ndarray):
        vn = []
        for i in number:
            assert (i > 1 and maxprime <= i)
            while try_smaller_primes(i, maxprime=maxprime, required_dividers=required_dividers) is False:
                i = i - 1
                if i == 0:
                    return 0
            vn.append(i)
        if type(number) is np.ndarray:
            return np.array(vn)
        return vn
    else:
        assert (number > 1 and maxprime <= number)
        while try_smaller_primes(number, maxprime=maxprime, required_dividers=required_dividers) is False:
            number = number - 1
            if number == 0:
                return 0
        return number


def try_smaller_primes(number, maxprime=13, required_dividers=(4,)):
    """
    Check if the largest prime divider is <=maxprime, and optionally includes some dividers. Adapted from PyNX.

    :param number: the integer number for which the prime decomposition will be checked
    :param maxprime: the maximum acceptable prime number. This defaults to the largest integer accepted by the clFFT
        library for OpenCL GPU FFT.
    :param required_dividers: list of required dividers in the prime decomposition. If None, this check is skipped.
    :return: True if the conditions are met.
    """
    p = primes(number)
    if max(p) > maxprime:
        return False
    if required_dividers is not None:
        for k in required_dividers:
            if number % k != 0:
                return False
    return True


def update_aliens(key, pix, piy, original_data, updated_data, updated_mask, figure, width, dim, idx,
                  vmax, vmin=0):
    """
    Update the plot while removing the parasitic diffraction intensity in 3D dataset

    :param key: the keyboard key which was pressed
    :param pix: the x value of the mouse pointer
    :param piy: the y value of the mouse pointer
    :param original_data: the 3D data array before masking aliens
    :param updated_data: the current 3D data array
    :param updated_mask: the current 3D mask array
    :param figure: the figure instance
    :param width: the half_width of the masking window
    :param dim: the axis currently under review (axis 0, 1 or 2)
    :param idx: the frame index in the current axis
    :param vmax: the higher boundary for the colorbar
    :param vmin: the lower boundary for the colorbar
    :return: updated data, mask and controls
    """
    if original_data.ndim != 3 or updated_data.ndim != 3 or updated_mask.ndim != 3:
        raise ValueError('original_data, updated_data and updated_mask should be 3D arrays')

    nbz, nby, nbx = original_data.shape
    stop_masking = False
    if dim > 2:
        raise ValueError('dim should be 0, 1 or 2')

    if key == 'u':
        idx = idx + 1
        figure.clear()
        if dim == 0:
            if idx > nbz - 1:
                idx = 0
            plt.imshow(updated_data[idx, :, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbz) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 1:
            if idx > nby - 1:
                idx = 0
            plt.imshow(updated_data[:, idx, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nby) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 2:
            if idx > nbx - 1:
                idx = 0
            plt.imshow(updated_data[:, :, idx], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbx) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'd':
        idx = idx - 1
        figure.clear()
        if dim == 0:
            if idx < 0:
                idx = nbz - 1
            plt.imshow(updated_data[idx, :, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbz) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 1:
            if idx < 0:
                idx = nby - 1
            plt.imshow(updated_data[:, idx, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nby) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 2:
            if idx < 0:
                idx = nbx - 1
            plt.imshow(updated_data[:, :, idx], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbx) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'up':
        width = width + 1
        print('width: ', width)

    elif key == 'down':
        width = width - 1
        if width < 0:
            width = 0
        print('width: ', width)

    elif key == 'right':
        vmax = vmax * 2
        print('vmax: ', vmax)
        figure.clear()
        if dim == 0:
            plt.imshow(updated_data[idx, :, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbz) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 1:
            plt.imshow(updated_data[:, idx, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nby) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 2:
            plt.imshow(updated_data[:, :, idx], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbx) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'left':
        vmax = vmax / 2
        if vmax < 1:
            vmax = 1
        print('vmax: ', vmax)
        figure.clear()
        if dim == 0:
            plt.imshow(updated_data[idx, :, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbz) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 1:
            plt.imshow(updated_data[:, idx, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nby) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 2:
            plt.imshow(updated_data[:, :, idx], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbx) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'm':
        figure.clear()
        if (piy - width) < 0:
            starty = 0
        else:
            starty = piy - width
        if (pix - width) < 0:
            startx = 0
        else:
            startx = pix - width
        if dim == 0:
            updated_data[idx, starty:piy + width + 1, startx:pix + width + 1] = 0
            updated_mask[idx, starty:piy + width + 1, startx:pix + width + 1] = 1
            plt.imshow(updated_data[idx, :, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbz) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 1:
            updated_data[starty:piy + width + 1, idx, startx:pix + width + 1] = 0
            updated_mask[starty:piy + width + 1, idx, startx:pix + width + 1] = 1
            plt.imshow(updated_data[:, idx, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nby) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 2:
            updated_data[starty:piy + width + 1, startx:pix + width + 1, idx] = 0
            updated_mask[starty:piy + width + 1, startx:pix + width + 1, idx] = 1
            plt.imshow(updated_data[:, :, idx], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbx) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'b':
        figure.clear()
        if (piy - width) < 0:
            starty = 0
        else:
            starty = piy - width
        if (pix - width) < 0:
            startx = 0
        else:
            startx = pix - width
        if dim == 0:
            updated_data[idx, starty:piy + width + 1, startx:pix + width + 1] = \
                original_data[idx, starty:piy + width + 1, startx:pix + width + 1]
            updated_mask[idx, starty:piy + width + 1, startx:pix + width + 1] = 0
            plt.imshow(updated_data[idx, :, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbz) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 1:
            updated_data[starty:piy + width + 1, idx, startx:pix + width + 1] = \
                original_data[starty:piy + width + 1, idx, startx:pix + width + 1]
            updated_mask[starty:piy + width + 1, idx, startx:pix + width + 1] = 0
            plt.imshow(updated_data[:, idx, :], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nby) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        elif dim == 2:
            updated_data[starty:piy + width + 1, startx:pix + width + 1, idx] = \
                original_data[starty:piy + width + 1, startx:pix + width + 1, idx]
            updated_mask[starty:piy + width + 1, startx:pix + width + 1, idx] = 0
            plt.imshow(updated_data[:, :, idx], vmin=vmin, vmax=vmax)
            plt.title("Frame " + str(idx + 1) + "/" + str(nbx) + "\n"
                      "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                      "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'q':
        stop_masking = True

    return updated_data, updated_mask, width, vmax, idx, stop_masking


def update_aliens_2d(key, pix, piy, original_data, updated_data, updated_mask, figure, width,
                     vmax, vmin=0):
    """
    Update the plot while removing the parasitic diffraction intensity in 2D dataset

    :param key: the keyboard key which was pressed
    :param pix: the x value of the mouse pointer
    :param piy: the y value of the mouse pointer
    :param original_data: the 2D data array before masking aliens
    :param updated_data: the current 2D data array
    :param updated_mask: the current 2D mask array
    :param figure: the figure instance
    :param width: the half_width of the masking window
    :param vmax: the higher boundary for the colorbar
    :param vmin: the lower boundary for the colorbar
    :return: updated data, mask and controls
    """
    if original_data.ndim != 2 or updated_data.ndim != 2 or updated_mask.ndim != 2:
        raise ValueError('original_data, updated_data and updated_mask should be 2D arrays')

    stop_masking = False

    if key == 'up':
        width = width + 1
        print('width: ', width)

    elif key == 'down':
        width = width - 1
        if width < 0:
            width = 0
        print('width: ', width)

    elif key == 'right':
        vmax = vmax * 2
        print('vmax: ', vmax)
        figure.clear()

        plt.imshow(updated_data, vmin=vmin, vmax=vmax)
        plt.title("m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'left':
        vmax = vmax / 2
        if vmax < 1:
            vmax = 1
        print('vmax: ', vmax)
        figure.clear()

        plt.imshow(updated_data, vmin=vmin, vmax=vmax)
        plt.title("m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'm':
        figure.clear()
        if (piy - width) < 0:
            starty = 0
        else:
            starty = piy - width
        if (pix - width) < 0:
            startx = 0
        else:
            startx = pix - width

        updated_data[starty:piy + width + 1, startx:pix + width + 1] = 0
        updated_mask[starty:piy + width + 1, startx:pix + width + 1] = 1
        plt.imshow(updated_data, vmin=vmin, vmax=vmax)
        plt.title("m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'b':
        figure.clear()
        if (piy - width) < 0:
            starty = 0
        else:
            starty = piy - width
        if (pix - width) < 0:
            startx = 0
        else:
            startx = pix - width

        updated_data[starty:piy + width + 1, startx:pix + width + 1] = \
            original_data[starty:piy + width + 1, startx:pix + width + 1]
        updated_mask[starty:piy + width + 1, startx:pix + width + 1] = 0
        plt.imshow(updated_data, vmin=vmin, vmax=vmax)
        plt.title("m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'q':
        stop_masking = True

    return updated_data, updated_mask, width, vmax, stop_masking


def update_mask(key, pix, piy, original_data, original_mask, updated_data, updated_mask, figure, flag_pause, points,
                xy, width, dim, vmax, vmin=0, masked_color=0.1):
    """
    Update the mask to remove parasitic diffraction intensity and hotpixels in 3D dataset.

    :param key: the keyboard key which was pressed
    :param pix: the x value of the mouse pointer
    :param piy: the y value of the mouse pointer
    :param original_data: the 3D data array before masking
    :param original_mask: the 3D mask array before masking
    :param updated_data: the current 3D data array
    :param updated_mask: the temporary 2D mask array with updated points
    :param figure: the figure instance
    :param flag_pause: set to 1 to stop registering vertices using mouse clicks
    :param points: list of all point coordinates: points=np.stack((x, y), axis=0).T with x=x.flatten() , y = y.flatten()
     given x,y=np.meshgrid(np.arange(nx), np.arange(ny))
    :param xy: the list of vertices which defines a polygon to be masked
    :param width: the half_width of the masking window
    :param dim: the axis currently under review (axis 0, 1 or 2)
    :param vmax: the higher boundary for the colorbar
    :param vmin: the lower boundary for the colorbar
    :param masked_color: the value that detector gaps should have in plots
    :return: updated data, mask and controls
    """
    if original_data.ndim != 3 or updated_data.ndim != 3 or original_mask.ndim != 3:
        raise ValueError('original_data, updated_data and original_mask should be 3D arrays')
    if updated_mask.ndim != 2:
        raise ValueError('updated_mask should be 2D arrays')

    nbz, nby, nbx = original_data.shape
    stop_masking = False
    if dim != 0 and dim != 1 and dim != 2:
        raise ValueError('dim should be 0, 1 or 2')

    if key == 'up':
        width = width + 1
        print('width: ', width)

    elif key == 'down':
        width = width - 1
        if width < 0:
            width = 0
        print('width: ', width)

    elif key == 'right':
        vmax = vmax + 1
        print('vmax: ', vmax)
        array = updated_data.sum(axis=dim)
        array[updated_mask == 1] = masked_color
        myfig = plt.gcf()
        myaxs = myfig.gca()
        xmin, xmax = myaxs.get_xlim()
        ymin, ymax = myaxs.get_ylim()
        figure.clear()
        plt.imshow(np.log10(abs(array)), vmin=vmin, vmax=vmax)
        myaxs = myfig.gca()
        myaxs.set_xlim([xmin, xmax])
        myaxs.set_ylim([ymin, ymax])
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'left':
        vmax = vmax - 1
        if vmax < 1:
            vmax = 1
        print('vmax: ', vmax)
        array = updated_data.sum(axis=dim)
        array[updated_mask == 1] = masked_color
        myfig = plt.gcf()
        myaxs = myfig.gca()
        xmin, xmax = myaxs.get_xlim()
        ymin, ymax = myaxs.get_ylim()
        figure.clear()
        plt.imshow(np.log10(abs(array)), vmin=vmin, vmax=vmax)
        myaxs = myfig.gca()
        myaxs.set_xlim([xmin, xmax])
        myaxs.set_ylim([ymin, ymax])
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'm':
        if (piy - width) < 0:
            starty = 0
        else:
            starty = piy - width
        if (pix - width) < 0:
            startx = 0
        else:
            startx = pix - width
        updated_mask[starty:piy + width + 1, startx:pix + width + 1] = 1
        array = updated_data.sum(axis=dim)
        array[updated_mask == 1] = masked_color
        myfig = plt.gcf()
        myaxs = myfig.gca()
        xmin, xmax = myaxs.get_xlim()
        ymin, ymax = myaxs.get_ylim()
        figure.clear()
        plt.imshow(np.log10(abs(array)), vmin=vmin, vmax=vmax)
        myaxs = myfig.gca()
        myaxs.set_xlim([xmin, xmax])
        myaxs.set_ylim([ymin, ymax])
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'b':
        if (piy - width) < 0:
            starty = 0
        else:
            starty = piy - width
        if (pix - width) < 0:
            startx = 0
        else:
            startx = pix - width
        updated_mask[starty:piy + width + 1, startx:pix + width + 1] = 0
        array = updated_data.sum(axis=dim)
        array[updated_mask == 1] = masked_color
        myfig = plt.gcf()
        myaxs = myfig.gca()
        xmin, xmax = myaxs.get_xlim()
        ymin, ymax = myaxs.get_ylim()
        figure.clear()
        plt.imshow(np.log10(abs(array)), vmin=vmin, vmax=vmax)
        myaxs = myfig.gca()
        myaxs.set_xlim([xmin, xmax])
        myaxs.set_ylim([ymin, ymax])
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'a':  # restart mask from beginning
        updated_data = np.copy(original_data)
        xy = []
        print('restart masking')
        if dim == 0:
            updated_data[
                original_mask == 1] = masked_color / nbz  # masked pixels plotted with the value of masked_pixel
            updated_mask = np.zeros((nby, nbx))
        if dim == 1:
            updated_data[
                original_mask == 1] = masked_color / nby  # masked pixels plotted with the value of masked_pixel
            updated_mask = np.zeros((nbz, nbx))
        if dim == 2:
            updated_data[
                original_mask == 1] = masked_color / nbx  # masked pixels plotted with the value of masked_pixel
            updated_mask = np.zeros((nbz, nby))
        figure.clear()
        plt.imshow(np.log10(abs(updated_data.sum(axis=dim))), vmin=0, vmax=vmax)
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'p':  # plot masked image
        if len(xy) != 0:
            xy.append(xy[0])
            print(xy)
            if dim == 0:
                ind = Path(np.array(xy)).contains_points(points).reshape((nby, nbx))
            elif dim == 1:
                ind = Path(np.array(xy)).contains_points(points).reshape((nbz, nbx))
            else:  # dim=2
                ind = Path(np.array(xy)).contains_points(points).reshape((nbz, nby))
            updated_mask[ind] = 1
        array = updated_data.sum(axis=dim)
        array[updated_mask == 1] = masked_color
        xy = []  # allow to mask a different area
        figure.clear()
        plt.imshow(np.log10(abs(array)), vmin=vmin, vmax=vmax)
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()
        thismanager = plt.get_current_fig_manager()
        thismanager.toolbar.pan()  # deactivate the pan
    elif key == 'x':
        if not flag_pause:
            flag_pause = True
            print('pause for pan/zoom')
        else:
            flag_pause = False
            print('resume masking')

    elif key == 'q':
        stop_masking = True

    return updated_data, updated_mask, flag_pause, xy, width, vmax, stop_masking


def update_mask_2d(key, pix, piy, original_data, original_mask, updated_data, updated_mask, figure, flag_pause, points,
                   xy, width, vmax, vmin=0, masked_color=0.1):
    """
    Update the mask to remove parasitic diffraction intensity and hotpixels for 2d dataset.

    :param key: the keyboard key which was pressed
    :param pix: the x value of the mouse pointer
    :param piy: the y value of the mouse pointer
    :param original_data: the 2D data array before masking
    :param original_mask: the 2D mask array before masking
    :param updated_data: the current 2D data array
    :param updated_mask: the temporary 2D mask array with updated points
    :param figure: the figure instance
    :param flag_pause: set to 1 to stop registering vertices using mouse clicks
    :param points: list of all point coordinates: points=np.stack((x, y), axis=0).T with x=x.flatten() , y = y.flatten()
     given x,y=np.meshgrid(np.arange(nx), np.arange(ny))
    :param xy: the list of vertices which defines a polygon to be masked
    :param width: the half_width of the masking window
    :param vmax: the higher boundary for the colorbar
    :param vmin: the lower boundary for the colorbar
    :param masked_color: the value that detector gaps should have in plots
    :return: updated data, mask and controls
    """
    if original_data.ndim != 2 or updated_data.ndim != 2 or original_mask.ndim != 2 or updated_mask.ndim != 2:
        raise ValueError('original_data, updated_data, original_mask and updated_mask should be 2D arrays')

    nby, nbx = original_data.shape
    stop_masking = False

    if key == 'up':
        width = width + 1
        print('width: ', width)

    elif key == 'down':
        width = width - 1
        if width < 0:
            width = 0
        print('width: ', width)

    elif key == 'right':
        vmax = vmax + 1
        print('vmax: ', vmax)
        updated_data[updated_mask == 1] = masked_color
        myfig = plt.gcf()
        myaxs = myfig.gca()
        xmin, xmax = myaxs.get_xlim()
        ymin, ymax = myaxs.get_ylim()
        figure.clear()
        plt.imshow(np.log10(abs(updated_data)), vmin=vmin, vmax=vmax)
        myaxs = myfig.gca()
        myaxs.set_xlim([xmin, xmax])
        myaxs.set_ylim([ymin, ymax])
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'left':
        vmax = vmax - 1
        if vmax < 1:
            vmax = 1
        print('vmax: ', vmax)
        updated_data[updated_mask == 1] = masked_color
        myfig = plt.gcf()
        myaxs = myfig.gca()
        xmin, xmax = myaxs.get_xlim()
        ymin, ymax = myaxs.get_ylim()
        figure.clear()
        plt.imshow(np.log10(abs(updated_data)), vmin=vmin, vmax=vmax)
        myaxs = myfig.gca()
        myaxs.set_xlim([xmin, xmax])
        myaxs.set_ylim([ymin, ymax])
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'm':
        if (piy - width) < 0:
            starty = 0
        else:
            starty = piy - width
        if (pix - width) < 0:
            startx = 0
        else:
            startx = pix - width
        updated_mask[starty:piy + width + 1, startx:pix + width + 1] = 1
        updated_data[updated_mask == 1] = masked_color
        myfig = plt.gcf()
        myaxs = myfig.gca()
        xmin, xmax = myaxs.get_xlim()
        ymin, ymax = myaxs.get_ylim()
        figure.clear()
        plt.imshow(np.log10(abs(updated_data)), vmin=vmin, vmax=vmax)
        myaxs = myfig.gca()
        myaxs.set_xlim([xmin, xmax])
        myaxs.set_ylim([ymin, ymax])
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'b':
        if (piy - width) < 0:
            starty = 0
        else:
            starty = piy - width
        if (pix - width) < 0:
            startx = 0
        else:
            startx = pix - width
        updated_mask[starty:piy + width + 1, startx:pix + width + 1] = 0
        updated_data[updated_mask == 1] = masked_color
        myfig = plt.gcf()
        myaxs = myfig.gca()
        xmin, xmax = myaxs.get_xlim()
        ymin, ymax = myaxs.get_ylim()
        figure.clear()
        plt.imshow(np.log10(abs(updated_data)), vmin=vmin, vmax=vmax)
        myaxs = myfig.gca()
        myaxs.set_xlim([xmin, xmax])
        myaxs.set_ylim([ymin, ymax])
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'a':  # restart mask from beginning
        updated_data = np.copy(original_data)
        xy = []
        print('restart masking')

        updated_data[
            original_mask == 1] = masked_color  # masked pixels plotted with the value of masked_pixel
        updated_mask = np.zeros((nby, nbx))

        figure.clear()
        plt.imshow(np.log10(abs(updated_data)), vmin=0, vmax=vmax)
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()

    elif key == 'p':  # plot masked image
        if len(xy) != 0:
            xy.append(xy[0])
            print(xy)
            ind = Path(np.array(xy)).contains_points(points).reshape((nby, nbx))
            updated_mask[ind] = 1

        updated_data[updated_mask == 1] = masked_color
        xy = []  # allow to mask a different area
        figure.clear()
        plt.imshow(np.log10(abs(updated_data)), vmin=vmin, vmax=vmax)
        plt.title('x to pause/resume masking for pan/zoom \n'
                  'p plot mask ; a restart ; click to select vertices\n'
                  "m mask ; b unmask ; q quit ; u next frame ; d previous frame\n"
                  "up larger ; down smaller ; right darker ; left brighter")
        plt.draw()
        thismanager = plt.get_current_fig_manager()
        thismanager.toolbar.pan()  # deactivate the pan
    elif key == 'x':
        if not flag_pause:
            flag_pause = True
            print('pause for pan/zoom')
        else:
            flag_pause = False
            print('resume masking')

    elif key == 'q':
        stop_masking = True

    return updated_data, updated_mask, flag_pause, xy, width, vmax, stop_masking


def zero_pad(array, padding_width=np.array([0, 0, 0, 0, 0, 0]), mask_flag=False, debugging=False):
    """
    Pad obj with zeros.

    :param array: 3D array to be padded
    :param padding_width: number of zero pixels to padd on each side
    :param mask_flag: set to True to pad with 1, False to pad with 0
    :type mask_flag: bool
    :param debugging: set to True to see plots
    :type debugging: bool
    :return: obj padded with zeros
    """
    if array.ndim != 3:
        raise ValueError('3D Array expected, got ', array.ndim, 'D')

    nbz, nby, nbx = array.shape
    padding_z0 = padding_width[0]
    padding_z1 = padding_width[1]
    padding_y0 = padding_width[2]
    padding_y1 = padding_width[3]
    padding_x0 = padding_width[4]
    padding_x1 = padding_width[5]
    if debugging:
        gu.multislices_plot(array=array, sum_frames=False, invert_yaxis=True, plot_colorbar=True, vmin=0, vmax=1,
                            title='Array before padding')

    if mask_flag:
        newobj = np.ones((nbz + padding_z0 + padding_z1, nby + padding_y0 + padding_y1, nbx + padding_x0 + padding_x1))
    else:
        newobj = np.zeros((nbz + padding_z0 + padding_z1, nby + padding_y0 + padding_y1, nbx + padding_x0 + padding_x1))
    newobj[padding_z0:padding_z0 + nbz, padding_y0:padding_y0 + nby, padding_x0:padding_x0 + nbx] = array
    if debugging:
        gu.multislices_plot(array=newobj, sum_frames=False, invert_yaxis=True, plot_colorbar=True, vmin=0, vmax=1,
                            title='Array after padding')
    return newobj


if __name__ == "__main__":
    data = np.ones((12, 50, 40))
    nz, ny, nx = data.shape
    mask = np.zeros((12, 50, 40))
    import bcdi.experiment.experiment_utils as exp
    from mayavi import mlab
    setup = exp.SetupPreprocessing(beamline='P10', energy=8700, rocking_angle='inplane', angular_step=20,
                                   distance=5100)
    data, mask = grid_cdi(data, mask, setup)

    grid_qx, grid_qz, grid_qy = np.mgrid[np.arange(-nz//2, nz//2), np.arange(-ny//2, ny//2),
                                np.arange(-nx//2, nx//2)]
    # in nexus convention, z is downstream, y vertical and x outboard
    # but with Q, Qx is downstream, Qz vertical and Qy outboard
    mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
    mlab.contour3d((grid_qx, grid_qz, grid_qy, data), contours=20, opacity=0.5, colormap="jet")
    mlab.colorbar(orientation="vertical", nb_labels=6)
    mlab.outline(line_width=2.0)
    mlab.axes(xlabel='Qx', ylabel='Qz', zlabel='Qy')  #
    mlab.show()

