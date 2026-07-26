from typing import Callable, Dict
from .entities import NormEvent

class EventBus:
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        print(f"✅ Subscribed to {event_type}")
    
    def publish(self, event: NormEvent):
        print(f"📤 Event published: {event.type} (id: {event.id})")
        if event.type in self.handlers:
            for handler in self.handlers[event.type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in handler: {e}")
