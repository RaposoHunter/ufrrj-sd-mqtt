import json
from random import random
# import smbus 
import time # Usado na manipulação dos ciclos de repetição
import requests as request # Usado para fazer requisições HTTP
# import RPi.GPIO as GPIO # Usado para controlar os pinos I/O do RPi
from ctypes import c_short, c_byte, c_ubyte
from datetime import datetime # Usado para adquirir a hora atual do sistema
from queue import Full, Queue
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SERVER_URL = getenv('SERVER_URL', 'http://localhost:8000')
DEVICE = 0x76 # Endereço padrão para dispositivos I2C

# bus = smbus.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
#                      # Rev 1 Pi uses bus 0

# def getShort(data, index):
#   # return two bytes from data as a signed 16-bit value
#   return c_short((data[index+1] << 8) + data[index]).value

# def getUShort(data, index):
#   # return two bytes from data as an unsigned 16-bit value
#   return (data[index+1] << 8) + data[index]

# def getChar(data,index):
#   # return one byte from data as a signed char
#   result = data[index]
#   if result > 127:
#     result -= 256
#   return result

# def getUChar(data,index):
#   # return one byte from data as an unsigned char
#   result =  data[index] & 0xFF
#   return result

# def readBME280ID(addr=DEVICE):
#   # Chip ID Register Address
#   REG_ID     = 0xD0
#   (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
#   return (chip_id, chip_version)

# def readBME280All(addr=DEVICE):
#   # Register Addresses
#   REG_DATA = 0xF7
#   REG_CONTROL = 0xF4
#   REG_CONFIG  = 0xF5

#   REG_CONTROL_HUM = 0xF2
#   REG_HUM_MSB = 0xFD
#   REG_HUM_LSB = 0xFE

#   # Oversample setting - page 27
#   OVERSAMPLE_TEMP = 2
#   OVERSAMPLE_PRES = 2
#   MODE = 1 # Modo forçado de leitura

#   # Oversample setting for humidity register - page 26
#   OVERSAMPLE_HUM = 2
#   bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

#   control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
#   bus.write_byte_data(addr, REG_CONTROL, control)

#   # Read blocks of calibration data from EEPROM
#   # See Page 22 data sheet
#   cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
#   cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
#   cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

#   # Convert byte data to word values
#   dig_T1 = getUShort(cal1, 0)
#   dig_T2 = getShort(cal1, 2)
#   dig_T3 = getShort(cal1, 4)

#   dig_P1 = getUShort(cal1, 6)
#   dig_P2 = getShort(cal1, 8)
#   dig_P3 = getShort(cal1, 10)
#   dig_P4 = getShort(cal1, 12)
#   dig_P5 = getShort(cal1, 14)
#   dig_P6 = getShort(cal1, 16)
#   dig_P7 = getShort(cal1, 18)
#   dig_P8 = getShort(cal1, 20)
#   dig_P9 = getShort(cal1, 22)

#   dig_H1 = getUChar(cal2, 0)
#   dig_H2 = getShort(cal3, 0)
#   dig_H3 = getUChar(cal3, 2)

#   dig_H4 = getChar(cal3, 3)
#   dig_H4 = (dig_H4 << 24) >> 20
#   dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)

#   dig_H5 = getChar(cal3, 5)
#   dig_H5 = (dig_H5 << 24) >> 20
#   dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)

#   dig_H6 = getChar(cal3, 6)

#   # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
#   wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
#   time.sleep(wait_time/1000)  # Wait the required time  

#   # Read temperature/pressure/humidity
#   data = bus.read_i2c_block_data(addr, REG_DATA, 8)
#   pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
#   temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
#   hum_raw = (data[6] << 8) | data[7]

#   # Refine temperature
#   var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
#   var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
#   t_fine = var1+var2
#   temperature = float(((t_fine * 5) + 128) >> 8)

#   # Refine pressure and adjust for temperature
#   var1 = t_fine / 2.0 - 64000.0
#   var2 = var1 * var1 * dig_P6 / 32768.0
#   var2 = var2 + var1 * dig_P5 * 2.0
#   var2 = var2 / 4.0 + dig_P4 * 65536.0
#   var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
#   var1 = (1.0 + var1 / 32768.0) * dig_P1
#   if var1 == 0:
#     pressure=0
#   else:
#     pressure = 1048576.0 - pres_raw
#     pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
#     var1 = dig_P9 * pressure * pressure / 2147483648.0
#     var2 = pressure * dig_P8 / 32768.0
#     pressure = pressure + (var1 + var2 + dig_P7) / 16.0

#   # Refine humidity
#   humidity = t_fine - 76800.0
#   humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
#   humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
#   if humidity > 100:
#     humidity = 100
#   elif humidity < 0:
#     humidity = 0

#   return temperature/100.0,pressure/100.0,humidity

# Realiza a formatação das mensagens de erro
def formatError(err):
    err['mensagem'] = " | ".join(err['mensagem']) # Junta todas as mensagens em uma string única separada por " | "
    err['lido_em'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Recupera a data e hora em que a leitura foi realizada

    return json.dumps(err)

# Realiza uma requisição ao banco de dados para capturar os limites das medições estalecidos pelo supervisor
def loadDataLimits():
    # response = request.get(
    #     f'{SERVER_URL}/mysql/limites'
    # ).json()

    # limits = {
    #     "temperatura" : response['temperatura'],
    #     "umidade" : response['umidade'],
    #     "co2" : response['co2']
    # }

    limits = {
        "temperatura" : {
            "min": 17,
            "max": 31
        },
        "umidade" : {
            "min": 58,
            "max": 83
        },
        "co2" : {
            "min": 10,
            "max": 27
        }
    }
    
    
    return limits

# Registra a ocorrência de um erro na fila a ser publicada no broker MQTT
def publishError(errors_queue: Queue, err):
    try:
        errors_queue.put(formatError(err))
    except Full:
        # TODO - Guardar o erro em um arquivo e enviar todos os erros deste arquivo para o banco de dados assim que uma requisição bem-sucedida ocorrer
        pass

# Realiza uma requisição que registra o resultado da média das leituras
def postReadingAvarage(bmeData):
    response = request.post(
        f'{SERVER_URL}/mysql',
        json=bmeData
    )
    
    return response

# def main(readings_queue: Queue, errors_queue: Queue):
def main(errors_queue: Queue):
	# Dados de identificação do sensor
    # (chip_id, chip_version) = readBME280ID()
    
    # print("ID do Chip:", chip_id)
    # print("Versão....:", chip_version)
    # print()
    
    # NOTE - A numeração dos pinos precisa ser avaliada na hora
    ARES_CONDICIONADOS = 17 # Pino ligado aos ares-condicionados
    IRRIGADORES = 27 # Pino ligado aos irrigadores
    EXAUSTORES = 22 # Pino ligado aos exaustores
    
    cycle_interval = 60 # X segundos entre cada leitura
    max_readings_num = 10 # Y leituras antes do envio dos dados
    readings = [] # Guarda até Y leituras e é resetado a cada X*Y/6 minutos
    
    # GPIO.setmode(GPIO.BCM) # Indica para o módulo que será usada a numeração no padrão BCM
    
    # Configurando os pinos dos equipamentos como saída de dados
    # GPIO.setup(ARES_CONDICIONADOS, GPIO.OUT)
    # GPIO.setup(IRRIGADORES, GPIO.OUT)
    # GPIO.setup(EXAUSTORES, GPIO.OUT)
    
    while True:
        readingError = False # Variável para checar por erros a cada leitura
        limits = loadDataLimits() # Seta os limites aceitos na leitura
        
		# Realiza uma leitura dos dados pelo sensor
        # temperatura,pressao,umidade = readBME280All()
        temperatura,umidade = [random() * 100, random() * 100]

        #pressaoPA = pressao * 100
        #pressaoATM = pressaoPA / 101325
        
		# Dicionário para guardar a leitura realizada
        reading = {
            "temperatura": temperatura,
            "umidade": umidade,
            #"co2": co2,
        }
        
		# Dicionário para guardar qual medida está ligada à qual pino
        equipments = {
            "temperatura": ARES_CONDICIONADOS,
            "umidade": IRRIGADORES,
            "co2": EXAUSTORES
        }
        
		# Dicionário para guardar um possível erro
        err = {
            "mensagem": [],
            "lido_em": None
        } 
        
        # TODO - NOTIFICAR O CLIENTE DE ERROS
        for key in reading:
            # Caso um dado da leitura esteja fora dos limites adiciona essa informação ao erro
            
            if(reading[key] > limits[key]['max']):
                readingError = True # Um erro ocorreu
                
				# Os relês funcionam em low-state. 0 = Ligado e 1 = Desligado
                # if(key == "umidade"):
                #     GPIO.output(equipments[key], GPIO.HIGH) # 1
                # else:
                #     GPIO.output(equipments[key], GPIO.LOW) # 0
                    
                err['mensagem'].append(f"O parametro '{key}' esta acima do limite definido ({limits[key]['max']})!")
                
            elif(reading[key] < limits[key]['min']):
                readingError = True
                
                # if(key == "umidade"):
                #     GPIO.output(equipments[key], GPIO.LOW)
                # else:
                #     GPIO.output(equipments[key], GPIO.HIGH)
                    
                err['mensagem'].append(f"O parametro '{key}' esta abaixo do limite definido ({limits[key]['min']})!")
            
		# Caso exista um erro
        if(readingError):
            publishError(errors_queue, err)
            
		# Contabilizando a leitura
        readings.append(reading) 
        
        # TODO - Enviar leiturar para uma fila a ser processada por outra Thread
        if(len(readings) == max_readings_num):
            temperaturaMedia = 0
            umidadeMedia = 0
            # co2Media = 0
            
            for leitura in readings:
                temperaturaMedia += leitura['temperatura']
                umidadeMedia     += leitura['umidade']
                # co2Media         += leitura['co2']
                
            temperaturaMedia /= max_readings_num
            umidadeMedia     /= max_readings_num
            # co2Media         /= max_readings_num
            
            # TODO - ENVIAR UMA MENSAGEM DE ERRO NA MÉDIA CASO EXISTA
            
			# Dicionário para guardar os dados da leitura
            bmeData = {
                "temperatura": temperaturaMedia,
                "umidade": umidadeMedia,
                # "co2": co2Media,
                "lido_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
			# TODO - USAR FUNÇÕES ASSÍNCRONAS PARA EVITAR GARGALOS
			# Enviando a média  para o banco de dados
            postReadingAvarage(bmeData)
            
			# Limpando o array para o próximo ciclo de leituras
            readings = []
        
        time.sleep(cycle_interval) # Espera X segundos até a próxima leitura
