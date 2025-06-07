import time

import kr8s
from kr8s.objects import Deployment

print("Pods before scaling: ")
labels = {'test-label': 'test-value'}
for pod in kr8s.get("pods", namespace="test", label_selector=labels):
    print(pod.name)

deploy = Deployment("nginx-deployment", namespace="test")
deploy.scale(5)

while not deploy.ready():
    time.sleep(1)

print("Pods after scaling: ")
for pod in kr8s.get("pods", namespace="test"):
    print(pod.name)