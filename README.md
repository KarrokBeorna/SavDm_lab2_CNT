# Lab2 - DHCP Server + NTP Client

RFC NTP - https://datatracker.ietf.org/doc/html/rfc5905  
RFC DHCP - https://datatracker.ietf.org/doc/html/rfc2132

## DHCP Server

### Поля:
- `op` - тип сообщения (1 байт)
- `htype` - тип аппаратного адреса (1 байт)
- `hlen` - длина аппаратного адреса в байтах (1 байт)
- `hops` - кол-во промежуточных маршрутизаторов (1 байт)
- `xid` - уникальный идентификатор транзакции (4 байта)
- `secs` - время в секундах с начала процесса получения адреса (2 байта)
- `flags` - поле для флагов (2 байта)
- `ciaddr` - IP-адрес клиента, если он есть (4 байта)
- `yiaddr` - новый IP-адрес клиента в OFFER (4 байта)
- `siaddr` - IP-адрес сервера (4 байта)
- `giaddr` - IP-адрес агента ретранслятора (4 байта)
- `chaddr` - аппаратный адрес клиента (обычно MAC) (16 байт)
- `sname` - необязательное имя сервера (64 байта)
- `file` - необязательное имя файла на сервере (192 байта)
- `options` - различные дополнительные параметры конфигурации. В начале поля всегда указывается "волшебное число" (99,130,83,99)

  - порт сервера - 67
  - порт клиента - 68

### 4 этапа:
- DHCPDISCOVER (C -> S)
- DHCPOFFER (S -> C)
- DHCPREQUEST (C -> S)
- DHCPACK (S -> C)

Вообще, DHCP нужен для получения IP-адреса, однако в моем же случае сервер просто получает NTP Packet и выводит его содержимое в консоль, 
отвечая при этом DHCPOFFER (по широковещательному адресу и порту 68).

## NTP Client

  - порт - 123

Клиент заполняет 3 поля - `version`, `mode` (3, так как клиент) и `transmit` (время отправления пакета).  
Затем сервер должен скопировать значение из `transmit` в `originate`, записать время получения в `receive`, а также время отправления ответа в `transmit`.

Сам протокол нужен для синхронизации времени. В моём же случае отправляет NTP Packet серверу (по широковещательному адресу и порту 67)
и ждет ответ, получая при этом DHCPOFFER, который выводит в консоль.

## Вывод в консоль

![image](https://user-images.githubusercontent.com/43076360/146403477-e383718f-fe2b-4187-9df5-f62d50a3a0fe.png)

- `Options 1` - DHCPACK
- `Options 2` - 255.255.255.0 маска подсети
- `Options 3` - 192.168.1.1 маршрутизатор
- `Options 4` - срок аренды IP-адреса (86400 сек - 1 день)
- `Options 5` - DHCP сервер