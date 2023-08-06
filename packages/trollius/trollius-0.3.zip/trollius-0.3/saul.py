import asyncio
import trollius
import dis

LOOP = 'asyncio'
#LOOP = 'trollius'

def aiodns_done(fut):
    print(fut, "is done")

@trollius.coroutine
def aiodns(loop):
    #fut = trollius.Future()
    fut = trollius.Future(loop=loop)
    print("fut.loop:", fut._loop)
    fut.add_done_callback(aiodns_done)
    loop.call_soon(fut.set_result, 42)

if LOOP == 'trollius':
    loop = trollius.get_event_loop()
    #asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
    #trollius.set_event_loop(loop)
print("event loop:", loop)

coro = aiodns(loop)
if LOOP == 'trollius':
    trollius.async(coro, loop=loop)
else:
    asyncio.async(coro, loop=loop)

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit (CTRL+c)")
finally:
    print("close")
    loop.stop()
    loop.close()

