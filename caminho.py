#!.venv/bin/python3

from controle import *
from sys      import argv
from math     import atan2

from main import GRADE_INICIAL as grade

from itertools import pairwise

def espera_jogadas(mov, jogadas: list[movimento]):
    for j in jogadas:
        #print(j)
        aplica_mov(mov, j)
        transmissor.enviar()
        espera_mov(mov)

def colorir_nó(n: int) -> str:
    if   n == 0: return '⬛'
    elif n == 2: return '🔳'
    elif n == 3: return '☑️'
    else:        return '⬜'

def print_caminho(grade, cam):
    g = np.zeros_like(grade)

    x, y = cam[0]
    g[y, x] = 2
    for p in cam[1:-1]:
        x, y    = p
        g[y, x] = 1
    x, y = cam[-1]
    g[y, x] = 3

    for lin in g:
        linha = map(colorir_nó, lin)
        print(''.join(tuple(linha)))

def gerar_difs(caminho):
    difs = []
    for ant, p in pairwise(caminho):
        x,  y  = ant
        nx, ny = p
        dx, dy = nx-x, ny-y

        ds = dx, dy
        difs.append(ds)
    return difs

def dif_inicial(ori):
    if   ori ==-pi/2: ori_dif = ( 0, 1)
    elif ori == pi/2: ori_dif = ( 0,-1)
    elif ori == 0.00: ori_dif = ( 1, 0)
    elif ori == 1*pi: ori_dif = (-1, 0)
    else: assert False

    return ori_dif

def gerar_giros(difs):
    giros = []
    giros.append(0) #! trocar p/ prependar (0,0) nos difs (+lidar)
    for ant, dif in pairwise(difs):
        giro = computar_giro(ant, dif)
        giros.append(giro)
        if giro != 0:
            giros.append(0)
    return giros

def normalizar_angulo(ang: float) -> float:
    # a partir de https://stackoverflow.com/a/2321125
    return atan2(sin(ang), cos(ang)) #! deve ser devagar

def computar_giro(_ant: tuple, _dif: tuple) -> float: #! typ
    ant = complex(*_ant)
    dif = complex(*_dif)
    ang = phase(dif) - phase(ant)
    return normalizar_angulo(ang)

def gerar_jogadas(ori:     float, a: posi,
                  ori_fin: float, b: posi, *,
                  vel: int) -> list[movimento]:
    from astar import astar as planejar

    caminho = planejar(grade, a, b)
    dif_ini = dif_inicial(ori)
    difs    = gerar_difs(caminho) #[dif_ini] + gerar_difs(caminho)
    giro_ini= computar_giro(dif_ini, difs[0])
    giros   = [giro_ini] + gerar_giros(difs)
    #! ang_final = ori + sum(giros)

    jogs = []
    for ang in giros:
        if ang == 0: jogs.append(avançar_bloco(None, vel))
        else:        jogs.append(girar(None, vel, ang=ang))

    print_caminho(grade, caminho)
    print(dif_ini, difs)
    print(list(map("{:.0f}".format, map(lambda x: x*180/pi, giros))))
    print(jogs)

    return jogs

gerar_jogadas(0, (1,1), None, (4,6), vel=50)
gerar_jogadas(0, (4,6), None, (1,1), vel=50)
exit(0)

    

vel = 50
l: list[movimento] = [
    avançar_bloco(None, vel),
    avançar_bloco(None, vel),
    avançar_bloco(None, vel),
    girar(None, vel, ang=pi/2),
    avançar_bloco(None, vel),
    girar(None, vel, ang=2*pi),
]

mov = movedor(0); mov.send(None)
if transmissor.inicializar():
    espera_jogadas(mov,l)
    transmissor.finalizar()
else:
    print("deu ruim: transmissor")

