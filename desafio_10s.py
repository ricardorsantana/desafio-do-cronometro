#!/usr/bin/env python3
import tkinter as tk
import threading
import time
import os
import sys
import RPi.GPIO as GPIO

# =============================
# CONFIGURAÇÕES
# =============================
BOTAO = 24
ALVO = 10.00
LONG_PRESS = 3  # segundos
RANK_MAX = 5

BG = "#0b0f14"
TXT = "#e8e8e8"
VERDE = "#33ff99"
VERMELHO = "#ff3333"
AMARELO = "#ffcc00"

# =============================
# GPIO
# =============================
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BOTAO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# =============================
# VARIÁVEIS
# =============================
rodando = False
tempo_inicio = 0
tempo_atual = 0.0
ranking = []

botao_pressionado = False
tempo_pressionado = 0

idle_pisca = True

# =============================
# UTIL
# =============================
def tocar(arquivo):
    caminho = os.path.join(os.path.dirname(__file__), arquivo)
    if os.path.exists(caminho):
        os.system(f"aplay {caminho} >/dev/null 2>&1 &")

def formatar(t):
    m = int(t // 60)
    s = int(t % 60)
    c = int((t - int(t)) * 100)
    return f"{m:02d}:{s:02d}:{c:02d}"

# =============================
# CRONÔMETRO
# =============================
def atualizar():
    global tempo_atual
    if rodando:
        tempo_atual = time.time() - tempo_inicio
        lbl_tempo.config(text=formatar(tempo_atual))
        root.after(10, atualizar)

def iniciar():
    global rodando, tempo_inicio
    if not rodando:
        tocar("start.wav")
        tempo_inicio = time.time() - tempo_atual
        rodando = True
        atualizar()

def parar():
    global rodando
    if rodando:
        rodando = False
        tocar("stop.wav")
        avaliar()

def resetar():
    global rodando, tempo_atual
    rodando = False
    tempo_atual = 0
    lbl_tempo.config(text="00:00:00", fg=VERDE)
    lbl_info.config(text="PRESSIONE O BOTÃO PARA INICIAR")
    atualizar_ranking()
    tocar("idle.wav")

# =============================
# RESULTADO
# =============================
def avaliar():
    erro = abs(tempo_atual - ALVO)

    ranking.append(erro)
    ranking.sort()
    del ranking[RANK_MAX:]

    if erro == 0:
        lbl_info.config(text="VOCÊ GANHOU!!!", fg=VERDE)
        tocar("win.wav")
    else:
        lbl_info.config(
            text=f"ERRO! {tempo_atual:.2f}s  (±{erro:.2f}s)",
            fg=VERMELHO
        )
        tocar("error.wav")
        piscar_erro(0)

    atualizar_ranking()

def piscar_erro(cont):
    if cont >= 6:
        lbl_tempo.config(fg=VERDE)
        return

    cor = VERMELHO if cont % 2 == 0 else VERDE
    lbl_tempo.config(fg=cor)
    root.after(500, lambda: piscar_erro(cont + 1))

# =============================
# RANKING
# =============================
def atualizar_ranking():
    if not ranking:
        lbl_rank.config(text="TOP 5\n--")
        return

    texto = "TOP 5\n"
    for i, e in enumerate(ranking, 1):
        texto += f"{i}º ±{e:.2f}s\n"
    lbl_rank.config(text=texto.strip())

# =============================
# IDLE ANIMADO
# =============================
def animacao_idle():
    if not rodando and idle_pisca:
        cor = VERDE if lbl_tempo.cget("fg") == TXT else TXT
        lbl_tempo.config(fg=cor)
    root.after(800, animacao_idle)

# =============================
# BOTÃO (POLLING)
# =============================
def monitorar_botao():
    global botao_pressionado, tempo_pressionado

    estado_ant = GPIO.input(BOTAO)

    while True:
        estado = GPIO.input(BOTAO)

        # pressionou
        if estado_ant == 1 and estado == 0:
            botao_pressionado = True
            tempo_pressionado = time.time()

        # segurando
        if botao_pressionado and estado == 0:
            if time.time() - tempo_pressionado >= LONG_PRESS:
                botao_pressionado = False
                root.after(0, resetar)

        # soltou
        if estado_ant == 0 and estado == 1:
            if botao_pressionado:
                botao_pressionado = False
                root.after(0, clique_curto)

        estado_ant = estado
        time.sleep(0.01)

def clique_curto():
    if not rodando:
        iniciar()
    else:
        parar()

# =============================
# INTERFACE
# =============================
root = tk.Tk()
root.configure(bg=BG)
root.attributes("-fullscreen", True)
root.config(cursor="none")

W = root.winfo_screenwidth()
H = root.winfo_screenheight()

lbl_titulo = tk.Label(
    root,
    text="DESAFIO DO CRONÔMETRO",
    fg=TXT,
    bg=BG,
    font=("Arial", int(H * 0.06), "bold")
)
lbl_titulo.pack(pady=(H * 0.05, 10))

lbl_sub = tk.Label(
    root,
    text="Pare o relógio em exatos 10 segundos (00:10:00) para vencer!!!",
    fg=TXT,
    bg=BG,
    font=("Arial", int(H * 0.03))
)
lbl_sub.pack()

lbl_tempo = tk.Label(
    root,
    text="00:00:00",
    fg=VERDE,
    bg=BG,
    font=("Courier", int(H * 0.18), "bold")
)
lbl_tempo.pack(pady=H * 0.05)

lbl_info = tk.Label(
    root,
    text="Pare o relógio exatamente em 10.00s",
    fg=TXT,
    bg=BG,
    font=("Arial", int(H * 0.035))
)
lbl_info.pack(pady=10)

lbl_rank = tk.Label(
    root,
    text="TOP 5\n--",
    fg=AMARELO,
    bg=BG,
    font=("Courier", int(H * 0.03)),
    justify="center"
)
lbl_rank.pack(pady=H * 0.05)

# =============================
# START
# =============================
threading.Thread(target=monitorar_botao, daemon=True).start()
animacao_idle()
resetar()

def sair(event=None):
    GPIO.cleanup()
    root.destroy()
    sys.exit(0)

root.bind("<Escape>", sair)
root.protocol("WM_DELETE_WINDOW", sair)
root.mainloop()
