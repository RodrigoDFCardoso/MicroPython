import time
from machine import Pin, I2C

# Configurar os números dos pinos SDA e SCL
sda_pin = Pin(10)  # Substitua pelo número do pino SDA desejado
scl_pin = Pin(11)  # Substitua pelo número do pino SCL desejado

# Inicializar o barramento I2C
i2c = I2C(1, sda=sda_pin, scl=scl_pin)  # Configure os pinos SDA e SCL corretamente

# Endereço I2C do SSD1306 (depende da configuração do display)
ssd1306_addr = 0x78  # Pode variar de acordo com o display

# Comandos de inicialização do SSD1306 (dependem do display)
init_commands = [
    0xAE,  # Desligar o display
    0xD5,  # Configurar clock dividido/ratio
    0x80,  # Valor para o clock dividido (0x80 é um valor comum)
    0xA8,  # Configurar multiplexação (altura do display - 1)
    0x3F,  # Valor para a altura do display (0x3F é um valor comum para 128x64)
    0xD3,  # Configurar deslocamento vertical
    0x00,  # Nenhum deslocamento vertical
    0x40,  # Definir a linha de partida (vertical)
    0x8D,  # Configurar carga da tabela de cores
    0x14,  # Valor para carga da tabela de cores (0x14 é um valor comum)
    0x20,  # Modo de endereçamento da página (horizontal)
    0x00,  # Não usar deslocamento (horizontal)
    0xA1,  # Segment re-map (A0/A1)
    0xC8,  # Comutação da direção dos segmentos
    0xDA,  # Configurar comum pads hardware
    0x12,  # Valor para comum pads hardware (0x12 é um valor comum)
    0x81,  # Configurar contraste
    0xCF,  # Valor para contraste (ajuste conforme necessário)
    0xD9,  # Configurar pré-carga de cor
    0xF1,  # Valor para pré-carga de cor (ajuste conforme necessário)
    0xDB,  # Configurar VCOMH deslocamento
    0x40,  # Valor para VCOMH deslocamento (ajuste conforme necessário)
    0xA4,  # Display seguirá o RAM (0xA4 para exibir dados, 0xA5 para exibir todos)
    0xA6,  # Normal (não-invertido) (0xA6 para normal, 0xA7 para invertido)
    0xAF   # Ligando o display
]

# Enviar os comandos de inicialização para o SSD1306
for command in init_commands:
    i2c.writeto(ssd1306_addr, bytes([0x00, command]))

# Limpar a tela
i2c.writeto(ssd1306_addr, bytes([0x40] + [0x00] * (128 * 64 // 8)))

# Função para desenhar um pixel no display
def set_pixel(x, y):
    if 0 <= x < 128 and 0 <= y < 64:
        page = y // 8
        bit = y % 8
        cmd = 0xB0 + page
        i2c.writeto(ssd1306_addr, bytes([0x00, cmd, (x & 0x0F) | 0x10, bit << 3]))

# Exemplo: Definir um pixel na posição (30, 30)
set_pixel(30, 30)

# Aguardar um pouco para ver o pixel
time.sleep(5)
