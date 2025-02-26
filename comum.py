from typing import Final
from typing_extensions import TypeIs

from threading import Event

import numpy as np
from   numpy.typing import NDArray


## constantes
largura_campo: Final[int] = 1700 #mm
altura_campo:  Final[int] = 1300 #mm
largura_gol:   Final[int] = 100  #mm
altura_gol:    Final[int] = 400  #mm

VEL_MAX: Final[int] = 100 #%
N_ROBÔS: Final[int] = 3

DIST_BLOCO:   Final[int]   = 100 #mm
TAM_BLOCO:    Final[int]   = DIST_BLOCO
FATOR_MATRIZ: Final[float] = 1/DIST_BLOCO


## funções utilitárias
type Num = int | float
type Vec = tuple[Num, Num]

def clamp(val: Num, MIN: Num, MAX: Num) -> Num:
    return min(MAX, max(MIN, val))

def dist(a: Vec, b: Vec) -> float:
    x0, y0 = a; x1, y1 = b
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

def none(obj: object | None) -> TypeIs[None]:
    return obj is None
def some(obj: object | None) -> bool:
    return not none(obj) #! ainda inclui None, não entendi ainda pq

def complex_to_tuple(pos: complex) -> tuple:
    return float(pos.real), float(pos.imag)

def complex_to_xy(cp: complex):
    return np.array([cp.real, cp.imag], np.int32)

def xy_to_complex(points: NDArray): #! tipos
    if len(points) <= 0: return np.array([])
    return points @ np.array([[1], [1j]])[:, 0]


## classes utilitárias
class Evento(Event):
    __call__ = Event.is_set

