# Sistema de Assets del Juego Chrome Dino

Esta carpeta contiene todos los gráficos del juego organizados por categorías.

## Estructura de Carpetas

```
assets/
├── Dino/           # Sprites del dinosaurio
│   ├── DinoRun1.png
│   ├── DinoRun2.png
│   ├── DinoJump.png
│   ├── DinoDuck1.png
│   └── DinoDuck2.png
├── Cactus/         # Sprites de cactus
│   ├── SmallCactus1.png
│   ├── SmallCactus2.png
│   ├── SmallCactus3.png
│   ├── LargeCactus1.png
│   ├── LargeCactus2.png
│   └── LargeCactus3.png
├── Bird/           # Sprites de pájaros
│   ├── Bird1.png
│   └── Bird2.png
└── Other/          # Otros elementos
    ├── Cloud.png
    └── Track.png
```

## Cómo Usar el Sistema de Assets

### 1. Colocar los archivos de imagen
Coloca los archivos PNG en las carpetas correspondientes según la estructura anterior.

### 2. El sistema se encarga automáticamente de:
- Cargar todas las imágenes al iniciar el juego
- Escalar los sprites al tamaño apropiado
- Proporcionar métodos fáciles de usar para obtener sprites

### 3. Uso en el código:
```python
from core.assets import asset_manager

# Obtener sprite del dinosaurio corriendo
dino_sprite = asset_manager.get_dino_running(frame)

# Obtener cactus aleatorio
cactus_sprite = asset_manager.get_small_cactus()

# Obtener nube
cloud_sprite = asset_manager.get_cloud()
```

## Características del Sistema

- **Carga automática**: Todos los assets se cargan al iniciar el juego
- **Escalado automático**: Los sprites se escalan al tamaño apropiado
- **Gestión centralizada**: Un solo lugar para manejar todos los gráficos
- **Fácil de usar**: Métodos simples para obtener sprites
- **Optimizado**: Los sprites se cargan una sola vez y se reutilizan

## Notas Importantes

- Los archivos deben estar en formato PNG
- Los nombres de archivo deben coincidir exactamente con los especificados
- El sistema maneja automáticamente los errores si faltan archivos
- Los sprites se escalan a 0.5x por defecto (ajustable en `scale_assets()`)
