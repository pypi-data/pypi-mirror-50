# KLplus

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://github.com/danbros/KLplus/blob/master/LICENSE)
[![Python 3.6](https://img.shields.io/badge/Python-3.6+-red.svg)](https://www.python.org/downloads/)
[![Maintenance yes](https://img.shields.io/badge/Mantido%3F-yes-green.svg)](https://github.com/danbros/KLplus/graphs/commit-activity)
[![PyPI](https://img.shields.io/pypi/v/KLplus.svg?color=green&label=pypi%20release)](https://pypi.org/project/KLplus/#history)
![PyPI - Downloads](https://img.shields.io/pypi/dm/KLplus.svg?label=PyPi%20Downloads)

Um [Keylogger](https://pt.wikipedia.org/wiki/Keylogger) CLI para OS Linux baseado no principio [KISS](https://pt.wikipedia.org/wiki/Princ%C3%ADpio_KISS).<br>

O objetivo deste pacote é entregar um keylogger minimalista, configurável por linha de comando e principalmente confiável.


## Conteúdo
* [Guia de Instalação](#Guia-de-Instalação)
    * [Requisitos](#Requisitos)
    * [Instalação](#Instalação)
* [Configurando](#Configurando)
* [Autoria e contribuições](#Autoria-e-contribuições)
* [Licença](#Licença)



### Guia de Instalação

#### Requisitos:

Para executar este aplicativo você precisa de um interpretador [Python 3.6+](https://www.python.org/downloads/) disponivel em seu OS Linux.  
Para obter uma lista dos interpretadores Python do seu sistema, digite no Shell:
```Shell
$ ls -1 /usr/bin/python* | grep '[2-3].[0-9]$'
# Ou
$ find /usr/bin/python* ! -type l
# Ou isso no caso de estar usando ambientes virtuais
$ whereis python
```
Você pode instalar o Python com:
```Shell
# OS Debian/Ubuntu
$ sudo apt-get -y install python3.7
```


#### Instalação:

De sua linha de comando:
```Shell
# Instalar dependências via Pypi
$ pip install KLplus

# Ou

# Instalar dependências via Pypi pelo Python 3 (necessário se
# Python 3 estiver instalado e não for o padrão do sistema)
$ python3 -m pip install KLplus
```
Ou:
```Shell
# Clonar este repositório e instalar (necessário wheel):
$ pip install https://github.com/danbros/KLplus/releases/download/v0.1.2/KLplus-0.1.1-py3-none-any.whl
```

Alternativas:
```Shell
# Instalar via GIT e .egg
$ pip install git+https://github.com/danbros/KLplus.git#egg=KLplus

# Via .zip
$ pip install https://github.com/danbros/KLplus/archive/master.zip
```


### Configurando

Voçê pode iniciar o keylogger do terminal com:  
```Shell
$ python -m KLplus & disown -h %1
```
Assim ele é executado em segundo plano, podendo fechar o terminal
sem destruir seu processo.

<br>

Ele captura todas as teclas digitadas até que o comando de saída seja pressionado (F12), e então finaliza.

O log capturado fica armazenado no mesmo diretório do módulo klplus. Insira esse comando se precisar descobrir o diretório.  
```Shell
$ { pip show KLplus | grep Loc; echo "/KLplus/log.txt"; } | sed 'N;s/\n//'
```  
Ou faça `pip show KLplus` e olhe para `Location`.


### Autoria e contribuições

[**pyxhook.py**](https://github.com/danbros/KLplus/blob/release-0.1.1/KLplus/pyxhook.py)  
* Uma implementação do [**pyHook**](https://pypi.org/project/pyHook/) (Windows) para sistemas Linux.  Clonado do repositório de [JeffHoogland](https://github.com/JeffHoogland/pyxhook), é um pedaço do código fonte de [**Simple Python Keylogger**](https://sourceforge.net/projects/pykeylogger/), sob licença GPL v2.


### Licença
* [Licença GNU GPLv2](https://github.com/danbros/KLplus/blob/release-0.1.1/LICENSE)
* Copyright 2019, Dan Barros.
