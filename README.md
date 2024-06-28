# Queue-API
API to simulate queue in real world
A Queue will last only 24 hours from the last modification. After 24 hours, it will be deleted.

Usage
-------
**Create New Queue**

```
https://luigiliu.com/openapi/queues/create/
```
This creates a new queue by responding its id. Response:
```
{
    "status": "success",
    "message": "New queue has been created, use https://luigiliu.com/api/queues/<queue_id>/ to access the queue information",
    "queue_id": <queue_id>
}
```

**View Queue Information**

```
https://luigiliu.com/openapi/queues/<queue_id>/
```
Response:
```
{
    "status": "success",
    "result": {
        "queue_info": {
            "id": <queue_id>,
            "time_created": "dd/mm/YYYY HH:MM:SS"
        },
        "waiting": {
            <waiter_id>: {
                "id": <waiter_id>,
                "name": <name>,
                "type": <type>,
                "start_waiting": "dd/mm/YYYY HH:MM:SS",
                "end_waiting": null,
                "start_processing": null,
                "end_processing": null
            }
        },
        "processing": {
            <waiter_id>: {
                "id": <waiter_id>,
                "name": <name>,
                "type": <type>,
                "start_waiting": "dd/mm/YYYY HH:MM:SS",
                "end_waiting": "dd/mm/YYYY HH:MM:SS",
                "start_processing": "dd/mm/YYYY HH:MM:SS",
                "end_processing": null
            }
        },
        "completed": {
            <waiter_id>: {
                "id": <waiter_id>,
                "name": <name>,
                "type": <type>,
                "start_waiting": "dd/mm/YYYY HH:MM:SS",
                "end_waiting": "dd/mm/YYYY HH:MM:SS",
                "start_processing": "dd/mm/YYYY HH:MM:SS",
                "end_processing": "dd/mm/YYYY HH:MM:SS"
            }
        }
    }
}
```

**Add Waiter to the Queue**

```
https://luigiliu.com/openapi/queues/<queue_id>/add_waiter/?name=<name>&type=<type>
```
Both name and type are optionals. Name is used to give custom name to the waiter, but only id is used to identify the waiter. Type is used to classify different waiters. If type is included, you can filter the expected waiting or processing time to each types.
Response:
```
{
    "status": "success",
    "result": {
        "id": <waiter_id>,
        "name": <name>,
        "type": <type>,
        "start_waiting": "dd/mm/YYYY HH:MM:SS",
        "end_waiting": null,
        "start_processing": null,
        "end_processing": null
    }
}
```

**Process Waiter**

```
https://luigiliu.com/openapi/queues/<queue_id>/process_next_waiter/
```
It changes the status from waiting to processing of the next waiter according to FIFO rule.

If you desire to process a specific waiter, you can use
```
https://luigiliu.com/openapi/queues/<queue_id>/process_waiter/<waiter_id>/
```

**Finish Processing Waiter**

```
https://luigiliu.com/openapi/queues/<queue_id>/finish_processing_waiter/<waiter_id>/
```
It changes the status from processing to completed of the waiter.

**Get Expected Waiting Time**

To get the expected waiting time of the a existing waiter, use
```
https://luigiliu.com/openapi/queues/<queue_id>/expected_waiting_time/<waiter_id>/
```
If type is included to the waiter, it will consider waiters of the same type.

To get the expected waiting time of the queue
```
https://luigiliu.com/openapi/queues/<queue_id>/expected_waiting_time/?type=<type>
```
If type is provided, it will consider waiters of the type. Otherwise, all waiters are considered.

**Get Expected Processing Time**

To get the expected waiting time of the queue
```
https://luigiliu.com/openapi/queues/<queue_id>/expected_processing_time/?type=<type>
```
If type is provided, it will consider waiters of the type. Otherwise, all waiters are considered.
