# Hunting-Rabbit-PortScanner

Hunting-Rabbit-PortScanner（猎兔端口扫描器）：一款快速，准确的主机存活检测和端口扫描工具。

GO版本：https://github.com/langsasec/Hunting-Rabbit-PortScanner-Go

## Usage

```
Hunting-Rabbit-PortScanner  author:浪飒

positional arguments:
  network               Network to scan (e.g. "192.168.0.1" or "192.168.0.0/24")

options:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Ports to scan (e.g. "80" or "1-65535", default: 
  -t TIMEOUT, --timeout TIMEOUT
                        TCP connection timeout in seconds (default: 0.5)
  -w WORKERS, --workers WORKERS
                        Maximum number of worker threads for the scan (default: 64)
  -v, --verbose         Verbose output
```

## e.g.

扫描单个主机：

```cmd
python Hunting-Rabbit-PortScanner.py 192.168.0.1 -v
```

扫描网段的所有80端口

```
python Hunting-Rabbit-PortScanner.py 192.168.0.0/24 -v -p 80
```

## help

1.如果想提高准确率，可提高超时时间，eg:-t=1。

2.主机存活非ping检测，禁ping也会检测到存活。

3.不检测手机，不在渗透测试范围。
