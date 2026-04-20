import requests
from django.conf import settings


def notify_nextjs(type):
    try:
        res = requests.post(
           f"{settings.NEXTJS_URL}/api/revalidate?secret={settings.REVALIDATION_SECRET}" ,
           json={"type":type},
           timeout=5
        )
        print(f"Revalidation response:{res.status_code}{res.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Revalidation failed:{e}")