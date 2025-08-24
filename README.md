# Descrição do funcionamento básico do programa

TO DO: quando todos finalizarem suas funções

# Capturas de tela (screenshots) das respostas obtidas pelo endpoint /status

TO DO: quando todos finalizarem suas funções

# Explicação de como cada informação exibida é obtida a partir de /proc e /sys

## datetime

[How can I get system time from a proc file?](https://stackoverflow.com/questions/5242296/how-can-i-get-system-time-from-a-proc-file)
[Real Time Clock (RTC) Drivers for Linux](https://docs.kernel.org/admin-guide/rtc.html)

O datetime pode ser encontrado através do comando:

```bash
cat /proc/driver/rtc
```

Esse arquivo contém informações do RTC (Real-Time Clock) do hardware, e coletamos as informações de "rtc_time" e "rtc_date".

## uptime_seconds

[The /proc Filesystem](https://docs.kernel.org/filesystems/proc.html)

O uptime (tempo que o sistema está ativo) pode ser encontrado através do comando:

```bash
cat /proc/uptime
```

Ele é o primeiro valor a ser exibido, enquanto o segundo é o tempo que o sistema ficou ocioso.

## cpu

TO DO

## memory

TO DO

## os_version

[The /proc Filesystem](https://docs.kernel.org/filesystems/proc.html)

A versão do sistema operacional pode ser encontrada através do comando:

```bash
cat /proc/version
```

Ou também:

```bash
cat /proc/version_signature
```

Dado o exemplo de retorno, usamos o primeiro arquivo ```/proc/version``` para montar a versão.
Ele detalha versão do kernel e detalhes de compilação do sistema.

## processes

TO DO

## disks

TO DO

## usb_devices

TO DO

## network_adapters

TO DO



