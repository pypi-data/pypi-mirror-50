import datetime

import click

from ik_cli.cli import pass_context


def datetime_to_str(ctx, timestamp):
    try:
        # format_str = '%Y-%m-%d %H:%M:%S'
        print(timestamp)
        res = timestamp.isoformat(sep=' ', timespec='microseconds')
        return res
    except Exception as e:
        ctx.v_log(f"Input timestamp {timestamp} can not convert to str. errors: {e}")
        return None


def str_to_datetime(ctx, timestamp):
    if isinstance(timestamp, datetime.datetime):
        return timestamp
    if len(timestamp) <= 10:  # 2019-08-02
        format_str = '%Y-%m-%d'
    else:
        format_str = '%Y-%m-%d %H:%M:%S'
    try:
        timestamp = datetime.datetime.strptime(timestamp, format_str)
        return timestamp
    except ValueError:
        ctx.v_log(f"Input timestamp {timestamp} not match {format_str}")
        return None


@click.command('time', short_help='timestamp convert')
@click.argument('timestamp', nargs=1, default='')
@click.option('-ms', '--microsecond', is_flag=True, help='Use microsecond.')
@pass_context
def cli(ctx, timestamp, microsecond):
    if not timestamp:
        timestamp = datetime.datetime.now()
    o_timestamp = timestamp
    # check timestamp type: time_str or timestamp
    is_timestamp_to_time = True
    try:
        timestamp = int(timestamp)  # try
        microseconds = 0
        if microsecond:
            microseconds = timestamp % 1000000
            timestamp = timestamp // 1000000
            print(timestamp)
        res_time = datetime.datetime.fromtimestamp(timestamp)
        if microseconds:
            res_time = res_time.replace(microsecond=microseconds)
            print(res_time)
            print(res_time.microsecond)
    except (TypeError, ValueError) as e:
        if 'out of range' in str(e):
            ctx.log(f"Input timestamp {timestamp} too large.")
            return
        ctx.v_log(f"Input timestamp {timestamp} adjudged to datetime str, errors: {e}")
        is_timestamp_to_time = False

    if is_timestamp_to_time:
        res_time = datetime_to_str(ctx, res_time)
        ctx.log(f"Timestamp:  {o_timestamp}")
        ctx.log(f"Time:       {res_time}")
    else:
        res_time = str_to_datetime(ctx, timestamp)
        if res_time is not None:
            if microsecond:
                res_timestamp = int(round(res_time.timestamp() * 1000000))
            else:
                res_timestamp = int(res_time.timestamp())
            ctx.log(f"Timestamp:  {res_timestamp}")
            ctx.log(f"Time:       {o_timestamp}")
