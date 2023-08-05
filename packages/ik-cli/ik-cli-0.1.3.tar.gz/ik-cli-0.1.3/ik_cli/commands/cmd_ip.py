import click
import requests
from requests.exceptions import Timeout

from . import constant
from .models import IpInfo
from ik_cli.cli import pass_context


@click.command('ip', short_help='get ip info')
@click.argument('ip', nargs=1)
@click.option('-m', '--mode', type=str, default='net', help='Now only support `net`')
@pass_context
def cli(ctx, ip, mode):
    if not ip:
        ip = ''
    if mode == 'net':
        session = requests.session()
        try:
            ctx.v_log(f'Now begin to retrieve ip: {ip} info from ip.sb')
            uri = constant.NETWORK_IP_SB_URI + ip
            resp = session.get(uri)
            if resp.ok:
                ip_info = IpInfo.build_info(resp.json())
                click.echo(f'---- IP {ip_info.ip} Status ----')
                click.echo(f'IP:              {ip_info.ip}')
                click.echo(f'ASN:             {ip_info.asn}')
                click.echo(f'CONTINENT_CODE:  {ip_info.continent_code}')
                click.echo(f'COUNTRY:         {ip_info.country}')
                click.echo(f'COUNTRY_CODE:    {ip_info.country_code}')
                click.echo(f'LATITUDE:        {ip_info.latitude}')
                click.echo(f'LONGITUDE:       {ip_info.longitude}')
                click.echo(f'ORGANIZATION:    {ip_info.organization}')
                click.echo(f'TIMEZONE:        {ip_info.timezone}')
                if ip_info.postal_code:
                    click.echo(f'POSTAL_CODE:     {ip_info.postal_code}')
                if ip_info.region:
                    click.echo(f'REGION:          {ip_info.region}')
                if ip_info.region_code:
                    click.echo(f'REGION_CODE:     {ip_info.region_code}')
            if resp.status_code == 400:
                ctx.log(f'Input string for {ip} is not a valid IP address')
        except Timeout as e:
            ctx.log('Ops. Maybe your internet not work.', color='red')
            ctx.v_log(f'Exception in get data from net. errors: {e}')
        except Exception as e:
            ctx.log('Ops. Some wrong appear. Please retry.', color='red')
            ctx.v_log(f'Exception in get data from net. errors: {e}')
    else:
        ctx.log(f"This mode for {mode} not implement")
