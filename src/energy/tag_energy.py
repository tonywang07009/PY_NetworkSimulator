"""Pure RF/DC conversion, complete-operation admission and inactive accounting."""
import math
from decimal import Decimal, localcontext

from .contracts import (TagMode, TagSnapshot, TagTraceRow, TagTrace,
                        D2R_OCCUPANCY_NS, GUARD_NS, INACTIVE_MODES, RESOURCE_PHASES)


def default_energy_settings():
    """Return the accepted synthetic profile as an independent dictionary."""
    return {
        'capacity_j': 1e-6,
        'initial_energy_j': 1e-6,
        'quiescent_power_w': 10e-9,
        'receive_power_w': 1e-6,
        'd2r_power_w': 1e-6,
        'activation_energy_j': 1e-9,
        'maximum_dc_w': 10e-6,
        'slope_per_w': 2e5,
        'midpoint_w': 10e-6,
    }


def harvested_power_w(rf_input_w, *, maximum_w, slope_per_w, midpoint_w):
    values = {
        'rf_input_w': rf_input_w,
        'maximum_w': maximum_w,
        'slope_per_w': slope_per_w,
        'midpoint_w': midpoint_w,
    }
    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f'{name} must be a finite number')

        try:
            finite = math.isfinite(value) # return bool
        except OverflowError:
            finite = False

        if not finite:
            raise ValueError(f'{name} must be a finite number')

    if rf_input_w < 0:
        raise ValueError('rf_input_w must be non-negative')

    if maximum_w <= 0 or slope_per_w <= 0 or midpoint_w <= 0:
        raise ValueError('Sigmoid parameters must be positive')

    rf_input_w = float(rf_input_w)
    maximum_w = float(maximum_w)
    slope_per_w = float(slope_per_w)
    midpoint_w = float(midpoint_w)

    shape = slope_per_w * midpoint_w
    if not math.isfinite(shape):
        raise ValueError('Sigmoid shape must be finite')

    # The tag charge caclus
    inverse_shape_exp = math.exp(-shape)
    omega = inverse_shape_exp / (1 + inverse_shape_exp)

    if omega == 0:
        raise ValueError('Sigmoid shape is outside the supported numerical range')

    # The fix 0 error formula
    slope_bound = maximum_w * slope_per_w / (4 * (1 - omega))
    if not math.isfinite(slope_bound) or slope_bound > 1:
        raise ValueError('Sigmoid parameters must satisfy the passive slope bound')

    scaled_input = slope_per_w * rf_input_w
    exponential = math.exp(-scaled_input)
    normalized_fraction = omega * (-math.expm1(-scaled_input)) / (omega + (1 - omega) * exponential)

    return maximum_w * normalized_fraction



def _energy_decimal(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{name} must be a finite non-negative number')

    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False

    if not finite or value < 0:
        raise ValueError(f'{name} must be a finite non-negative number')

    return Decimal(str(value))


def _nonnegative_ns(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(f'{name} must be a non-negative integer ns value')

    return value


def _trace_settings(settings):
    if not isinstance(settings, dict):
        raise ValueError('settings must be the explicit energy settings dictionary')

    values = {}
    for name in ('capacity_j', 'quiescent_power_w', 'receive_power_w', 'd2r_power_w', 'activation_energy_j'):
        if name not in settings:
            raise ValueError(f'missing energy setting: {name}')
        values[name] = _energy_decimal(settings[name], name)

    if any(values[name] <= 0 for name in ('capacity_j', 'quiescent_power_w', 'receive_power_w', 'd2r_power_w')):
        raise ValueError('capacity and mode powers must be positive')

    return values


def _validate_snapshot(snapshot, values):
    if not isinstance(snapshot, TagSnapshot):
        raise ValueError('snapshot must be a TagSnapshot')

    if not isinstance(snapshot.tag_id, str) or not snapshot.tag_id.strip():
        raise ValueError('tag_id must be a non-empty string')

    _nonnegative_ns(snapshot.now_ns, 'now_ns')
    energy = _energy_decimal(snapshot.energy_j, 'energy_j')
    if energy > values['capacity_j']:
        raise ValueError('stored energy exceeds capacity')

    if not isinstance(snapshot.mode, TagMode):
        raise ValueError('mode must be TagMode')

    return energy


def trace_tag_operation(snapshot, *, tbs_bytes, paging_ns, wait_ns,
                        window_end_ns, deadline_ns, receive_success=True, cw_available=True, settings=None,
                        cw_off_ns=None, cw_power_dbm=None, distance_m=None):
    """Admit a whole operation from stored energy, then produce an immutable trace.

    With CW context, the caller guarantees explicit batch membership and supplies
    its final D2R completion as cw_off_ns. The operation cannot infer other Tags.
    No-batch callers retain immediate Guard and zero post-TBS harvesting.
    """
    selected_settings = default_energy_settings() if settings is None else settings
    values = _trace_settings(selected_settings)
    energy = _validate_snapshot(snapshot, values)
    if snapshot.mode not in INACTIVE_MODES:
        raise ValueError('a new operation requires an inactive Tag')

    if type(tbs_bytes) is not int or tbs_bytes not in D2R_OCCUPANCY_NS:
        raise ValueError('tbs_bytes must be one of 8, 16, 32, 64')

    _nonnegative_ns(paging_ns, 'paging_ns')
    _nonnegative_ns(wait_ns, 'wait_ns')
    _nonnegative_ns(window_end_ns, 'window_end_ns')
    _nonnegative_ns(deadline_ns, 'deadline_ns')

    if paging_ns == 0:
        raise ValueError('paging_ns must be positive')

    if type(receive_success) is not bool:
        raise ValueError('receive_success must be bool')

    if type(cw_available) is not bool or not cw_available:
        raise ValueError('CW must be available for the admitted D2R interval')

    d2r_ns = D2R_OCCUPANCY_NS[tbs_bytes] # The d2r refelction duration time
    d2r_end_ns = snapshot.now_ns + paging_ns + wait_ns + d2r_ns
    if cw_off_ns is None:
        if cw_power_dbm is not None or distance_m is not None:
            raise ValueError('CW source requires an explicit batch CW_OFF')
        guard_start_ns = d2r_end_ns
        cw_rf_w = 0.0
    else:
        _nonnegative_ns(cw_off_ns, 'cw_off_ns')
        if cw_off_ns < d2r_end_ns:
            raise ValueError('batch CW_OFF precedes complete D2R')
        guard_start_ns = cw_off_ns
        cw_rf_w = cw_rf_input_w(cw_power_dbm=cw_power_dbm, distance_m=distance_m)

    guard_end_ns = guard_start_ns + GUARD_NS

    if guard_end_ns > window_end_ns:
        raise ValueError('complete operation and Guard exceed the Window')

    if d2r_end_ns >= deadline_ns:
        raise ValueError('D2R completion must precede the exclusive deadline')

    with localcontext() as context:
        context.prec = 50
        segments = ( # The tag status transformer
            (TagMode.WAKING, 'ACTIVATION', 0, Decimal(0), values['activation_energy_j']),
            (TagMode.PAGING_RX, 'PAGING', paging_ns, values['receive_power_w'], Decimal(0)),
            (TagMode.WAIT_D2R, 'WAIT_D2R', wait_ns, values['quiescent_power_w'], Decimal(0)),
            (TagMode.BACKSCATTER, 'D2R', d2r_ns, values['d2r_power_w'], Decimal(0)),
            (TagMode.SLEEP, 'GUARD', GUARD_NS, values['quiescent_power_w'], Decimal(0)),
        )
        required_energy = Decimal(0)
        # This is caluer tag need consum how many elect for this round.
        for _, _, duration_ns, power_w, fixed_j in segments:
            required_energy += fixed_j + power_w * Decimal(duration_ns) / Decimal(1_000_000_000)

        # The energy check
        if energy < required_energy:
            raise ValueError('stored energy does not cover the complete operation')

        rows = []
        cursor_ns = snapshot.now_ns

        for mode, phase, duration_ns, power_w, fixed_j in segments:
            if phase == 'GUARD' and cw_off_ns is not None:
                mode = TagMode.ENERGY_RECOVERY if energy == 0 else TagMode.SLEEP
                completed = TagSnapshot(snapshot.tag_id, cursor_ns, _trace_float(energy), mode)
                if cursor_ns < cw_off_ns:
                    tail = advance_tag_interval(completed, duration_ns=cw_off_ns - cursor_ns,
                                                phase='POST_TBS_CW', rf_input_w=cw_rf_w,
                                                settings=selected_settings)
                    rows.extend(tail.rows)
                    completed = tail.snapshot
                guard = advance_tag_interval(completed, duration_ns=GUARD_NS, phase='GUARD',
                                             settings=selected_settings)
                rows.extend(guard.rows)
                cursor_ns = guard.snapshot.now_ns
                energy = Decimal(str(guard.snapshot.energy_j))
                continue

            before = energy
            consumed = fixed_j + power_w * Decimal(duration_ns) / Decimal(1_000_000_000)
            energy -= consumed
            note = ''
            if mode is TagMode.BACKSCATTER:
                note = 'receive success' if receive_success else 'receive failure; no energy refund'
            rows.append(TagTraceRow(cursor_ns, cursor_ns + duration_ns, mode, phase,
                                    _trace_float(before), 0.0, _trace_float(consumed), 0.0, _trace_float(energy), note))
            cursor_ns += duration_ns

        final_mode = (guard.snapshot.mode if cw_off_ns is not None else
                      TagMode.ENERGY_RECOVERY if energy == 0 else TagMode.SLEEP)
        updated = TagSnapshot(snapshot.tag_id, cursor_ns, _trace_float(energy), final_mode)
    return TagTrace(updated, tuple(rows), receive_success=receive_success)


def _trace_float(value):
    result = float(value)
    if not math.isfinite(result) or (value != 0 and result == 0):
        raise ValueError('trace energy is outside the supported floating-point range')

    return result

# handle inactive model the tag energy change.
def advance_tag_interval(snapshot, *, duration_ns, phase, rf_input_w=0.0, settings=None):
    """Account one inactive interval without changing the supplied snapshot.

    POST_TBS_CW requires caller-established completed membership in the current
    batch, ending no later than its CW_OFF. Ordinary D2R never grants credit.
    Active reception/backscatter must use complete-operation admission instead.
    """
    selected_settings = default_energy_settings() if settings is None else settings
    values = _trace_settings(selected_settings)
    energy = _validate_snapshot(snapshot, values)

    if snapshot.mode not in INACTIVE_MODES:
        raise ValueError('background accounting requires an inactive Tag')

    _nonnegative_ns(duration_ns, 'duration_ns')
    if phase not in RESOURCE_PHASES:
        raise ValueError('unknown resource phase')

    for name in ('maximum_dc_w', 'slope_per_w', 'midpoint_w'):
        if name not in selected_settings:
            raise ValueError(f'missing conversion setting: {name}')

    dc = harvested_power_w(rf_input_w, maximum_w=selected_settings['maximum_dc_w'],
                           slope_per_w=selected_settings['slope_per_w'],
                           midpoint_w=selected_settings['midpoint_w'])
    allowed = phase in ('UE_UL', 'UE_DL', 'POST_TBS_CW')

    with localcontext() as context:
        context.prec = 50
        duration_s = Decimal(duration_ns) / Decimal(1_000_000_000)
        harvest_w = Decimal(str(dc)) if allowed else Decimal(0)
        harvested = harvest_w * duration_s
        recovering = snapshot.mode is TagMode.ENERGY_RECOVERY or energy == 0
        mode_power = Decimal(0) if recovering else values['quiescent_power_w'] # quiescent -> stan by
        raw = energy + (harvest_w - mode_power) * duration_s
        depletion_s = None

        # The attribute time charge tag
        if not recovering and raw <= 0:
            depletion_s = energy / (mode_power - harvest_w)
            consumed = mode_power * depletion_s
            after = Decimal(0) if raw == 0 else harvest_w * (duration_s - depletion_s)
            recovering = True
        else:
            consumed = mode_power * duration_s
            after = raw

        spilled = max(Decimal(0), after - values['capacity_j'])
        after -= spilled
        final_mode = TagMode.ENERGY_RECOVERY if recovering else snapshot.mode
        end_ns = snapshot.now_ns + duration_ns
        row = TagTraceRow(snapshot.now_ns, end_ns, snapshot.mode, phase,
                          _trace_float(energy), _trace_float(harvested), _trace_float(consumed),
                          _trace_float(spilled), _trace_float(after),
                          'depletion split: offset is diagnostic seconds' if depletion_s is not None else '')
        updated = TagSnapshot(snapshot.tag_id, end_ns, _trace_float(after), final_mode)
    return TagTrace(updated, (row,), float(depletion_s) if depletion_s is not None else None)


def cw_rf_input_w(*, cw_power_dbm, distance_m):
    """One-way serving-DU CW input; no reflection coefficient or channel fading."""
    if isinstance(cw_power_dbm, bool) or not isinstance(cw_power_dbm, (int, float)):
        raise ValueError('cw_power_dbm must be an accepted CW power')

    if cw_power_dbm not in (-2, 10, 22):
        raise ValueError('cw_power_dbm must be -2, 10 or 22 dBm')

    distance = _energy_decimal(distance_m, 'distance_m')
    if not Decimal(1) <= distance <= Decimal(50):
        raise ValueError('distance_m must be within 1-50 m')

    return 10 ** ((cw_power_dbm - 30) / 10) * 0.0006797973850689421 / float(distance) ** 2


def validate_energy_inputs(*, snapshots, rf_inputs_w, settings=None):
    """Check initialization inputs without changing caller-owned dictionaries."""
    selected_settings = default_energy_settings() if settings is None else settings
    values = _trace_settings(selected_settings)
    if not isinstance(snapshots, dict) or not isinstance(rf_inputs_w, dict):
        raise ValueError('snapshots and rf_inputs_w must be dictionaries')

    for snapshot in snapshots.values():
        _validate_snapshot(snapshot, values)
    for rf_input_w in rf_inputs_w.values():
        _energy_decimal(rf_input_w, 'rf_input_w')
    return {'snapshots':dict(snapshots), 'rf_inputs_w':dict(rf_inputs_w)}


def project_tag_operation(plan, *, now_ns, cw_rf_input_w=0.0, settings=None):
    """Read a plan made by trace_tag_operation at one current time; never debit it."""
    _nonnegative_ns(now_ns, 'now_ns')
    _energy_decimal(cw_rf_input_w, 'cw_rf_input_w')
    if not isinstance(plan, TagTrace) or not plan.rows:
        raise ValueError('plan must be a nonempty TagTrace')

    if not plan.rows[0].start_ns <= now_ns <= plan.snapshot.now_ns:
        raise ValueError('now_ns is outside the plan interval')

    if now_ns == plan.snapshot.now_ns:
        return plan.snapshot
    for row in plan.rows:
        if row.start_ns <= now_ns < row.end_ns:
            break
    else:
        raise ValueError('now_ns is outside the plan interval')

    if row.phase in ('POST_TBS_CW', 'GUARD'):
        beginning = TagSnapshot(plan.snapshot.tag_id, row.start_ns, row.before_j, row.mode)
        rf_input_w = cw_rf_input_w if row.phase == 'POST_TBS_CW' else 0.0
        result = advance_tag_interval(beginning, duration_ns=now_ns-row.start_ns,
                                      phase=row.phase, rf_input_w=rf_input_w, settings=settings)
        return result.snapshot
    elapsed = Decimal(now_ns-row.start_ns) / Decimal(row.end_ns-row.start_ns)
    stored = Decimal(str(row.before_j)) - Decimal(str(row.consumed_j))*elapsed
    return TagSnapshot(plan.snapshot.tag_id, now_ns, _trace_float(stored), row.mode)
