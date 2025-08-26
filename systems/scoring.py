# systems/scoring.py
import csv, time, pathlib, json
from dataclasses import asdict

class HiScore:
    def load(self, path="data/hiscore.dat"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def save(self, score, path="data/hiscore.dat"):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(str(int(score)))
        except Exception:
            pass

class Telemetry:
    def __init__(self, path="data/runs.csv"):
        self.path = pathlib.Path(path)
        if not self.path.exists():
            self.path.write_text("ts,ttf,score,rating,init_speed,spawn_base_ms,seed\n")
    def append_run(self, ttf, score, profile, seed):
        # rating debe venir del AdaptiveManager
        rating = getattr(profile, 'rating', 0.0)
        line = f"{int(time.time())},{ttf:.3f},{score},{rating},{profile.__dict__['init_speed']},{profile.__dict__['spawn_base_ms']},{seed}\n"
        with self.path.open("a") as f: f.write(line)
