# Troubleshooting

[Back to the user guide](README.en.md)

## Common problems and solutions

If settings break a rule, the program shows `ValueError` and a reason. Read that message first, then use the table below.

| Problem | Cause and action |
|---|---|
| Too few Tags | Five Nodes with a minimum of two each require at least 10 Tags; raising the minimum also raises the required total |
| Node circles overlap or touch | With the default 50 m outer radius, every pair of Node centres must be more than 100 m apart; adjust their positions |
| Invalid radii | Use three positive radii in increasing order, such as `(10, 30, 50)` |
| Settings use square brackets | Use parentheses instead; for example, change `[10, 13, 7]` to `(10, 13, 7)` |
| Repeated Node or Donor ID | Use distinct names and avoid IDs reserved for generated UEs and Tags |
| Teaching checks stop after changing Tag counts | The supplied checks expect 30 Tags with counts of 10/13/7; update their expected counts too, or run the sections individually up to the table display to inspect your new layout |
| Images or data cannot be saved | Check that the output folder is writable; a failed export may leave some files, so rerun export after fixing the issue |

To try a different random layout, change `seed` and run again. The specified Donor and Node positions stay fixed; Tag assignments and positions are generated again.
