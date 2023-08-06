# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-present : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.measurements import center_of_mass
import pathlib
import vtk
from vtk.util import numpy_support
import os
import tkinter as tk
from tkinter import filedialog
from skimage import measure
import logging
import sys
import gc
sys.path.append('//win.desy.de/home/carnisj/My Documents/myscripts/bcdi/')
import bcdi.graph.graph_utils as gu
import bcdi.facet_recognition.facet_utils as fu
import bcdi.postprocessing.postprocessing_utils as pu

helptext = """
Script for detecting facets on a 3D crytal reconstructed by a phasing algorithm (Bragg CDI) and making some statistics
 about strain by facet. The correct isosurface value should be given as input.

Input: a reconstruction .npz file with fields: 'amp' and 'strain' 
Output: a log file with strain statistics by plane, a VTK file for 3D visualization of detected planes.
"""

scan = 2227  # spec scan number
datadir = 'D:/data/PtRh/PtRh(103x98x157)/'
# datadir = "C:/Users/carnis/Work Folders/Documents/data/CH4760_Pt/S"+str(scan)+"/simu/new_model/"
support_threshold = 0.55  # threshold for support determination
savedir = datadir + "isosurface_" + str(support_threshold) + "/"
# datadir = "C:/Users/carnis/Work Folders/Documents/data/CH4760_Pt/S"+str(scan)+"/pynxraw/"
# datadir = "C:/Users/carnis/Work Folders/Documents/data/CH5309/data/S"+str(scan)+"/pynxraw/"
reflection = np.array([1, 1, 1])  # measured crystallographic reflection
debug = False  # set to True to see all plots for debugging
smoothing_iterations = 10  # number of iterations in Taubin smoothing
smooth_lamda = 0.5  # lambda parameter in Taubin smoothing
smooth_mu = 0.51  # mu parameter in Taubin smoothing
projection_method = 'stereographic'  # 'stereographic' or 'equirectangular'
my_min_distance = 20  # pixel separation between peaks in corner_peaks()
max_distance_plane = 0.90  # in pixels, maximum allowed distance to the facet plane of a voxel
#########################################################
# parameters only used in the stereographic projection #
#########################################################
threshold_stereo = -1000  # threshold for defining the background in the density estimation of normals
max_angle = 95  # maximum angle in degree of the stereographic projection (should be larger than 90)
#########################################################
# parameters only used in the equirectangular projection #
#########################################################
bw_method = 0.03  # bandwidth in the gaussian kernel density estimation
kde_threshold = -0.2  # threshold for defining the background in the density estimation of normals
##############################################################################################
# define crystallographic planes of interest for the stereographic projection (cubic lattice #
##############################################################################################
planes = dict()  # create dictionnary
planes['1 0 0'] = fu.plane_angle_cubic(reflection, np.array([1, 0, 0]))
planes['1 1 0'] = fu.plane_angle_cubic(reflection, np.array([1, 1, 0]))
planes['1 -1 1'] = fu.plane_angle_cubic(reflection, np.array([1, -1, 1]))
planes['2 1 0'] = fu.plane_angle_cubic(reflection, np.array([2, 1, 0]))
planes['2 -1 0'] = fu.plane_angle_cubic(reflection, np.array([2, -1, 0]))
planes['3 2 1'] = fu.plane_angle_cubic(reflection, np.array([3, 2, 1]))
planes['4 0 -1'] = fu.plane_angle_cubic(reflection, np.array([4, 0, -1]))
planes['5 2 0'] = fu.plane_angle_cubic(reflection, np.array([5, 2, 0]))
planes['5 2 1'] = fu.plane_angle_cubic(reflection, np.array([5, 2, 1]))
planes['5 -2 -1'] = fu.plane_angle_cubic(reflection, np.array([5, -2, -1]))
##########################
# end of user parameters #
##########################

###########################################################
# create directory and initialize error logger #
###########################################################
pathlib.Path(savedir).mkdir(parents=True, exist_ok=True)
logger = logging.getLogger()

###################
# define colormap #
###################
colormap = gu.Colormap()
my_cmap = colormap.cmap

#############
# load data #
#############
plt.ion()
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir=datadir, filetypes=[("NPZ", "*.npz")])
npzfile = np.load(file_path)
amp = npzfile['amp']
amp = amp / amp.max()
nz, ny, nx = amp.shape
print("Initial data size: (", nz, ',', ny, ',', nx, ')')
strain = npzfile['strain']

# define the support and the surface layer
support = np.zeros(amp.shape)
support[amp > support_threshold*amp.max()] = 1
coordination_matrix = pu.calc_coordination(support, kernel=np.ones((3, 3, 3)), debugging=False)
surface = np.copy(support)
surface[coordination_matrix > 22] = 0  # remove the bulk 22


# Use marching cubes to obtain the surface mesh of these ellipsoids
vertices_old, faces, _, _ = measure.marching_cubes_lewiner(amp, level=support_threshold, step_size=1)
nb_vertices = vertices_old.shape[0]
# vertices is a list of 3d coordinates of all vertices points
# faces is a list of facets defined by the indices of 3 vertices

# from scipy.io import savemat
# savemat('//win.desy.de/home/carnisj/My Documents/MATLAB/TAUBIN/vertices.mat', {'V': vertices_old})
# savemat('//win.desy.de/home/carnisj/My Documents/MATLAB/TAUBIN/faces.mat', {'F': faces})

# Display mesh before smoothing
if debug:
    gu.plot_3dmesh(vertices_old, faces, (nz, ny, nx), title='Mesh after marching cubes')
    plt.ion()

# smooth the mesh using taubin_smooth
vertices_new, normals, areas, color, _ = \
    fu.taubin_smooth(faces, vertices_old, iterations=smoothing_iterations, lamda=smooth_lamda, mu=smooth_mu,
                     debugging=1)

# Display smoothed triangular mesh
if debug:
    gu.plot_3dmesh(vertices_new, faces, (nz, ny, nx), title='Mesh after Taubin smoothing')
    plt.ion()

del vertices_new
gc.collect()

nb_normals = normals.shape[0]
if projection_method == 'stereographic':
    labels_top, labels_bottom, stereo_proj = fu.stereographic_proj(normals=normals, color=color, weights=areas,
                                                                   background_threshold=threshold_stereo,
                                                                   min_distance=my_min_distance, savedir=savedir,
                                                                   save_txt=False, planes=planes, plot_planes=True,
                                                                   max_angle=max_angle, debugging=debug)
    numy, numx = labels_top.shape  # identical to labels_bottom.shape
    if stereo_proj.shape[0] != nb_normals:
        print('incompatible number of normals')
        sys.exit()

    # look for potentially duplicated labels (labels crossing the 90 degree circle)
    duplicated_label = [0]  # it will store bottom_labels which are duplicate from top_labels
    for label in range(1, labels_top.max()+1, 1):
        label_points = np.argwhere(labels_top == label)
        label_points[:, 0] = (label_points[:, 0] * 2*max_angle / numy) - max_angle  # rescale to [-max_angle max_angle]
        label_points[:, 1] = (label_points[:, 1] * 2*max_angle / numx) - max_angle  # rescale to [-max_angle max_angle]

        label_distances = np.sqrt(label_points[:, 0]**2 + label_points[:, 1]**2)
        if (label_distances < 90).sum() < label_points.shape[0]:  # some points on the other side of the 90deg border
            print('Label ', str(label), 'is potentially duplicated')
            # look for the corresponding label in the bottom projection
            for idx in range(nb_normals):
                if 85 < np.sqrt(stereo_proj[idx, 0]**2 + stereo_proj[idx, 1]**2) < 90:  # point near the 90deg border
                    # calculate the corresponding index coordinates
                    # by rescaling from [-max_angle max_angle] to [0 numy] or [0 numx]
                    u_top = int((stereo_proj[idx, 0] + max_angle) * numy / (2*max_angle))
                    v_top = int((stereo_proj[idx, 1] + max_angle) * numx / (2*max_angle))
                    u_bottom = int((stereo_proj[idx, 2] + max_angle) * numy / (2*max_angle))
                    v_bottom = int((stereo_proj[idx, 3] + max_angle) * numx / (2*max_angle))
                    try:
                        if labels_top[u_top, v_top] == label and \
                                labels_bottom[u_bottom, v_bottom] not in duplicated_label:
                            # only the first duplicated point will be checked, then the whole bottom_label is changed
                            # and there is no need to checked anymore
                            duplicated_label.append(labels_bottom[u_bottom, v_bottom])
                            print('    Corresponding label=', str(labels_bottom[u_bottom, v_bottom]))
                            labels_bottom[labels_bottom == labels_bottom[u_bottom, v_bottom]] = label
                    except IndexError:
                        continue
    del label_points, label_distances
    gc.collect()

    # reorganize stereo_proj to keep only the projected point which is in the range [-90 90]
    pole_proj = np.zeros((nb_normals, 4), dtype=stereo_proj.dtype)
    # 1st and 2nd columns are coordinates
    # the 3rd column is an indicator for South, North or duplicated facets
    for idx in range(nb_normals):
        if abs(stereo_proj[idx, 0]) > 90 or abs(stereo_proj[idx, 1]) > 90:
            pole_proj[idx, 0:2] = stereo_proj[idx, 2:]  # use values for the projection from North pole
            pole_proj[idx, 2] = 1  # need to use values from labels_bottom (projection from North pole)
        else:
            pole_proj[idx, 0:2] = stereo_proj[idx, 0:2]  # use values for the projection from South pole
            pole_proj[idx, 2] = 0  # need to use values from labels_top (projection from South pole)
    del stereo_proj
    gc.collect()

    # rescale euclidian u axis from [-95 95] to [0 numy]
    pole_proj[:, 0] = (pole_proj[:, 0] + max_angle) * numy / (2*max_angle)
    # rescale euclidian v axis from [-95 95] to [0 numx]
    pole_proj[:, 1] = (pole_proj[:, 1] + max_angle) * numx / (2*max_angle)
    # change pole_proj to an array of integer indices
    coordinates = pole_proj.astype(int)
    max_label = max(labels_top.max(), labels_bottom.max())

    del pole_proj
    gc.collect()

    ##############################################
    # assign back labels to normals and vertices #
    ##############################################
    normals_label = np.zeros(nb_normals, dtype=int)
    vertices_label = np.zeros(nb_vertices, dtype=int)  # the number of vertices is: vertices_new.shape[0]
    for idx in range(nb_normals):
        # check to which label belongs this normal
        if coordinates[idx, 2] == 0:  # use values from labels_top (projection from South pole)
            label_idx = labels_top[coordinates[idx, 0], coordinates[idx, 1]]
        else:  # use values from labels_bottom (projection from North pole)
            label_idx = labels_bottom[coordinates[idx, 0], coordinates[idx, 1]]

        normals_label[idx] = label_idx  # attribute the label to the normal
        vertices_label[faces[idx, :]] = label_idx  # attribute the label to the corresponding vertices

elif projection_method == 'equirectangular':
    labels, longitude_latitude = fu.equirectangular_proj(normals, color, weights=areas, bw_method=bw_method,
                                                         background_threshold=kde_threshold,
                                                         min_distance=my_min_distance, debugging=debug)
    if longitude_latitude.shape[0] != nb_normals:
        print('incompatible number of normals')
        sys.exit()
    numy, numx = labels.shape
    # rescale the horizontal axis from [-pi pi] to [0 numx]
    longitude_latitude[:, 0] = (longitude_latitude[:, 0] + np.pi) * numx / (2 * np.pi)  # longitude
    # rescale the vertical axis from [-pi/2 pi/2] to [0 numy]
    longitude_latitude[:, 1] = (longitude_latitude[:, 1] + np.pi / 2) * numy / np.pi  # latitude
    # change longitude_latitude to an array of integer indices
    coordinates = np.fliplr(longitude_latitude).astype(int)  # put the vertical axis in first position
    max_label = labels.max()

    del longitude_latitude
    gc.collect()

    ##############################################
    # assign back labels to normals and vertices #
    ##############################################
    normals_label = np.zeros(nb_normals, dtype=int)
    vertices_label = np.zeros(nb_vertices, dtype=int)  # the number of vertices is: vertices_new.shape[0]
    for idx in range(nb_normals):
        label_idx = labels[coordinates[idx, 0], coordinates[idx, 1]]
        normals_label[idx] = label_idx  # attribute the label to the normal
        vertices_label[faces[idx, :]] = label_idx  # attribute the label to the corresponding vertices

else:
    print('Invalid value for projection_method')
    sys.exit()

updated_label = []
print('Background: ', str((normals_label == 0).sum()), 'normals')
for idx in range(1, max_label+1):
    print("Facet", str(idx), ': ', str((normals_label == idx).sum()), 'normals detected')
    if (normals_label == idx).sum() != 0:
        updated_label.append(idx)

del normals_label, coordinates
gc.collect()

###############################################
# assign back labels to voxels using vertices #
###############################################
all_planes = np.zeros((nz, ny, nx), dtype=int)
planes_counter = np.zeros((nz, ny, nx), dtype=int)  # check if a voxel is used several times
for idx in range(nb_vertices):
    temp_indices = np.rint(vertices_old[idx, :]).astype(int)
    planes_counter[temp_indices[0], temp_indices[1], temp_indices[2]] = \
        planes_counter[temp_indices[0], temp_indices[1], temp_indices[2]] + 1
    # check duplicated pixels (appearing several times) and remove them if they belong to different planes
    if planes_counter[temp_indices[0], temp_indices[1], temp_indices[2]] > 1:
        if all_planes[temp_indices[0], temp_indices[1], temp_indices[2]] != vertices_label[idx]:
            # belongs to different groups, therefore it is set as background (label 0)
            all_planes[temp_indices[0], temp_indices[1], temp_indices[2]] = 0
    else:  # non duplicated pixel
        all_planes[temp_indices[0], temp_indices[1], temp_indices[2]] = \
                vertices_label[idx]

del planes_counter, vertices_label, vertices_old
gc.collect()

#####################################################
# define surface gradient using a conjugate support #
#####################################################
# this support is 1 outside, 0 inside so that the gradient points towards exterior
support = np.ones((nz, ny, nx))
support[abs(amp) > support_threshold * abs(amp).max()] = 0
zCOM, yCOM, xCOM = center_of_mass(support)
print("COM at (z, y, x): (", str('{:.2f}'.format(zCOM)), ',', str('{:.2f}'.format(yCOM)), ',',
      str('{:.2f}'.format(xCOM)), ')')
gradz, grady, gradx = np.gradient(support, 1)  # support

######################
# define the support #
######################
support = np.zeros((nz, ny, nx))
support[abs(amp) > support_threshold * abs(amp).max()] = 1

######################################
# Initialize log files and .vti file #
######################################
file = open(os.path.join(savedir, "S" + str(scan) + "_planes.dat"), "w")
file.write('{0: <10}'.format('Plane #') + '\t' + '{0: <10}'.format('angle') + '\t' +
           '{0: <10}'.format('points #') + '\t' + '{0: <10}'.format('<strain>') + '\t' +
           '{0: <10}'.format('std dev') + '\t' + '{0: <10}'.format('A (x)') + '\t' +
           '{0: <10}'.format('B (y)') + '\t' + 'C (Ax+By+C=z)' + '\t' + 'normal X' + '\t' +
           'normal Y' + '\t' + 'normal Z' + '\n')
strain_file = open(os.path.join(savedir, "S" + str(scan) + "_strain.dat"), "w")
strain_file.write('{0: <10}'.format('Plane #') + '\t' + '{0: <10}'.format('Z') + '\t' + '{0: <10}'.format('Y') + '\t' +
                  '{0: <10}'.format('X') + '\t' + '{0: <10}'.format('strain')+'\n')


# prepare amp for vti file
amp_array = np.transpose(amp).reshape(amp.size)
amp_array = numpy_support.numpy_to_vtk(amp_array)
image_data = vtk.vtkImageData()
image_data.SetOrigin(0, 0, 0)
image_data.SetSpacing(1, 1, 1)
image_data.SetExtent(0, nz - 1, 0, ny - 1, 0, nx - 1)
pd = image_data.GetPointData()
pd.SetScalars(amp_array)
pd.GetArray(0).SetName("amp")
index_vti = 1

##################################################################
# fit points by a plane, exclude points far away, refine the fit #
##################################################################
for label in updated_label:
    # raw fit including all points
    plane = np.copy(all_planes)
    plane[plane != label] = 0
    plane[plane == label] = 1
    if plane[plane == 1].sum() == 0:  # no points on the plane
        print('Raw fit: no points for plane', label)
        continue
    # Why not using direclty the centroid to find plane equation?
    # Because it does not distinguish pixels coming from different but parallel facets
    coeffs,  plane_indices, errors, stop = fu.fit_plane(plane=plane, label=label, debugging=debug)
    if stop == 1:
        print('No points remaining after raw fit for plane', label)
        continue

    # update plane by filtering out pixels too far from the fit plane
    plane, stop = fu.distance_threshold(fit=coeffs, indices=plane_indices, shape=plane.shape,
                                        max_distance=max_distance_plane)
    if stop == 1:  # no points on the plane
        print('Refined fit: no points for plane', label)
        continue
    else:
        print('Plane', label, ', ', str(plane[plane == 1].sum()), 'points after checking distance to plane')

    if debug:
        gu.scatter_plot(array=np.asarray(plane_indices).T, labels=('x', 'y', 'z'),
                        title='Plane' + str(label) + ' after raw fit')

    ##################
    # grow the facet #
    ##################
    iterate = 0
    while stop == 0:
        previous_nb = plane[plane == 1].sum()
        plane, stop = fu.grow_facet(fit=coeffs, plane=plane, label=label, support=support,
                                    max_distance=max_distance_plane, debugging=debug)
        plane_indices = np.nonzero(plane == 1)
        iterate = iterate + 1
        if plane[plane == 1].sum() == previous_nb:  # no growth anymore, the number of voxels is constant
            break
    grown_points = plane[plane == 1].sum()
    print('Plane ', label, ', ', str(grown_points), 'points after growing facet into support')
    # update plane indices
    plane_indices = np.nonzero(plane)

    if debug:
        gu.scatter_plot(array=np.asarray(plane_indices).T, labels=('x', 'y', 'z'),
                        title='Plane' + str(label) + ' after growing facet into support')
    ##########################################################################################################
    # Look for the surface: correct for the offset between plane equation and the outer shell of the support #
    # Effect of meshing/smoothing: the meshed support is smaller than the initial support #
    #############################################################################################
    # crop the support to a small ROI included in the plane box
    support_indices = np.nonzero(surface[
                                 plane_indices[0].min() - 3:plane_indices[0].max() + 3,
                                 plane_indices[1].min() - 3:plane_indices[1].max() + 3,
                                 plane_indices[2].min() - 3:plane_indices[2].max() + 3])
    sup0 = support_indices[0] + plane_indices[0].min() - 3  # add offset plane_indices[0].min() - 3
    sup1 = support_indices[1] + plane_indices[1].min() - 3  # add offset plane_indices[1].min() - 3
    sup2 = support_indices[2] + plane_indices[2].min() - 3  # add offset plane_indices[2].min() - 3
    plane_normal = np.array([coeffs[0, 0], coeffs[1, 0], -1])  # normal is [a, b, c] if ax+by+cz+d=0

    dist = np.zeros(len(support_indices[0]))
    for point in range(len(support_indices[0])):
        dist[point] = (coeffs[0, 0]*sup0[point] + coeffs[1, 0]*sup1[point] - sup2[point] + coeffs[2, 0]) \
               / np.linalg.norm(plane_normal)
    mean_dist = dist.mean()
    print('Mean distance of plane ', label, ' to outer shell = ' + str('{:.2f}'.format(mean_dist)) + 'pixels')

    dist = np.zeros(len(support_indices[0]))
    for point in range(len(support_indices[0])):
        dist[point] = (coeffs[0, 0]*sup0[point] + coeffs[1, 0]*sup1[point] - sup2[point]
                       + (coeffs[2, 0] - mean_dist / 2)) / np.linalg.norm(plane_normal)
    new_dist = dist.mean()

    step_shift = 0.5  # will scan by half pixel through the crystal in order to not miss voxels
    # these directions are for a mesh smaller than the support
    if mean_dist*new_dist < 0:  # crossed the support surface
        step_shift = np.sign(mean_dist) * step_shift
    elif abs(new_dist) - abs(mean_dist) < 0:
        step_shift = np.sign(mean_dist) * step_shift
    else:  # going away from surface, wrong direction
        step_shift = -1 * np.sign(mean_dist) * step_shift

    step_shift = -1*step_shift  # added JCR 24082018 because the direction of normals was flipped

    common_previous = 0
    found_plane = 0
    nbloop = 1
    crossed_surface = 0
    shift_direction = 0
    while found_plane == 0:
        common_points = 0
        # shift indices
        plane_newindices0, plane_newindices1, plane_newindices2 =\
            fu.offset_plane(indices=plane_indices, offset=nbloop*step_shift, plane_normal=plane_normal)

        for point in range(len(plane_newindices0)):
            for point2 in range(len(sup0)):
                if plane_newindices0[point] == sup0[point2] and plane_newindices1[point] == sup1[point2]\
                        and plane_newindices2[point] == sup2[point2]:
                    common_points = common_points + 1

        if debug:
            tempcoeff2 = coeffs[2, 0] - nbloop * step_shift
            dist = np.zeros(len(support_indices[0]))
            for point in range(len(support_indices[0])):
                dist[point] = (coeffs[0, 0] * sup0[point] + coeffs[1, 0] * sup1[point] - sup2[point] + tempcoeff2) \
                              / np.linalg.norm(plane_normal)
            temp_mean_dist = dist.mean()
            plane = np.zeros(surface.shape)
            plane[plane_newindices0, plane_newindices1, plane_newindices2] = 1

            # plot plane points overlaid with the support
            gu.scatter_plot_overlaid(arrays=(np.concatenate((plane_newindices0[:, np.newaxis],
                                                             plane_newindices1[:, np.newaxis],
                                                             plane_newindices2[:, np.newaxis]), axis=1),
                                             np.concatenate((sup0[:, np.newaxis],
                                                             sup1[:, np.newaxis],
                                                             sup2[:, np.newaxis]), axis=1)),
                                     markersizes=(8, 2), markercolors=('b', 'r'), labels=('x', 'y', 'z'),
                                     title='Plane' + str(label) + ' after shifting facet - iteration' + str(nbloop))

            print('(while) iteration ', nbloop, '- Mean distance of the plane to outer shell = ' +
                  str('{:.2f}'.format(temp_mean_dist)) + '\n pixels - common_points = ', common_points)

        if common_points != 0:
            if common_points >= common_previous:
                found_plane = 0
                common_previous = common_points
                print('(while) iteration ', nbloop, ' - ', common_previous, 'points belonging to the facet for plane ',
                      label)
                nbloop = nbloop + 1
                crossed_surface = 1
            elif common_points < grown_points / 5:  # try to keep enough points for statistics, half step back
                found_plane = 1
                print('Exiting while loop after threshold reached - ', common_previous,
                      'points belonging to the facet for plane ', label, '- next step common points=', common_points)
            else:
                found_plane = 0
                common_previous = common_points
                print('(while) iteration ', nbloop, ' - ', common_previous, 'points belonging to the facet for plane ',
                      label)
                nbloop = nbloop + 1
                crossed_surface = 1
        else:
            if crossed_surface == 1:  # found the outer shell, which is 1 step before
                found_plane = 1
                print('Exiting while loop - ', common_previous, 'points belonging to the facet for plane ', label,
                      '- next step common points=', common_points)
            elif nbloop < 5:
                print('(while) iteration ', nbloop, ' - ', common_previous, 'points belonging to the facet for plane ',
                      label)
                nbloop = nbloop + 1
            else:
                if shift_direction == 1:  # already unsuccessful in the other direction
                    print('No point from support is intersecting the plane ', label)
                    stop = 1
                    break
                else:  # distance to support metric not reliable, start again in the other direction
                    shift_direction = 1
                    print('Shift scanning direction')
                    step_shift = -1 * step_shift
                    nbloop = 1

    if stop == 1:  # no points on the plane
        print('Intersecting with support: no points for plane', label)
        continue

    # go back one step
    coeffs[2, 0] = coeffs[2, 0] - (nbloop-1)*step_shift
    # shift indices
    plane_newindices0, plane_newindices1, plane_newindices2 = \
        fu.offset_plane(indices=plane_indices, offset=(nbloop-1)*step_shift, plane_normal=plane_normal)

    plane = np.zeros(surface.shape)
    plane[plane_newindices0, plane_newindices1, plane_newindices2] = 1

    # use only pixels belonging to the outer shell of the support
    plane = plane * surface

    # plot plane points overlaid with the support
    plane_indices = np.nonzero(plane == 1)
    gu.scatter_plot_overlaid(arrays=(np.asarray(plane_indices).T,
                                     np.concatenate((sup0[:, np.newaxis],
                                                     sup1[:, np.newaxis],
                                                     sup2[:, np.newaxis]), axis=1)),
                             markersizes=(8, 2), markercolors=('b', 'r'), labels=('x', 'y', 'z'),
                             title='Plane' + str(label) + ' after finding the surface\n iteration' +
                                   str(iterate) + '- Points number=' + str(len(plane_indices[0])))

    if plane[plane == 1].sum() == 0:  # no point belongs to the support
        print('Plane ', label, ' , no point belongs to support')
        continue

    #######################################
    # grow again the facet on the surface #
    #######################################
    print('Growing again the facet')
    while stop == 0:
        previous_nb = plane[plane == 1].sum()
        plane, stop = fu.grow_facet(fit=coeffs, plane=plane, label=label, support=support,
                                    max_distance=max_distance_plane, debugging=debug)
        plane_indices = np.nonzero(plane)
        plane = plane * surface  # use only pixels belonging to the outer shell of the support
        if plane[plane == 1].sum() == previous_nb:
            break
    grown_points = plane[plane == 1].sum().astype(int)
    print('Plane ', label, ', ', str(grown_points), 'points after growing facet at the surface\n')

    if debug:
        plane_indices = np.nonzero(plane == 1)
        gu.scatter_plot(array=np.asarray(plane_indices).T, labels=('x', 'y', 'z'),
                        title='Plane' + str(label) + ' after growing facet at the surface\nPoints number='
                              + str(len(plane_indices[0])))

    ################################################################
    # refine plane fit, now we are sure that we are at the surface #
    ################################################################
    coeffs, plane_indices, errors, stop = fu.fit_plane(plane=plane, label=label, debugging=debug)
    if stop == 1:
        print('No points remaining after refined fit for plane', label)
        continue

    # update plane by filtering out pixels too far from the fit plane
    plane, stop = fu.distance_threshold(fit=coeffs, indices=plane_indices, shape=plane.shape,
                                        max_distance=max_distance_plane)
    if stop == 1:  # no points on the plane
        print('Refined fit: no points for plane', label)
        continue
    print('Plane', label, ', ', str(plane[plane == 1].sum()), 'points after refined fit')
    plane_indices = np.nonzero(plane)

    ############################################
    # final growth of the facet on the surface #
    ############################################
    print('Final growth of the facet')
    while stop == 0:
        previous_nb = plane[plane == 1].sum()
        plane, stop = fu.grow_facet(fit=coeffs, plane=plane, label=label, support=support,
                                    max_distance=max_distance_plane, debugging=debug)
        plane = plane * surface  # use only pixels belonging to the outer shell of the support
        plane_indices = np.nonzero(plane)
        if plane[plane == 1].sum() == previous_nb:
            break
    grown_points = plane[plane == 1].sum().astype(int)
    # plot plane points overlaid with the support
    print('Plane ', label, ', ', str(grown_points), 'points after the final growth of the facet\n')

    gu.scatter_plot_overlaid(arrays=(np.asarray(plane_indices).T,
                                     np.concatenate((sup0[:, np.newaxis],
                                                     sup1[:, np.newaxis],
                                                     sup2[:, np.newaxis]), axis=1)),
                             markersizes=(8, 2), markercolors=('b', 'r'), labels=('x', 'y', 'z'),
                             title='Plane' + str(label) + ' final growth at the surface\nPoints number='
                                   + str(len(plane_indices[0])))
    # TODO: create an edge support in order to exclude edge points from planes (this is probably not easy).

    #################################################################
    # calculate quantities of interest and update log and VTK files #
    #################################################################
    # calculate mean gradient
    mean_gradient = np.zeros(3)
    ind_z = plane_indices[0]
    ind_y = plane_indices[1]
    ind_x = plane_indices[2]
    for point in range(len(plane_indices[0])):
        mean_gradient[0] = mean_gradient[0] + (ind_z[point] - zCOM)
        mean_gradient[1] = mean_gradient[1] + (ind_y[point] - yCOM)
        mean_gradient[2] = mean_gradient[2] + (ind_x[point] - xCOM)

    if np.linalg.norm(mean_gradient) == 0:
        print('gradient at surface is 0, cannot determine the correct direction of surface normal')
    else:
        mean_gradient = mean_gradient / np.linalg.norm(mean_gradient)

    # check the correct direction of the normal using the gradient of the support
    ref_direction = np.array([0, 1, 0])  # [111] is vertical
    plane_normal = np.array([coeffs[0, 0], coeffs[1, 0], -1])  # normal is [a, b, c] if ax+by+cz+d=0
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    if np.dot(plane_normal, mean_gradient) < 0:  # normal is in the reverse direction
        print('Flip normal direction plane', str(label),'\n')
        plane_normal = -1 * plane_normal

    # calculate the angle of the plane normal to [111]
    angle_plane = 180 / np.pi * np.arccos(np.dot(ref_direction, plane_normal))

    # calculate the average strain for plane voxels and update the log file
    plane_indices = np.nonzero(plane == 1)
    ind_z = plane_indices[0]
    ind_y = plane_indices[1]
    ind_x = plane_indices[2]
    nb_points = len(plane_indices[0])
    for idx in range(nb_points):
        strain_file.write('{0: <10}'.format(str(label)) + '\t' +
                          '{0: <10}'.format(str(ind_z[idx])) + '\t' +
                          '{0: <10}'.format(str(ind_y[idx])) + '\t' +
                          '{0: <10}'.format(str(ind_x[idx])) + '\t' +
                          '{0: <10}'.format(str('{:.7f}'.format(strain[ind_z[idx], ind_y[idx], ind_x[idx]])))+'\n')

    plane_strain = np.mean(strain[plane == 1])
    plane_deviation = np.std(strain[plane == 1])
    file.write('{0: <10}'.format(str(label)) + '\t' +
               '{0: <10}'.format(str('{:.3f}'.format(angle_plane))) + '\t' +
               '{0: <10}'.format(str(nb_points)) + '\t' +
               '{0: <10}'.format(str('{:.7f}'.format(plane_strain))) + '\t' +
               '{0: <10}'.format(str('{:.7f}'.format(plane_deviation))) + '\t' +
               '{0: <10}'.format(str('{:.5f}'.format(coeffs[0, 0]))) + '\t' +
               '{0: <10}'.format(str('{:.5f}'.format(coeffs[1, 0]))) + '\t' +
               '{0: <10}'.format(str('{:.5f}'.format(coeffs[2, 0]))) + '\t' +
               '{0: <10}'.format(str('{:.5f}'.format(plane_normal[0]))) + '\t' +
               '{0: <10}'.format(str('{:.5f}'.format(plane_normal[1]))) + '\t' +
               '{0: <10}'.format(str('{:.5f}'.format(plane_normal[2]))) + '\n')

    # update vti file
    PLANE = np.transpose(plane).reshape(plane.size)
    plane_array = numpy_support.numpy_to_vtk(PLANE)
    pd.AddArray(plane_array)
    pd.GetArray(index_vti).SetName("plane_"+str(label))
    pd.Update()
    index_vti = index_vti + 1

##########################
# update and close files #
##########################
file.write('\n'+'Isosurface value'+'\t' '{0: <10}'.format(str(support_threshold)))
strain_file.write('\n'+'Isosurface value'+'\t' '{0: <10}'.format(str(support_threshold)))
file.close()
strain_file.close()
# export data to file
writer = vtk.vtkXMLImageDataWriter()
writer.SetFileName(os.path.join(savedir, "S" + str(scan) + "_refined planes.vti"))
writer.SetInputData(image_data)
writer.Write()
print('End of script')
plt.ioff()
plt.show()
