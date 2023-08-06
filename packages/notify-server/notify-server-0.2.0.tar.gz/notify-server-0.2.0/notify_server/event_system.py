class EventSystem:
    def __init__(self):
        self.callbacks = {}

    def send(self, event, data):
        event_data = {'type': 'event', 'event': event, 'data': data}
        for callback in self.callbacks.get(event, []):
            callback(event_data)

    def subscribe(self, event, callback):
        self.callbacks.setdefault(event, []).append(callback)

    def unsubscribe(self, event, callback):
        callbacks = self.callbacks[event]
        callbacks.remove(callback)
        if not callbacks:
            del self.callbacks[event]
