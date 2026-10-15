"""Small, deliberately bounded target for the Topic 4 fuzzing experiment.

The vulnerable parser treats one four-byte maintenance packet as an access
override.  The patched parser rejects that packet.  Both implementations are
fixtures for the experiment only; neither communicates with a physical lock.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from random import Random
from statistics import median
from time import perf_counter
from typing import Callable

from z3 import BitVec, Solver, sat


MAGIC_PACKET = b"SLAC"
SEEDS = (11, 23, 37, 53, 71)
MAX_ATTEMPTS = 100_000


class Decision(str, Enum):
    DENIED = "denied"
    OVERRIDE_GRANTED = "override_granted"


@dataclass(frozen=True)
class SearchResult:
    method: str
    seed: int | None
    attempts: int
    duration_seconds: float
    reached_target: bool
    packet: bytes | None


@dataclass(frozen=True)
class ExperimentReport:
    black_box_runs: tuple[SearchResult, ...]
    concolic_runs: tuple[SearchResult, ...]
    patched_decision: Decision
    max_attempts: int

    def summary(self) -> dict[str, object]:
        def summarize(runs: tuple[SearchResult, ...]) -> dict[str, object]:
            attempts = [run.attempts for run in runs]
            durations = [run.duration_seconds for run in runs]
            return {
                "runs": [serialize_result(run) for run in runs],
                "mean_attempts": sum(attempts) / len(attempts),
                "median_attempts": median(attempts),
                "mean_duration_seconds": sum(durations) / len(durations),
                "median_duration_seconds": median(durations),
            }

        return {
            "target": "parse_override_packet",
            "magic_packet_hex": MAGIC_PACKET.hex(),
            "input_size_bytes": len(MAGIC_PACKET),
            "seeds": list(SEEDS),
            "max_attempts_per_run": self.max_attempts,
            "black_box": summarize(self.black_box_runs),
            "concolic": summarize(self.concolic_runs),
            "patched_magic_packet_decision": self.patched_decision.value,
        }


def evaluate_vulnerable_packet(packet: bytes) -> Decision:
    """Return the decision of the intentionally vulnerable parser."""
    if len(packet) != 4:
        return Decision.DENIED
    if packet[0:2] != b"SL":
        return Decision.DENIED
    if packet[2:4] != b"AC":
        return Decision.DENIED
    return Decision.OVERRIDE_GRANTED


def evaluate_patched_packet(packet: bytes) -> Decision:
    """Return the decision after removing the undocumented override path."""
    del packet
    return Decision.DENIED


def black_box_search(
    target: Callable[[bytes], Decision], *, seed: int, max_attempts: int
) -> SearchResult:
    """Randomly sample the same four-byte input domain without branch feedback."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")

    random = Random(seed)
    started = perf_counter()
    for attempt in range(1, max_attempts + 1):
        candidate = random.randbytes(4)
        if target(candidate) is Decision.OVERRIDE_GRANTED:
            return SearchResult(
                method="black_box",
                seed=seed,
                attempts=attempt,
                duration_seconds=perf_counter() - started,
                reached_target=True,
                packet=candidate,
            )
    return SearchResult(
        method="black_box",
        seed=seed,
        attempts=max_attempts,
        duration_seconds=perf_counter() - started,
        reached_target=False,
        packet=None,
    )


def concolic_solve_magic() -> bytes:
    """Solve the path constraints of the override branch with Z3."""
    bytes_ = [BitVec(f"byte_{index}", 8) for index in range(4)]
    solver = Solver()
    for symbol, value in zip(bytes_, MAGIC_PACKET, strict=True):
        solver.add(symbol == value)
    if solver.check() != sat:
        raise RuntimeError("override branch unexpectedly became unsatisfiable")
    model = solver.model()
    return bytes(model.evaluate(symbol).as_long() for symbol in bytes_)


def concolic_search(target: Callable[[bytes], Decision], *, seed: int) -> SearchResult:
    """Solve and validate the target branch; seed indexes a repeated trial."""
    started = perf_counter()
    candidate = concolic_solve_magic()
    reached = target(candidate) is Decision.OVERRIDE_GRANTED
    return SearchResult(
        method="concolic",
        seed=seed,
        attempts=1,
        duration_seconds=perf_counter() - started,
        reached_target=reached,
        packet=candidate if reached else None,
    )


def run_experiment(max_attempts: int = MAX_ATTEMPTS) -> ExperimentReport:
    """Run five indexed trials per method on the same vulnerable target."""
    black_box_runs = tuple(
        black_box_search(evaluate_vulnerable_packet, seed=seed, max_attempts=max_attempts)
        for seed in SEEDS
    )
    return ExperimentReport(
        black_box_runs=black_box_runs,
        concolic_runs=tuple(
            concolic_search(evaluate_vulnerable_packet, seed=seed) for seed in SEEDS
        ),
        patched_decision=evaluate_patched_packet(MAGIC_PACKET),
        max_attempts=max_attempts,
    )


def serialize_result(result: SearchResult) -> dict[str, object]:
    return {
        "method": result.method,
        "seed": result.seed,
        "attempts": result.attempts,
        "duration_seconds": result.duration_seconds,
        "reached_target": result.reached_target,
        "packet_hex": result.packet.hex() if result.packet is not None else None,
    }
