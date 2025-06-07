import asyncio
from kubernetes_asyncio import client, config


async def main():
    await config.load_kube_config()
    v1 = client.CoreV1Api()
    apps = client.AppsV1Api()

    print("Pods before scaling:")
    pods = await v1.list_namespaced_pod(
        namespace="test",
        label_selector="test-label=test-value",
    )
    for pod in pods.items:
        print(pod.metadata.name)

    scale = client.V1Scale(spec=client.V1ScaleSpec(replicas=5))
    await apps.patch_namespaced_deployment_scale(
        name="nginx-deployment",
        namespace="test",
        body=scale,
    )

    while True:
        dep = await apps.read_namespaced_deployment_status("nginx-deployment", "test")
        if dep.status.ready_replicas == dep.spec.replicas:
            break
        await asyncio.sleep(1)

    print("Pods after scaling:")
    pods = await v1.list_namespaced_pod(namespace="test")
    for pod in pods.items:
        print(pod.metadata.name)


if __name__ == "__main__":
    asyncio.run(main())
