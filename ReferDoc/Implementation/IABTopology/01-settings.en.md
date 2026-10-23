# Settings

[Back to the user guide](README.en.md)

## Which settings can I change?

| Setting | Default | Meaning |
|---|---|---|
| Donor and Node positions | Specified in the example | x and y coordinates on a flat map, in metres |
| Outer radius of each zone | `(10, 30, 50)` m | Draws near, middle and far zones around each Node |
| Tag count in each zone | `(10, 13, 7)` | 10 near, 13 middle and 7 far Tags across the entire scene: 30 in total |
| Minimum Tags per Node | `2` | Each Node receives at least two Tags; the remainder are assigned randomly |
| Random seed `seed` | `42` | A number controlling the random result; the same settings and number reproduce the layout within the same program and environment |

Zone distances are measured from each Tag's assigned Node:

| Zone | Distance |
|---|---|
| Near | More than 0 m and no more than 10 m |
| Middle | More than 10 m and no more than 30 m |
| Far | More than 30 m and no more than 50 m |

For example, a Tag at 10 m belongs to the near zone, while a Tag at 20 m belongs to the middle zone. Counts apply to the entire scene; each Node does not receive its own set of 10/13/7 Tags.

In the settings code, use parentheses `(...)` for radii, counts and the Node list, rather than square brackets `[...]`. A zone can have zero Tags, as in `(10, 0, 0)`, provided the total is sufficient to meet every Node's minimum.
