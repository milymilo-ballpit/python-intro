from lightkube import Client
from lightkube.resources.apps_v1 import Deployment
from lightkube.models.meta_v1 import ObjectMeta
from lightkube.models.autoscaling_v1 import ScaleSpec
from lightkube.resources.core_v1 import Pod

client = Client()

print("Pods before scaling:")
for pod in client.list(Pod, namespace="test", labels={"test-label": "test-value"}):
    print(pod.metadata.name)

deploy = Deployment.Scale(
    metadata=ObjectMeta(name="nginx-deployment", namespace="test"),
    spec=ScaleSpec(replicas=5),
)
client.replace(deploy)

for op, dep in client.watch(Deployment, namespace="test"):
    if dep.status.readyReplicas == deploy.spec.replicas:
        break

print("Pods after scaling:")
for pod in client.list(Pod, namespace="test"):
    print(pod.metadata.name)
