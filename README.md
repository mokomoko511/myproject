# Log acquistion systems for python.

Those tools are get logs by python for specific network device.

## Description
These tools are made specific network device's on the assumption of using on Windows.
- logging_telnet.py
Getting device log to execute in command list.

 - fileget_telnet.py
Getting tech support or configuration program.

 - httpserver.py and tftpserver.py
HTTP server and TFTP server. Start with one click.
(TFTP server does not support binary...)

Some console terminal application have implement for macro or logging system.
There tools is only auxiliary. Appeared the console window to showing human begin.
Therefore, Many of those tools are slow in operation.
I want to fast and easy getting the network device's logs.

## Requirement
 - Python3.6 or latest
 - To install requests pyinstaller, tftpy, paramiko.
 .. code-block:: python
    $ pip install pyinstaller tftpy paramiko.

  pyinstaller need Windows ".exe" binary created.

## Usage
 - "logging_telenet.py" need to execute command list. You must be specified it.

.. code-block:: python
usage: logging_telnet.exe [-h] [-f LOGFOLDER] [-l LOGFILENAME]
                          ipaddress username password cmdlist
logging_telnet.exe: error: the following arguments are required: ipaddress, username, password, cmdlist


 - "fileget_telnet.py" can select getting the configuration file(-c) or tech support file(-t). Default is tech support.

.. code-block:: python
usage: fileget_telnet.exe [-h] [-t] [-c] [-f LOGFOLDER] [-l LOGFILENAME]
                         ipaddress username password tftpserverip
fileget_telnet.exe: error: too few arguments

 - "httpserver.py" and "tftpserver.py"
Start ONE click only.



## Licence

[GPL](https://github.com/mokomoko511/myproject/LICENSE)

## Author

[mokomoko511](https://github.com/mokomoko511)
