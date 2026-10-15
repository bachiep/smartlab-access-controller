from slac_fuzz.override_packet import (
    MAGIC_PACKET,
    MAX_ATTEMPTS,
    Decision,
    black_box_search,
    concolic_solve_magic,
    evaluate_patched_packet,
    evaluate_vulnerable_packet,
    run_experiment,
)


def test_vulnerable_parser_grants_the_magic_packet():
    assert evaluate_vulnerable_packet(MAGIC_PACKET) is Decision.OVERRIDE_GRANTED


def test_vulnerable_parser_denies_non_magic_packet():
    assert evaluate_vulnerable_packet(b"NOPE") is Decision.DENIED


def test_parser_rejects_wrong_length_and_near_magic_packets():
    for packet in (b"", b"SLA", b"SLAC!", b"SLAX", b"TLAC"):
        assert evaluate_vulnerable_packet(packet) is Decision.DENIED


def test_patched_parser_denies_the_former_bypass_packet():
    assert evaluate_patched_packet(MAGIC_PACKET) is Decision.DENIED


def test_concolic_solver_produces_the_same_target_input():
    packet = concolic_solve_magic()
    assert packet == MAGIC_PACKET
    assert evaluate_vulnerable_packet(packet) is Decision.OVERRIDE_GRANTED


def test_black_box_records_a_bounded_attempt_count():
    result = black_box_search(evaluate_vulnerable_packet, seed=11, max_attempts=25)
    assert result.seed == 11
    assert 1 <= result.attempts <= 25
    assert result.duration_seconds >= 0


def test_experiment_compares_five_seeded_runs_for_each_method():
    report = run_experiment(max_attempts=10)

    assert [run.seed for run in report.black_box_runs] == [11, 23, 37, 53, 71]
    assert [run.seed for run in report.concolic_runs] == [11, 23, 37, 53, 71]
    assert len(report.black_box_runs) == 5
    assert len(report.concolic_runs) == 5
    assert all(run.packet == MAGIC_PACKET for run in report.concolic_runs)
    assert all(run.reached_target for run in report.concolic_runs)
    assert report.patched_decision is Decision.DENIED


def test_default_experiment_exhausts_the_declared_black_box_budget():
    report = run_experiment()

    assert MAX_ATTEMPTS == 100_000
    assert all(run.attempts == MAX_ATTEMPTS for run in report.black_box_runs)
    assert report.summary()["max_attempts_per_run"] == MAX_ATTEMPTS
