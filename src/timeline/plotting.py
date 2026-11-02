"""Plot UE occupancy and remaining Tag time from resource snapshots."""
import matplotlib.pyplot as plt

def plot_resources(windows):
    figure, axis = plt.subplots(figsize=(11, 4))
    node_ids = tuple(dict.fromkeys(node_resource.node_id for window in windows for node_resource in window.nodes))
    for window in windows:
        for node_resource in window.nodes:
            node_index = node_ids.index(node_resource.node_id)
            window_start_ms = node_resource.start_ns / 1_000_000
            ue_end_ms = node_resource.ue_end_ns / 1_000_000
            window_end_ms = node_resource.end_ns / 1_000_000
            # writen bar chart
            axis.barh(node_index, ue_end_ms-window_start_ms, left=window_start_ms, color='#82b1ff', edgecolor='black')
            axis.barh(node_index, window_end_ms-ue_end_ms, left=ue_end_ms, color='#a5d6a7', edgecolor='black')
            axis.text((window_start_ms+ue_end_ms)/2, node_index, node_resource.direction.value, ha='center', va='center')

        # set the vetical line in begin and enf for starts
        axis.axvline(window.start_ns/1_000_000, color='gray', linestyle='--')
        axis.axvline(window.end_ns/1_000_000, color='gray', linestyle='--')
    axis.set_yticks(range(len(node_ids)), node_ids)
    axis.set_xlabel('Global time (ms): blue = UE, green = Tag resource, blank = unavailable')
    axis.set_title('Resource availability, not completed payload')
    figure.tight_layout()
    return figure

