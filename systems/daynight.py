class DayNightCycle:
    def __init__(self):
        self.is_night = False
        self.cycle_points = 1000
        self.transition_duration = 200  # Puntos para la transición
        self.day_color = (245, 245, 245)  # Gris claro para el día
        self.night_color = (40, 40, 60)   # Azul-gris oscuro para la noche
        self.current_color = self.day_color

    def update(self, score):
        # Calcula la posición del ciclo (0 a 2*cycle_points)
        # Comienza con la fase de día (0 a cycle_points-1)
        cycle_pos = score % (2 * self.cycle_points)
        
        # Determina si estamos en fase de día o noche
        self.is_night = cycle_pos >= self.cycle_points
        
        # Calcula el progreso de la transición (0.0 a 1.0)
        if cycle_pos < self.cycle_points - self.transition_duration:
            # Día completo
            self.current_color = self.day_color
        elif cycle_pos < self.cycle_points:
            # Transición de día a noche
            progress = (cycle_pos - (self.cycle_points - self.transition_duration)) / self.transition_duration
            self.current_color = self._interpolate_color(self.day_color, self.night_color, progress)
        elif cycle_pos < 2 * self.cycle_points - self.transition_duration:
            # Noche completa
            self.current_color = self.night_color
        else:
            # Transición de noche a día
            progress = (cycle_pos - (2 * self.cycle_points - self.transition_duration)) / self.transition_duration
            self.current_color = self._interpolate_color(self.night_color, self.day_color, progress)

    def _interpolate_color(self, color1, color2, progress):
        """Interpola entre dos colores RGB basándose en el progreso (0.0 a 1.0)"""
        r = int(color1[0] + (color2[0] - color1[0]) * progress)
        g = int(color1[1] + (color2[1] - color1[1]) * progress)
        b = int(color1[2] + (color2[2] - color1[2]) * progress)
        return (r, g, b)

    def get_bg_color(self):
        return self.current_color
