# Reading the results

[Back to the user guide](README.en.md)

## How do I read the results?

### Tables

| Table | What it shows |
|---|---|
| Settings: `settings` | Positions, radii, Tag counts and random seed used for this run |
| Nodes: `nodes` | Each Node's position, UE and near/middle/far Tag counts |
| Tags: `tags` | Each Tag's ID, position, assigned Node, distance and zone |
| Connections: `links` | Donor-to-Node connections and each Node's associated UEs and Tags |

The default example should contain five Nodes, five UEs and 30 Tags, with near/middle/far counts of 10/13/7. Every Node has at least two Tags, but Node totals do not have to be equal.

### Deployment plot

| Mark | Meaning |
|---|---|
| Star | Donor position |
| Square | Node position |
| Teal, orange-brown and purple circles and Tag dots | Near, middle and far zones, respectively |
| Number beside a dot | Tag ID; for example, `001` means `Tag-001` |
| Line between the Donor and a Node | Their connection |

Both axes use metres at the same scale. UEs have an assigned Node but no physical position in the current model, so they are not plotted.

### Saved files

| File | Purpose |
|---|---|
| `deployment.png`, `deployment.svg` | Deployment images for viewing or inclusion in a report |
| `settings.csv`, `nodes.csv`, `tags.csv`, `links.csv` | Four tables that can be opened in a spreadsheet tool |
| `snapshot.json` | A data file containing the full settings and generated layout |
