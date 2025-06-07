from kubernetes import client, config
import time

config.load_kube_config()
v1 = client.CoreV1Api()
apps = client.AppsV1Api()

print("Pods before scaling:")
for pod in v1.list_namespaced_pod(
    namespace="test",
    label_selector="test-label=test-value",
).items:
    print(pod.metadata.name)

apps.patch_namespaced_deployment_scale(
    name="nginx-deployment",
    namespace="test",
    body=client.V1Scale(spec=client.V1ScaleSpec(replicas=5)),
)

while True:
    dep = apps.read_namespaced_deployment_status("nginx-deployment", "test")
    if dep.status.ready_replicas == dep.spec.replicas:
        break
    time.sleep(1)

print("Pods after scaling:")
for pod in v1.list_namespaced_pod(namespace="test").items:
    print(pod.metadata.name)
