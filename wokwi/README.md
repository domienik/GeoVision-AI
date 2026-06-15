# GeoSensor Fire Alert - Simulação ESP32 no Wokwi

Este módulo simula um sistema IoT de alerta de risco de queimada usando ESP32, sensor DHT22 e LED vermelho.

## Componentes utilizados

- ESP32
- Sensor DHT22
- LED vermelho
- Resistor

## Funcionamento

O ESP32 realiza a leitura da temperatura e da umidade do ar usando o sensor DHT22.

A lógica de alerta considera risco de queimada quando:

- Temperatura maior que 35°C
- Ou umidade do ar menor que 35%

Quando uma dessas condições ocorre, o LED vermelho é acionado.

## Integração com a solução principal

Este módulo complementa o dashboard GeoVision AI. Enquanto o modelo de Inteligência Artificial classifica imagens orbitais, o ESP32 simula sensores terrestres que poderiam ser usados para monitorar áreas de risco ambiental.

Em uma aplicação real, os dados do ESP32 poderiam ser enviados para o dashboard por API, MQTT ou serviços em nuvem como AWS IoT Core.

## Link da simulação

https://wokwi.com/projects/466922667659076609