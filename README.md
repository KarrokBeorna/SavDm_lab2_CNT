# Lab2 - DHCP Server + NTP Client

RFC NTP - https://datatracker.ietf.org/doc/html/rfc5905
RFC DHCP - https://datatracker.ietf.org/doc/html/rfc2132

## DHCP Server

- порт сервера - 67
- порт клиента - 68

4 этапа:
- DHCPDISCOVER (C -> S)
- DHCPOFFER (S -> C)
- DHCPREQUEST (C -> S)
- DHCPACK (S -> C)

Вообще, DHCP нужен для получения IP-адреса, однако в моем же случае сервер просто получает NTP Packet и выводит его содержимое в консоль, 
отвечая при этом DHCPOFFER (по широковещательному адресу и порту 68).

## NTP Client

- порт - 123

Клиент заполняет 3 поля - version, mode (3, так как клиент) и transmit (время отправления пакета).

Сам протокол нужен для синхронизации времени. В моём же случае отправляет NTP Packet серверу (по широковещательному адресу и порту 67)
и ждет ответ, получая при этом DHCPOFFER, который выводит в консоль.

## Вывод в консоль

