import pyglet
window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')
a=0

@window.event
def on_draw():
    global a
    window.clear()
    label.draw()
    print(a)
    a+=1

class CustomLoop(pyglet.app.EventLoop):
  def idle(self):    
    dt = self.clock.update_time()
    self.clock.call_scheduled_functions(dt)

    # Redraw all windows
    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_event('on_draw')
        window.flip()
        window._legacy_invalid = False

    # no timout (sleep-time between idle()-calls)
    return 0

event_loop = CustomLoop()
event_loop.run()
