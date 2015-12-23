import datetime
import asyncio
from aiohttp import web

async def send_time(ws):
    while True:
        ws.send_str(str(datetime.datetime.now()))
        await asyncio.sleep(1)

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await asyncio.gather(send_time(ws))
    return ws


if __name__ == '__main__':
    app = web.Application()
    app.router.add_route('GET', '/ws', websocket_handler)
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    f = loop.create_server(handler, '0.0.0.0', '8090')
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        STOPPING = True
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()
