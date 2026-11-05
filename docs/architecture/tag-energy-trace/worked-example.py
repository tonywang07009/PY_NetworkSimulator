"""Recompute the accepted charging examples; this is not the energy runtime."""
from decimal import Decimal, localcontext
import json
from pathlib import Path

with localcontext() as context:
    context.prec = 50
    D = Decimal
    rf_w = D('0.1') * D('0.00001')
    maximum_w = D('0.00001')
    slope_per_w = D('200000')
    midpoint_w = D('0.00001')
    omega = 1 / (1 + (slope_per_w * midpoint_w).exp())
    raw_w = maximum_w / (1 + (-slope_per_w * (rf_w - midpoint_w)).exp())
    dc_w = (raw_w - maximum_w * omega) / (1 - omega)
    dc_uw = dc_w * D('1000000')
    derivative_bound = maximum_w * slope_per_w / (4 * (1 - omega))
    assert abs(dc_uw - D('0.2571323571')) < D('0.0000000001')
    assert 0 < derivative_bound < 1
    examples = []
    for name, initial_uj, allowed, mode_uw in [
        ('normal_charge', D('0.8'), True, D('0.01')),
        ('capacity_saturation', D('0.95'), True, D('0.01')),
        ('passive_recovery', D('0'), True, D('0')),
        ('inter_window_gap', D('0.8'), False, D('0.01')),
    ]:
        harvested_uj = dc_uw * D('0.4') if allowed else D('0')
        consumed_uj = mode_uw * D('0.4')
        raw_uj = initial_uj + harvested_uj - consumed_uj
        spill_uj = max(D('0'), raw_uj - D('1'))
        final_uj = raw_uj - spill_uj
        assert D('0') <= final_uj <= D('1')
        balance_error = final_uj - initial_uj - harvested_uj + consumed_uj + spill_uj
        assert abs(balance_error) < D('1e-45')
        examples.append({
            'case': name, 'duration_ns': 400000000,
            'initial_energy_uj': str(initial_uj),
            'harvested_energy_uj': str(harvested_uj),
            'consumed_energy_uj': str(consumed_uj),
            'spilled_energy_uj': str(spill_uj),
            'final_energy_uj': str(final_uj),
        })
    assert examples[-1]['final_energy_uj'] == '0.796'
    depletion_s = D('0.002') / D('0.01')
    assert depletion_s == D('0.2')
    report = {
        'evidence_kind': 'scalar design arithmetic, not module or simulator test',
        'rf_input_w': str(rf_w), 'omega': str(omega),
        'raw_sigmoid_w': str(raw_w), 'dc_output_uw': str(dc_uw),
        'global_derivative_bound': str(derivative_bound),
        'examples': examples,
        'depletion_example': {
            'initial_energy_uj': '0.002', 'gap_duration_ns': 400000000,
            'normal_until_ns': 200000000, 'recovery_duration_ns': 200000000,
            'final_energy_uj': '0',
        },
    }
    destination = Path(__file__).with_name('worked-example.json')
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print('Scalar charging examples and energy balance checked:', destination)
