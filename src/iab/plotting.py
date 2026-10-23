"""從同一快照繪製等比例部署圖；不建立UE物理座標。"""
from .contracts import TagZone


def plot_topology(snapshot):
    """等比例平面部署圖；顏色只表示幾何分區，UE不畫物理位置。"""
    from matplotlib import pyplot as plt
    from matplotlib.patches import Circle

    fig, ax = plt.subplots(figsize=(11, 8),
                           layout='constrained')
    colors = {TagZone.NEAR: '#087f8c',
              TagZone.MID: '#c66a10',
              TagZone.FAR: '#7851a9'}

    config = snapshot.config
    donor = config.donor

    for node in config.iab_nodes:
        ax.plot([donor.position.x_m, node.position.x_m],
                [donor.position.y_m, node.position.y_m],
                color='#87929e', lw=0.9, zorder=0)



        for zone, radius in zip(TagZone, config.zone_outer_radii_m):
            ax.add_patch(Circle((node.position.x_m, node.position.y_m), radius,
                                fill=False, color=colors[zone], linewidth=1.0, alpha=0.75))
        # display node name
        ax.annotate(node.node_id,
                    (node.position.x_m,
                     node.position.y_m + config.zone_outer_radii_m[-1] + 3),
                    ha='center', va='bottom', fontsize=9, weight='bold')

    ax.scatter([n.position.x_m for n in config.iab_nodes],
               [n.position.y_m for n in config.iab_nodes],
               marker='s', s=65,
               color='#263544', label='IAB Node / Reader',
               zorder=4)
    ax.scatter([donor.position.x_m],
               [donor.position.y_m],
               marker='*',
               s=200,
               color='#263544',
               label='Donor',
               zorder=4)

    ax.annotate(donor.node_id,
                (donor.position.x_m, donor.position.y_m), #postion based
                xytext=(8, 0),
                textcoords='offset points',
                fontsize=10)

    for zone in TagZone:
        group = [t for t in snapshot.tags if t.zone == zone]
        if group: # if this area not tag just jump it
            ax.scatter([t.position.x_m for t in group],
                       [t.position.y_m for t in group],
                       color=colors[zone], s=28,
                       label=f'{zone.value} Tags ({len(group)})',
                       zorder=3)
        for tag in group:
            ax.annotate(tag.tag_id.removeprefix('Tag-'),
                        (tag.position.x_m, tag.position.y_m),
                        xytext=(3, 3),
                        textcoords='offset points',
                        fontsize=6.5)

    ax.set(xlabel='x (m)',
           ylabel='y (m)',
           title=f'Static IAB topology | seed={config.seed} | {len(snapshot.tags)} Tags')

    ax.set_aspect('equal', adjustable='box')
    ax.grid(alpha=0.18)
    ax.margins(0.12)
    ax.legend(loc='lower left', fontsize=8)

    # modle introduction
    ax.text(0.99, 0.01,
            'UEs: logical association only\nColors: distance zones, not SNR',
            transform=ax.transAxes,
            ha='right',
            va='bottom',
            fontsize=8)

    return fig, ax
