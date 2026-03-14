# desafio-do-cronometro
Desafio do Cronometro rodando em Raspberry Pi

# Ideia
Vi essa brincadeira em uma pizzaria, onde existia um desafio de quem conseguisse parar um cronometro em exatos 10 segundos (00:10:00) ganharia uma caneca de chopp.

Achei a brincadeira legal e decidi fazer a minha versão rodando em um Raspberry PI ligado em uma boteira e um monitor.

# Materiais (v1)

- Raspberry Pi 3B+
- Monitor (usei um externo mas pode ser qualquer tela que funcione no raspberry)
- Botão (usei um botão tic-tac daqueles de fiperama.)
  (https://lista.mercadolivre.com.br/botao-fliperama)
- Fio ou cabo jamper para ligar o botão na Gpio do raspberry.
  (https://lista.mercadolivre.com.br/cabo-jumper?sb=all_mercadolibre#D[A:cabo%20jumper])


# Passo a passo:

- Instalar dependencias;
- Configurar tela do Raspberry para não desligar/hibernar;
- Conectar o botão na porta GPIO do raspberry
- Copiar o script Python para o Raspberry;
- Configurar para executar o script no boot.


# Comandos / Funcionalidades:

- Pressionar o botão 1x, inicia ou para o cronometro;
- pressionar e segurar o botão pressionado por 3 segundos, zera o cronometro.
