import json
from consumer import Consumer
# from pymercure.publisher.sync import SyncPublisher
#
# a = json.dumps({'status': 'test'})
# p = SyncPublisher(
#     'http://127.0.0.1:3000/hub',
#     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjdXJlIjp7InB1Ymxpc2giOltdfX0.FFSjymJCGRDWrmAmPJDoVGuYwnx5FRTjRFkkYfvLkUg'
# )
# p.publish(['mytopicname'], a)


def callback(message):
    print(message.data)


c = Consumer('http://127.0.0.1:3000/hub', ['mytopicname'], callback)
c.start_consumption()
