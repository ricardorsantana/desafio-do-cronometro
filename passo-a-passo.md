### DESAFIO DO CRONOMETRO ###

Considerando que você já tem o Raspberry Pi configurado com o sistema operacional Raspberry Pi OS (ou outra distro Linux de sua preferencia) com interface gráfica, siga os passos abaixo para configurar o Desafio do Cronometro.


---------------------------------------------
## Configurar tela do Raspberry para não desligar/hibernar;

- via terminal
- Entre no modo de configuração do Raspberry:

sudo raspi-config

- Vá até a opção "Display Options" 

(img_01)
![Display Options](/imagens/img_01.png)

- Selecione a opção "Screen Blanking"

(img_02)
![Screen Blanking](/imagens/img_02.png)

Um prompt aparecerá perguntando sobre sua escolha para habilitar ou 
desabilitar a hibernação da tela.
Como queremos desativar o mode de hibernação que por padrão vem habilitado, escolha a opção "Não/No".

(img_03)
![Enable Screen Blanking](/imagens/img_03.png)

---------------------------------------------
## Instalando Dependencias do sistema:

sudo apt update
sudo apt install python3-tk python3-rpi.gpio python3-pil python3-pil.imagetk unclutter sox
sudo apt install fonts-freefont-ttf
sudo pip3 install pillow
sudo apt install sox

---------------------------------------------
## Copie o script do desafio para dentro do Raspberry:

- Crie um diretório dentro da home chamado "desafio_10s"
(/home/pi/desafio_10s)

mkdir desafio_10s

- Dentro do diretório criado, crie o arquivo "desafio_10s.py"

nano desafio_10s.py

E copie o conteúdo do script Python para dentro deste arquivo:

---------------------------------------------
## Rode o scritp Python no boot do Raspberry:

->> 🚀 AUTO START NO BOOT
->>> Criar serviço:
sudo nano /etc/systemd/system/desafio10s.service

=============================== INICIO ===============================
[Unit]
Description=Desafio do Cronometro 10s
After=graphical.target
Wants=graphical.target

[Service]
Type=simple
User=pi
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart=/usr/bin/python3 /home/pi/desafio_10s/desafio_10s.py
Restart=always
RestartSec=2

[Install]
WantedBy=graphical.target
=============================== FIM ===============================


-->>> Ativar
sudo systemctl daemon-reload
sudo systemctl enable desafio10s
sudo systemctl start desafio10s


->>> 🔘 LIGAÇÃO DO BOTÃO
✅ Conexões corretas

Um terminal do botão → GPIO 17

Outro terminal do botão → GND (terra)

👉 Não precisa resistor externo, o código já ativa o pull-up interno do Raspberry Pi.