import asyncio
import websockets
import json
import random
import time
import argparse
from datetime import datetime

# Event types and labels for testing
EVENT_TYPES = [
    'pulse', 'mode_shift', 'fault', 'flux', 'intervention'
]
MODE_LABELS = ['idle', 'active', 'learning', 'dreaming', 'maintenance']
FAULT_LABELS = ['overload', 'timeout', 'disconnect', 'corruption', 'drift']
INTERVENTION_LABELS = ['reset', 'recalibrate', 'boost', 'suppress']

WS_HOST = 'localhost'
WS_PORT = 8080
WS_PATH = '/consciousness/timeline'

parser = argparse.ArgumentParser(description='Synthetic Timeline Event Generator')
parser.add_argument('--events-per-second', type=int, default=5, help='Events per second')
parser.add_argument('--duration', type=int, default=60, help='Duration in seconds')
args = parser.parse_args()

async def send_events():
    uri = f"ws://{WS_HOST}:{WS_PORT}{WS_PATH}"
    print(f"Connecting to {uri}")
    async with websockets.connect(uri) as ws:
        start_time = time.time()
        event_count = 0
        while time.time() - start_time < args.duration:
            now = datetime.utcnow().isoformat() + 'Z'
            events = []
            for _ in range(args.events_per_second):
                event_type = random.choice(EVENT_TYPES)
                event = {
                    'timestamp': now,
                    'type': event_type,
                    'id': f"evt-{int(time.time() * 1000)}-{random.randint(1000,9999)}",
                    'label': None,
                    'value': None,
                    'details': {},
                }
                # Add event-specific fields
                if event_type == 'mode_shift':
                    event['label'] = random.choice(MODE_LABELS)
                    event['details']['from'] = random.choice(MODE_LABELS)
                    event['details']['to'] = event['label']
                elif event_type == 'fault':
                    event['label'] = random.choice(FAULT_LABELS)
                    event['details']['severity'] = random.choice(['low', 'medium', 'high', 'critical'])
                    # Fault injection: occasionally send malformed event
                    if random.random() < 0.1:
                        event['details']['corrupt'] = True
                        if random.random() < 0.5:
                            del event['type']  # Remove type to simulate error
                elif event_type == 'flux':
                    event['label'] = 'load_change'
                    event['value'] = round(random.uniform(0.1, 1.0), 3)
                    event['details']['trend'] = random.choice(['up', 'down', 'stable'])
                elif event_type == 'intervention':
                    event['label'] = random.choice(INTERVENTION_LABELS)
                    event['details']['success'] = random.choice([True, False])
                elif event_type == 'pulse':
                    event['label'] = 'tick'
                    event['value'] = int(time.time() * 1000) % 10000
                events.append(event)
                event_count += 1
            # Send all events
            for event in events:
                try:
                    await ws.send(json.dumps(event))
                except Exception as e:
                    print(f"Failed to send event: {e}")
            await asyncio.sleep(1.0 / args.events_per_second)
        print(f"Sent {event_count} events in {args.duration} seconds.")

if __name__ == '__main__':
    asyncio.run(send_events()) 