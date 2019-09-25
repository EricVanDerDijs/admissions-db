import asyncio, functools
from .formater import formatRequest
from .reqreader import Reader

class Go:
  def __init__(
    self,
    verb,
    route,
    *,
    sock = None,
    body = {},
    header = {},
  ):
    if sock is None:
      raise Exception('socket is missing!')
    else:
      self._sock = sock
      self.req = formatRequest(verb, route, body = body, header = header)

  async def as_coroutine(self):
    if self.req is not None:
      reader = Reader(self._sock)
      loop = asyncio.get_event_loop()
      # Send req
      try:
        await loop.sock_sendall(self._sock, self.req)
      except Exception as e:
        print(f'sendall() err: {e}')
        return None # Error Sending
      # Read res
      try:
        res = await asyncio.wait_for(
          reader.read(),
          10,
        )
        return res
      except asyncio.TimeoutError:
        return None
    else:
      return None


  def with_callback(self, callback = None, args = ()):
    if callback is None:
      raise Exception('Callback is missing!')
    else:
      loop = asyncio.get_event_loop()
      cb_with_args = functools.partial(callback, *args)
      task = loop.create_task( self.as_coroutine() )
      task.add_done_callback( cb_with_args )
      if not loop.is_running():
        loop.run_until_complete( task )
  