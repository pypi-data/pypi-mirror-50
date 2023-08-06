import click
import socket
import requests
from requests.exceptions import ConnectionError

from . import constant
from .models import IpInfo
from ik_cli.cli import pass_context


def get_ip_from_net(ctx, ip):
    session = requests.session()
    try:
        ctx.v_log(f'Now begin to retrieve ip: {ip} info from ip.sb')
        uri = constant.IP_SB_URI + ip
        resp = session.get(uri)
        if resp.ok:
            ip_info = IpInfo.build_info(resp.json())
            ctx.log(f'---- IP {ip_info.ip} Status ----')
            ctx.log(f'IP:              {ip_info.ip}')
            ctx.log(f'ASN:             {ip_info.asn}')
            ctx.log(f'CONTINENT_CODE:  {ip_info.continent_code}')
            ctx.log(f'COUNTRY:         {ip_info.country}')
            ctx.log(f'COUNTRY_CODE:    {ip_info.country_code}')
            ctx.log(f'LATITUDE:        {ip_info.latitude}')
            ctx.log(f'LONGITUDE:       {ip_info.longitude}')
            ctx.log(f'ORGANIZATION:    {ip_info.organization}')
            ctx.log(f'TIMEZONE:        {ip_info.timezone}')
            if ip_info.postal_code:
                ctx.log(f'POSTAL_CODE:     {ip_info.postal_code}')
            if ip_info.region:
                ctx.log(f'REGION:          {ip_info.region}')
            if ip_info.region_code:
                ctx.log(f'REGION_CODE:     {ip_info.region_code}')
        if resp.status_code == 400:
            ctx.log(f'Input string for {ip} is not a valid IP address')
    except ConnectionError as e:
        ctx.log('Ops. Maybe your internet not work. Please check you network', color='red')
        ctx.v_log(f'Exception in get data from net. errors: {e}')
    except Exception as e:
        ctx.log('Ops. Some wrong appear. Please retry.')
        ctx.v_log(f'Exception in get data from net. errors: {e}')


def get_host_ip(ctx):
    # first try use socket udp and need network
    ctx.v_log("Now try use socket udp to get host ip...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ctx.v_log(f"connecting to {constant.IP_UDP_ADDRESS}....")
        s.connect((constant.IP_UDP_ADDRESS, 80))
        sock_name = s.getsockname()
        ctx.log(f'Your IP:  {sock_name[0]}')
        ctx.log(f'Method:   UDP')
        return
    except OSError as e:
        ctx.v_log(f"Exception in connect to {constant.IP_UDP_ADDRESS}, errors: {e}")

    # try use get hostname but not correct
    ctx.v_log("Now try use socket udp to get host ip...")
    try:
        ip = socket.gethostbyname(socket.gethostname())
        ctx.log(f'Your IP:  {ip}')
        ctx.log(f'Method:   hostname')
        return
    except Exception as e:
        ctx.v_log(f"Exception in get ip by hostname, errors: {e}")

    ctx.log('Ops. Can not get your ip.')


@click.command('ip', short_help='get ip info')
@click.argument('ip', nargs=1, default='')
@click.option('-m', '--mode', type=str, default='net', help='Now only support `net`, `host`')
@pass_context
def cli(ctx, ip, mode):
    if not ip:
        ip = ''
    if mode == 'net':
        get_ip_from_net(ctx, ip)
    elif mode == 'host':
        get_host_ip(ctx)
    else:
        ctx.log(f"This mode for {mode} not implement")
