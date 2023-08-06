# Mark standard lib imports
import time, datetime, calendar
from decimal import Decimal

# Mark 3rd party lib imports
import lnt.rpc.rpc_pb2 as ln, lnt.rpc.rpc_pb2_grpc as lnrpc
import click, grpc

# Mark Local imports
from .utils import utils, rebal

def channel(ctx):
    stub, macaroon = utils.create_stub(ctx)

    # ListChannels RPC call
    request = ln.ListChannelsRequest(active_only=False)
    response = stub.ListChannels(request, metadata=[('macaroon', macaroon)])
    channels = utils.normalize_channels(response.channels)

    # GetChanInfo RPC call ( per channel )
    for ch_id in channels.keys():
        request = ln.ChanInfoRequest(chan_id=int(ch_id))
        response = stub.GetChanInfo(request, metadata=[('macaroon', macaroon)])
        chan_info = utils.normalize_get_chan_response(response)
        channels[ch_id] = { **channels[ch_id], **chan_info }
        
        # Prep for ForwardHistory call
        channels[ch_id]['forward_incoming'] = 0
        channels[ch_id]['forward_outgoing'] = 0


    # ForwardingHistory RPC call
    fwd_hist_start_time = calendar.timegm((datetime.date.today() - \
        datetime.timedelta(ctx.monthsago*365/12)).timetuple())

    fwd_hist_end_time = calendar.timegm(datetime.date.today().timetuple())

    request = ln.ForwardingHistoryRequest(
        start_time=fwd_hist_start_time,
        end_time=fwd_hist_end_time,
        num_max_events=10000
    )
    response = stub.ForwardingHistory(request, metadata=[('macaroon', macaroon)])

    for fwd_event in tuple(response.forwarding_events):
        try:
            channels[str(fwd_event.chan_id_in)]['forward_incoming'] += 1
        except KeyError:
            pass
        try:
            channels[str(fwd_event.chan_id_out)]['forward_outgoing'] += 1
        except KeyError:
            pass

    if not ctx.csv:
        header = "\n" + \
            "CHANNEL ID".ljust(21) + \
            "CAPACITY".ljust(11) + \
            "LOCAL_BAL".ljust(11) + \
            "LOCAL/CAP   " + \
            "FORWARDS   " + \
            "PENDING HTLCS   " + \
            "LAST USED"
    else:
        header = ",".join(["CHANNEL ID","CAPACITY","LOCAL_BAL","LOCAL/CAP","FORWARDS","PENDING HTLCS","LAST USED"])

    click.echo(header)
    for ch_id in channels.keys():
        channel = channels[ch_id]

        rows = []

        format_str = "{} {} {} {}% {} {} {}"
        if ctx.csv:
            format_str = "{},{},{},{}%,{},{},{}"

        if ctx.csv:
            prnt_str = format_str.format(
                            str(ch_id),
                            str(channel['capacity']),
                            str(channel['local_balance']),
                            str(round((Decimal(channel['local_balance'])/ \
                                Decimal(channel['capacity']))*100, 2)),
                            str(channel['forward_incoming'] + channel['forward_outgoing']),
                            str(len(channel['pending_htlcs'])),
                            time.strftime('%Y-%m-%d %H:%M', time.gmtime(channel['last_update'])),
                            )
        else:
            prnt_str = format_str.format(
                            str(ch_id).ljust(20),
                            str(channel['capacity']).ljust(10),
                            str(channel['local_balance']).ljust(10),
                            str(round((Decimal(channel['local_balance'])/ \
                                Decimal(channel['capacity']))*100, 2)).rjust(8),
                            str(channel['forward_incoming'] + channel['forward_outgoing']).ljust(10).rjust(12),
                            str(len(channel['pending_htlcs'])).ljust(15),
                            time.strftime('%Y-%m-%d %H:%M', time.gmtime(channel['last_update'])),
                            )

        click.echo(prnt_str)
    return