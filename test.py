# import numpy as np
# import matplotlib.pyplot as plt
#
#
# # First create some toy data:
# x = np.linspace(0, 2*np.pi, 400)
# y = np.sin(x**2)
#
# # Create just a figure and only one subplot
# # fig, ax = plt.subplots()
# # ax.plot(x, y)
# # ax.set_title('Simple plot')
# # plt.show()
#
# # Create two subplots and unpack the output array immediately
# # f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
# # ax1.plot(x, y)
# # ax1.set_title('Sharing Y axis')
# # ax2.scatter(x, y)
# # plt.show()
# #
# # # Create four polar axes and access them through the returned array
# fig, axs = plt.subplots(2, 2, subplot_kw=dict(polar=True))
# axs[0, 0].plot(x, y)
# axs[1, 1].scatter(x, y)
# plt.show()
#
# # Share a X axis with each column of subplots
# plt.subplots(2, 2, sharex='col')
# plt.show()
#
# # Share a Y axis with each row of subplots
# plt.subplots(2, 2, sharey='row')
# plt.show()
#
# # Share both X and Y axes with all subplots
# plt.subplots(2, 2, sharex='all', sharey='all')
#
# # Note that this is the same as
# plt.subplots(2, 2, sharex=True, sharey=True)
#
# # Create figure number 10 with a single subplot
# # and clears it if it already exists.
# fig, ax = plt.subplots(num=10, clear=True)

import sys
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import alphashape
import numpy as np
#
# points = [(0., 0.), (0., 1.), (1., 1.), (1., 0.),
#           (0.5, 0.25), (0.5, 0.75), (0.25, 0.5), (0.75, 0.5)]

# points = np.array([[0., 0.], [0., 1.], [1., 1.], [1., 0.],
#           [0.5, 0.25], [0.5, 0.75], [0.25, 0.5], [0.75, 0.5]])

# fig, ax = plt.subplots()
# ax.scatter(points[:,0], points[:,1])
# plt.show()

# alpha_shape = alphashape.alphashape(points, 0.)
#
# fig, ax = plt.subplots()
# ax.scatter(points[:,0], points[:,1])
# ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
# plt.show()
#
# alpha_shape = alphashape.alphashape(points, 2.0)
# fig, ax = plt.subplots()
# ax.scatter(points[:,0], points[:,1])
# ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
# plt.show()

from scipy.spatial import Delaunay
import numpy as np

arr = np.array([[0.0232, 0.3304], [2.456,34.5555]])
arr1 = arr*1000
arr2 = arr1.astype(int)
print(arr2)

#
# up_segment = np.arange(0,20*100,1)
# for i in up_segment:
#     if i == 0:
#         continue
#     x = i
#     y = coefs_up[2] * x * x + coefs_up[1] * x + coefs_up[0]
#     print('----------')
#     print(x, y)
#     k = y/x
#     #
#     # sym = symbols('res')
#     # # equation = Eq(coefs_down[3] * (sym**3) + coefs_down[2] * (sym**2) + coefs_down[1] * sym + coefs_down[0] - sym*(k), 0)
#     # sol = solve(coefs_down[3] * (sym**3) + coefs_down[2] * (sym**2) + coefs_down[1] * sym + coefs_down[0] - sym*(k), sym )
#
#     sol = np.roots([coefs_down[2], coefs_down[1], coefs_down[0] - k])
#
#     x_res1 = sol[0]
#     y_res1 = k * x_res1
#     dis_1 = x_res1 **2 + y_res1**2
#
#     x_res2 = sol[1]
#     y_res2 = k * x_res2
#     dis_2 = x_res2 **2 + y_res2**2
#
#     if dis_1 < dis_2:
#         x1 = x_res1
#         y1 = y_res1
#     else:
#         x1 = x_res2
#         y1 = y_res2
#
#     print(x1, y1)
#
# #     dis_cur = distance_point_to_point([x, y], [x1, y1])
# #
# #     target = fmld **2
# #     if dis_cur < target:
# #         target = dis_cur
# #
# # fmld = math.sqrt(target)
# # print('fmld: ', fmld)
#
