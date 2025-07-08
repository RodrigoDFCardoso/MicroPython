
## 🧩 Hardware Utilizado

### 🛠️ Placa de Desenvolvimento
- **BitdogLab 7E**

### 🌡️ Sensores Utilizados
- **INA226** – Sensor de tensão e corrente via I2C  
- **BME280** – Sensor ambiental (temperatura, pressão e umidade) via I2C  
- **NEO-6M** – Módulo GPS via UART

### 🔌 Arranjo de Ligações

| Sensor    | Interface | GPIOs Usadas | Endereço |
|-----------|-----------|--------------|----------|
| INA226    | I2C       | GP02 (SDA), GP03 (SCL) | `0x40` |
| BME280    | I2C       | GP02 (SDA), GP03 (SCL) | Automático |
| NEO-6M    | UART      | GP08 (TX), GP09 (RX)   | —        |

---

## 📚 Bibliotecas Utilizadas

```python
from machine import Pin, SoftI2C, UART
from micropyGPS import MicropyGPS
import bme280_float as bme280
import ssd1306
import time
