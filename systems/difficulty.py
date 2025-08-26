# systems/difficulty.py
from dataclasses import dataclass, asdict
from typing import Dict
import json, math, time, pathlib

@dataclass
class DifficultyProfile:
    # parámetros que influyen en el gameplay
    init_speed: float = 8.0
    speed_increment: float = 0.05
    spawn_base_ms: int = 500         # base del spawner
    spawn_jitter_ms: int = 120
    cactus_stack_p: float = 0.35
    triple_stack_p: float = 0.15
    ptero_p: float = 0.40            # mezcla pteros vs cactus
    ptero_heights: tuple = ( -80, -55, -110 )  # offsets relativos al GROUND_Y

@dataclass
class SkillState:
    # estado persistente del jugador
    ema_ttf: float = 60.0            # EMA de "time-to-first-death" (s)
    rating: float = 0.0              # rating relativo (Z-score ~ habilidad)
    k_pid_p: float = 0.10
    k_pid_i: float = 0.02
    k_pid_d: float = 0.02
    i_accum: float = 0.0
    last_err: float = 0.0

TARGET_TTF = 75.0  # objetivo de duración (s) hasta el primer choque
EMA_ALPHA = 0.25   # cuánto pesa la última partida

class AdaptiveManager:
    def __init__(self, store_path="data/progress.json"):
        self.store_path = pathlib.Path(store_path)
        self.profile = DifficultyProfile()
        self.skill = SkillState()
        self._load()

    # ----- API pública -----
    def profile_for_new_run(self) -> DifficultyProfile:
        """Calcula un perfil de dificultad para la próxima partida."""
        # mapear rating → multiplicadores
        # rating >0 => más difícil; <0 => más fácil
        r = self.skill.rating
        speed_mul  = 1.0 + 0.12 * math.tanh(r/2)         # [-0.12, +0.12]
        spawn_mul  = 1.0 - 0.18 * math.tanh(r/2)         # inverso: más rating, menos intervalo
        ptero_bias = 0.40 + 0.20 * math.tanh(r/2)        # mezcla

        prof = DifficultyProfile(**asdict(self.profile))
        prof.init_speed      *= speed_mul
        prof.speed_increment *= speed_mul
        prof.spawn_base_ms    = int(prof.spawn_base_ms * spawn_mul)
        prof.ptero_p          = float(max(0.1, min(0.8, ptero_bias)))
        return prof

    def update_after_run(self, ttf_seconds: float, score: int):
        """Actualizar estimadores tras una partida."""
        # 1) EMA del TTF (time to first death)
        self.skill.ema_ttf = (1-EMA_ALPHA)*self.skill.ema_ttf + EMA_ALPHA*ttf_seconds

        # 2) Control tipo PID empujando el TTF hacia TARGET_TTF
        err = (self.skill.ema_ttf - TARGET_TTF) / TARGET_TTF  # >0 = muy fácil
        self.skill.i_accum = (self.skill.i_accum + err)
        d = err - self.skill.last_err
        self.skill.last_err = err
        pid_out = (self.skill.k_pid_p*err +
                   self.skill.k_pid_i*self.skill.i_accum +
                   self.skill.k_pid_d*d)
        # 3) Rating acumulado con amortiguación
        self.skill.rating += pid_out
        self.skill.rating = max(-3.0, min(3.0, self.skill.rating))
        self._save()

    def _load(self):
        if self.store_path.exists():
            try:
                with self.store_path.open("r") as f:
                    data = json.load(f)
                for k, v in data.items():
                    if hasattr(self.skill, k):
                        setattr(self.skill, k, v)
            except Exception:
                pass  # Si hay error, usa valores por defecto

    def _save(self):
        try:
            with self.store_path.open("w") as f:
                json.dump(asdict(self.skill), f)
        except Exception:
            pass
