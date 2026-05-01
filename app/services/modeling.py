from __future__ import annotations

from collections import defaultdict
from datetime import date
import math
import numpy as np


def recency_weight(field_date: date, half_life_days: float = 14.0) -> float:
    days_old = (date.today() - field_date).days
    return math.exp(-max(days_old, 0) / half_life_days)


def compute_pollster_grade(rows: list[dict]) -> dict[str, dict]:
    by_pollster = defaultdict(list)
    for row in rows:
        by_pollster[row["pollster"]].append(row)

    grades = {}
    for pollster, items in by_pollster.items():
        errors = [abs(i["predicted_share"] - i["actual_share"]) for i in items]
        signed = [i["predicted_share"] - i["actual_share"] for i in items]
        mae = float(np.mean(errors)) if errors else 8.0
        bias = float(np.mean(signed)) if signed else 0.0
        reliability = min(1.0, len(items) / 25)
        composite = 1 / (mae + abs(bias) + 0.5)
        composite *= 0.5 + 0.5 * reliability
        grades[pollster] = {
            "mae": mae,
            "bias": bias,
            "reliability": reliability,
            "composite_weight": composite,
        }
    return grades


def weighted_projection(polls: list[dict], grade_by_pollster: dict[str, float]) -> dict:
    race_candidate_scores = defaultdict(lambda: {"num": 0.0, "den": 0.0, "party": None})

    for p in polls:
        grade = grade_by_pollster.get(p["pollster"], 0.08)
        w = recency_weight(p["field_date"]) * math.sqrt(max(p["sample_size"], 50)) * grade
        key = (p["race_id"], p["candidate"])
        race_candidate_scores[key]["num"] += w * p["vote_share"]
        race_candidate_scores[key]["den"] += w
        race_candidate_scores[key]["party"] = p["party"]

    projections = defaultdict(list)
    for (race_id, candidate), v in race_candidate_scores.items():
        projections[race_id].append(
            {
                "candidate": candidate,
                "party": v["party"],
                "projected_share": (v["num"] / v["den"]) if v["den"] else 0,
            }
        )

    return projections


def monte_carlo_win_probs(race_projection: dict, draws: int = 20_000) -> list[dict]:
    candidates = race_projection
    if not candidates:
        return []
    means = np.array([c["projected_share"] for c in candidates], dtype=float)
    sigma = np.full_like(means, 2.8)
    sims = np.random.normal(loc=means, scale=sigma, size=(draws, len(candidates)))
    winners = np.argmax(sims, axis=1)

    output = []
    for idx, c in enumerate(candidates):
        win_prob = float(np.mean(winners == idx))
        output.append({**c, "win_probability": round(win_prob * 100, 2)})
    return output
