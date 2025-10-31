import numpy as np
import matplotlib.pyplot as plt
import mpl_scatter_density
from matplotlib.gridspec import GridSpec
from astropy.visualization import ImageNormalize, LogStretch


n = 300_000
x = np.random.normal(0.0, 100.0, n)
y = np.random.normal(0.0, 50.0, n)


fig = plt.figure(figsize=(7.5, 7.5))
gs = GridSpec(
    2, 2, figure=fig,
    width_ratios=[1.0, 0.20],
    height_ratios=[0.25, 1.0],
    wspace=0.06, hspace=0.06
)


ax_joint = fig.add_subplot(gs[1, 0], projection='scatter_density')
ax_margx = fig.add_subplot(gs[0, 0], sharex=ax_joint)
ax_margy = fig.add_subplot(gs[1, 1], sharey=ax_joint)


norm = ImageNormalize(vmin=0., vmax=None, stretch=LogStretch())
im = ax_joint.scatter_density(x, y, cmap='viridis', norm=norm)

ax_joint.set_xlabel('X')
ax_joint.set_ylabel('Y')


bins = 80
ax_margx.hist(x, bins=bins, density=False, alpha=0.6, edgecolor='none')
ax_margy.hist(y, bins=bins, density=False, orientation='horizontal',
              alpha=0.7, edgecolor='none')
ax_margx.tick_params(labelbottom=False)
ax_margy.tick_params(labelleft=False)
ax_margx.set_ylabel('PDF of X')
ax_margy.set_xlabel('PDF of Y')
ax_margx.set_xlim(ax_joint.get_xlim())
ax_margy.set_ylim(ax_joint.get_ylim())


fig.canvas.draw()  
renderer = fig.canvas.get_renderer()


bbox_texts = [label.get_window_extent(renderer) for label in ax_joint.get_yticklabels()]
bbox_label = ax_joint.yaxis.label.get_window_extent(renderer)


min_x = min([b.x0 for b in bbox_texts + [bbox_label]])


fig_width_px = fig.bbox.width

left_edge = min_x / fig_width_px


bbox = ax_joint.get_position()

cbar_width = 0.02

gap = 0.015
cbar_left = left_edge - cbar_width - gap
cbar_bottom = bbox.y0
cbar_height = bbox.height

ax_cbar = fig.add_axes([cbar_left, cbar_bottom, cbar_width, cbar_height])

cbar = fig.colorbar(im, cax=ax_cbar)
cbar.set_label('Point density')
cbar.ax.yaxis.set_ticks_position('left')
cbar.ax.yaxis.set_label_position('left')


for ax in [ax_joint, ax_margx, ax_margy]:
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.0)


plt.subplots_adjust(left=0.2)   
plt.show()