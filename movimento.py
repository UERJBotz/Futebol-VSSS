#!.venv/bin/python3

from main import *
from cmath import phase

def main(arg_time='y', desenhar=True):
  vel = VEL_MAX//2

  frame = frames.get()
  visto, tela = visão(frame, vs_conf, CONVERSÃO, desenhar)
  time = visto.teams.get('team_yellow', {})

  mov = controle.movedor(0); mov.send(None)
  try:
    alvo = complex(100, 100)
    pos_ant = complex(0,0)
    parado = 0
    while not fim():
      if not frames.empty(): frame = frames.get()[100:, 200:544]

      visto, tela = visão(frame, vs_conf, CONVERSÃO, desenhar)
      amarelos = visto.teams['team_yellow']
      time = amarelos if len(amarelos) else time
      robô = list(time.values())[0]

      pos = robô.pos
      if abs(pos - pos_ant) < 10: parado += 1
      pos_ant = pos
      
      desloc = pos - alvo
      dist   = abs(desloc)
      dang   = phase(desloc) - robô.orientation

      #if   dist < 10: controle.parar(mov)
      if False: pass
      elif controle.terminou_mov(mov):
        #if parado > 10: controle.avançar_dist(mov, -vel, dist=100)
        if False: pass
        elif dang < .2: controle.avançar_dist(mov, vel, dist=dist)
        else:           controle.girar(mov, vel, ang=dang)
      transmissor.enviar()

      pos, desloc = complex_to_tuple(pos), complex_to_tuple(desloc)
      print(f"{pos=}, {desloc=}, {dist=:.2f}, {dang=:.2f}")

      cv.imshow("preview", tela["vision"])
      cv.waitKey(1) # necessário!!!
  finally:
    fim.set()

    cam.release()
    cv.destroyAllWindows()
    transmissor.finalizar()

## Ponto de entrada do programa
if __name__ == "__main__":
    if not (cam.isOpened()):
        print("Não foi possível abrir a câmera"); exit(1)
    if not (transmissor.inicializar()):
        print("Não foi possível abrir a serial"); exit(1)

    Thread(target=teclado.ler_para_sempre, daemon=True).start()
    Thread(target=camera, args=[fim], daemon=True).start()
    main(arg_time='y', desenhar=True)

