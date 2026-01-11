[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zP0O23M7)

## Installation et utilisation
Il est recommandé de créer un environnement virtuel avant d’installer les dépendances :

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Dependance
```bash
pip install -r requirements.txt
```

Or install dependencies manually:
```bash
pip install [package-name]
```

### Ligne de commande
```bash
python3 main.py [arguments]
```

## Prérequis

- Python 3.8+
- See `requirements.txt` for full dependency list

## Fichiers d'exemples
Les fichiers d'exemple sont situer dans `examples/` Vous pouvez lancer le script avec ces fichiers
- Example 1 : `examples/HorseHead.fits` (noir et blanc FITS image pour tester )
- Example 2 : `examples/test_M31_linear.fits` (Couleur FITS image pour tester )
- Example 3 : `examples/test_M31_raw.fits` (Couleur FITS image pour tester )


## Lancer l'appli

soyez sure d'installler :
```bash
python3 -m pip install PyQt6

sudo apt install -y \
libxcb-cursor0 \
libxcb-xinerama0 \
libxkbcommon-x11-0 \
libxcb-icccm4 \
libxcb-image0 \
libxcb-keysyms1 \
libxcb-render-util0 \
libxcb-shape0 \
libxcb-randr0 \
libxcb-xkb1ut0 \

pip install astropy
pip install opencv-python
pip install numpy
pip install requests
```