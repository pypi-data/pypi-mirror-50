Ik-cli

[![Build Status](https://travis-ci.org/MerleLiuKun/ik-cli.svg?branch=master)](https://travis-ci.org/MerleLiuKun/ik-cli)

## Introduction

This application provides some common command line tools for me.

## Install

You can use pip to install this tool.

```shell script
pip install ik-cli
```

## Usage

You can use main command to show all subcommands.

```shell script
ik_cli --help
# the echo are:
Usage: ik_cli [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose  Enable verbose mode.
  --help         Show this message and exit.

Commands:
  ip  get ip info

```

Now you can use `network` subcommand to get point ip info from `ip.sb`.

```shell script
ik_cli ip 8.8.8.8

# the echo is:
IP: 8.8.8.8
ASN: 15169
CONTINENT_CODE: NA
COUNTRY: United States
COUNTRY_CODE: US
LATITUDE: 37.751
LONGITUDE: -97.822
ORGANIZATION: Google LLC
TIMEZONE: America/Chicago
```