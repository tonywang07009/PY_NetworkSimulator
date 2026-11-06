"""Independent Decimal reference for the approved post-TBS CW example."""
from decimal import Decimal, localcontext
import json

with localcontext() as context:
    context.prec = 70
    D = Decimal
    rf_w = D('0.01') * D('0.0006797973850689421') / D(10) ** 2
    maximum_w, slope_per_w, midpoint_w = D('0.00001'), D(200000), D('0.00001')
    omega = 1 / (1 + (slope_per_w * midpoint_w).exp())
    sigmoid_w = maximum_w / (1 + (-slope_per_w * (rf_w-midpoint_w)).exp())
    dc_w = (sigmoid_w-maximum_w*omega) / (1-omega)
    harvested_j = dc_w * D('0.055')
    consumed_j = D('0.00000001') * D('0.055')
    after_j = D('0.0000008') - D('0.000000066012') + harvested_j - consumed_j
    assert abs(after_j-D('0.0000007343339972233599')) < D('1e-22')
    print(json.dumps({
        'evidence_kind': 'independent scalar arithmetic; no runtime imports or hardware claim',
        'rf_w': str(rf_w), 'dc_w': str(dc_w), 'tail_harvested_j': str(harvested_j),
        'tail_consumed_j': str(consumed_j), 'final_after_guard_j': str(after_j),
        'tail_ns': [66000000,121000000], 'guard_ns': [121000000,121200000],
    }, indent=2))
