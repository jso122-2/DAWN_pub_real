import asyncio
import random
import time

COGNITIVE_STATES = ['introspective', 'analytical', 'expansive', 'adaptive', 'reflective', 'creative']

async def get_event_stream():
    current_state = 'introspective'
    while True:
        await asyncio.sleep(random.uniform(0.5, 2.5))
        now = int(time.time() * 1000)
        event_type = random.choices(
            ['pulse', 'mode_shift', 'fault', 'flux', 'intervention'],
            weights=[0.45, 0.2, 0.05, 0.2, 0.1]
        )[0]
        event = {'id': str(random.randint(100000, 999999)), 'type': event_type, 'timestamp': now, 'duration': random.randint(80, 200)}
        if event_type == 'pulse':
            patterns = ['α', 'β', 'γ', 'θ', 'δ']
            event['label'] = random.choice(patterns)
            event['data'] = {'pattern': event['label'], 'frequency': round(random.uniform(20, 100), 1), 'intensity': random.random()}
        elif event_type == 'mode_shift':
            to_state = random.choice(COGNITIVE_STATES)
            event['label'] = to_state.upper()
            event['data'] = {'from': current_state, 'to': to_state, 'trigger': 'neural cascade'}
            current_state = to_state
        elif event_type == 'fault':
            faults = ['LOOP', 'FRAGMENT', 'OVERFLOW', 'DESYNC']
            event['label'] = random.choice(faults)
            event['data'] = {'severity': 'high', 'recovery': random.randint(500, 1500)}
        elif event_type == 'flux':
            intensity = random.randint(0, 100)
            event['label'] = f"{intensity}%"
            event['data'] = {'channel': 'neural load', 'intensity': intensity}
        elif event_type == 'intervention':
            actions = ['STABILIZE', 'AMPLIFY', 'DAMPEN', 'REALIGN']
            event['label'] = random.choice(actions)
            event['data'] = {'action': event['label'], 'magnitude': random.random()}
        yield event 