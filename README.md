# Queue-API
API to simulate queue in real world

Usage
-------
Create New Queue
```
https://luigiliu.com/openapi/queues/create/
```
This creates a new queue by responding its id. Response:
```
{
    "status": "success",
    "message": "New queue has been created, use https://luigiliu.com/api/queues/<id>/ to access the queue information",
    "queue_id": <id>
}
```
