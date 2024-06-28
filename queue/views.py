
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache

from datetime import datetime, timedelta


class QueueCreateAPIView(APIView):

    def get(self, request):
        queue_ids = cache.get("queue_ids", [])
        new_queue_id = max(queue_ids) + 1 if queue_ids else 0
        queue_ids.append(new_queue_id)
        cache.set("queue_ids", queue_ids, timeout=None)
        queue_info = {
            "queue_info": {
                "id": new_queue_id,
                "time_created": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            },
            "waiting": {},
            "processing": {},
            "completed": {},
        }
        cache.set(f"queue_{new_queue_id}", queue_info, timeout=86400)
        queue_info_url = request.build_absolute_uri(f"/api/queues/{new_queue_id}/")
        response = {
            "status": "success",
            "message": f"New queue has been created, use {queue_info_url} to access the queue information",
            "queue_id": new_queue_id
        }
        return Response(response)
    
class QueueInfoAPIView(APIView):

    def get(self, request, queue_id):
        queue_info = cache.get(f"queue_{queue_id}")
        if queue_info is None:
            queue_creation_url = request.build_absolute_uri(f"/api/queues/create/")
            response = {
                "status": "error",
                "message": f"this queue id is not valid, please input a valid one or create a new queue in {queue_creation_url}"
            }
            return Response(response)
        
        response = {
            "status": "success",
            "result": queue_info
        }
        return Response(response)
    
class QueueAddWaiterAPIView(APIView):

    def get(self, request, queue_id):
        queue_info = cache.get(f"queue_{queue_id}")
        if queue_info is None:
            queue_creation_url = request.build_absolute_uri(f"/api/queues/create/")
            response = {
                "status": "error",
                "message": f"this queue id is not valid, please input a valid one or create a new queue in {queue_creation_url}"
            }
            return Response(response)
        name = request.GET.get("name", "")
        category = request.GET.get("type", "")
        waiter_id = len(queue_info["waiting"]) + len(queue_info["processing"]) + len(queue_info["completed"]) + 1
        waiter_info = {
            "id": waiter_id,
            "name": name,
            "type": category,
            "start_waiting": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "end_waiting": None,
            "start_processing": None,
            "end_processing": None,
        }
        queue_info["waiting"][waiter_id] = waiter_info
        cache.set(f"queue_{queue_id}", queue_info, timeout=86400)
        response = {
            "status": "success",
            "result": waiter_info
        }
        return Response(response)
  
    
class QueueProcessWaiterAPIView(APIView):

    def get(self, request, queue_id, waiter_id):
        queue_info = cache.get(f"queue_{queue_id}")
        if queue_info is None:
            queue_creation_url = request.build_absolute_uri(f"/api/queues/create/")
            response = {
                "status": "error",
                "message": f"this queue id is not valid, please input a valid one or create a new queue in {queue_creation_url}"
            }
            return Response(response)

        if waiter_id not in queue_info["waiting"]:
            waiter_addition_url = request.build_absolute_uri(f"/api/queues/{queue_id}/add_waiter/")
            response = {
                "status": "error",
                "message": f"this waiter is not in the queue, please add new waiter in {waiter_addition_url}"
            }
            return Response(response)
        
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        waiter_info = queue_info["waiting"].pop(waiter_id)
        waiter_info["end_waiting"] = time
        waiter_info["start_processing"] = time
        queue_info["processing"][waiter_id] = waiter_info

        cache.set(f"queue_{queue_id}", queue_info, timeout=86400)
        response = {
            "status": "success",
            "result": waiter_info
        }
        return Response(response)
class QueueProcessNextWaiterAPIView(APIView):

    def get(self, request, queue_id):
        queue_info = cache.get(f"queue_{queue_id}")
        if queue_info is None:
            queue_creation_url = request.build_absolute_uri(f"/api/queues/create/")
            response = {
                "status": "error",
                "message": f"this queue id is not valid, please input a valid one or create a new queue in {queue_creation_url}"
            }
            return Response(response)
        
        next_waiter = list(queue_info["waiting"].values())[0]
        next_waiter_start_waiting_datetime = datetime.strptime(next_waiter["start_waiting"], "%d/%m/%Y %H:%M:%S")
        for _, waiter_info in queue_info["waiting"].items():
            start_waiting_datetime = datetime.strptime(waiter_info["start_waiting"], "%d/%m/%Y %H:%M:%S")
            if start_waiting_datetime < next_waiter_start_waiting_datetime:
                next_waiter = waiter_info
                next_waiter_start_waiting_datetime = start_waiting_datetime

        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        waiter_info = queue_info["waiting"].pop(next_waiter["id"])
        waiter_info["end_waiting"] = time
        waiter_info["start_processing"] = time
        queue_info["processing"][waiter_info["id"]] = waiter_info

        cache.set(f"queue_{queue_id}", queue_info, timeout=86400)
        response = {
            "status": "success",
            "result": waiter_info
        }
        return Response(response)
    
class QueueFinishProcessingWaiterAPIView(APIView):

    def get(self, request, queue_id, waiter_id):
        queue_info = cache.get(f"queue_{queue_id}")
        if queue_info is None:
            queue_creation_url = request.build_absolute_uri(f"/api/queues/create/")
            response = {
                "status": "error",
                "message": f"this queue id is not valid, please input a valid one or create a new queue in {queue_creation_url}"
            }
            return Response(response)

        if waiter_id not in queue_info["processing"]:
            waiter_addition_url = request.build_absolute_uri(f"/api/queues/{queue_id}/add_waiter/")
            response = {
                "status": "error",
                "message": f"this waiter is not being processed, please start processing the waiter or add new waiter in {waiter_addition_url}"
            }
            return Response(response)
        
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        waiter_info = queue_info["processing"].pop(waiter_id)
        waiter_info["end_processing"] = time
        queue_info["completed"][waiter_id] = waiter_info

        cache.set(f"queue_{queue_id}", queue_info, timeout=86400)
        response = {
            "status": "success",
            "result": waiter_info
        }
        return Response(response)
  
    
class QueueExpectedWaitingTimeAPIView(APIView):

    def get(self, request, queue_id):
        queue_info = cache.get(f"queue_{queue_id}")
        if queue_info is None:
            queue_creation_url = request.build_absolute_uri(f"/api/queues/create/")
            response = {
                "status": "error",
                "message": f"this queue id is not valid, please input a valid one or create a new queue in {queue_creation_url}"
            }
            return Response(response)

        category = request.GET.get("type", None)
        total_waited_time = timedelta()
        
        for _, waiter_info in queue_info["processing"].items():
            if category and waiter_info["type"] != category: continue
            start_waiting_datetime = datetime.strptime(waiter_info["start_waiting"], "%d/%m/%Y %H:%M:%S")
            end_waiting_datetime = datetime.strptime(waiter_info["end_waiting"], "%d/%m/%Y %H:%M:%S")
            total_waited_time += end_waiting_datetime - start_waiting_datetime
        for _, waiter_info in queue_info["completed"].items():
            if category and waiter_info["type"] != category: continue
            start_waiting_datetime = datetime.strptime(waiter_info["start_waiting"], "%d/%m/%Y %H:%M:%S")
            end_waiting_datetime = datetime.strptime(waiter_info["end_waiting"], "%d/%m/%Y %H:%M:%S")
            total_waited_time += end_waiting_datetime - start_waiting_datetime
        number_waiter_processing_or_completed = len(queue_info["processing"]) + len(queue_info["completed"])
        number_waiter_waiting = 0
        for _, waiter_info in queue_info["waiting"].items():
            if category and waiter_info["type"] != category: continue
            number_waiter_waiting += 1
        expected_waiting_time = (total_waited_time / number_waiter_processing_or_completed)*number_waiter_waiting if number_waiter_processing_or_completed > 0 else timedelta()
        
        
        response = {
            "status": "success",
            "message": f"The expected waiting time is {expected_waiting_time}",
        }
        return Response(response)
    
class QueueWaiterExpectedWaitingTimeAPIView(APIView):

    def get(self, request, queue_id, waiter_id):
        queue_info = cache.get(f"queue_{queue_id}")
        if queue_info is None:
            queue_creation_url = request.build_absolute_uri(f"/api/queues/create/")
            response = {
                "status": "error",
                "message": f"this queue id is not valid, please input a valid one or create a new queue in {queue_creation_url}"
            }
            return Response(response)
        
        if waiter_id not in queue_info["waiting"]:
            waiter_addition_url = request.build_absolute_uri(f"/api/queues/{queue_id}/add_waiter/")
            response = {
                "status": "error",
                "message": f"this waiter is not in the queue, please add new waiter in {waiter_addition_url}"
            }
            return Response(response)


        this_waiter_start_waiting_datetime = datetime.strptime(queue_info["waiting"][waiter_id]["start_waiting"], "%d/%m/%Y %H:%M:%S")
        category = queue_info["waiting"][waiter_id]["type"]
        
        total_waited_time = timedelta()
        
        for _, waiter_info in queue_info["processing"].items():
            if category and waiter_info["type"] != category: continue
            start_waiting_datetime = datetime.strptime(waiter_info["start_waiting"], "%d/%m/%Y %H:%M:%S")
            if start_waiting_datetime > this_waiter_start_waiting_datetime: continue
            end_waiting_datetime = datetime.strptime(waiter_info["end_waiting"], "%d/%m/%Y %H:%M:%S")
            total_waited_time += end_waiting_datetime - start_waiting_datetime
        for _, waiter_info in queue_info["completed"].items():
            if category and waiter_info["type"] != category: continue
            start_waiting_datetime = datetime.strptime(waiter_info["start_waiting"], "%d/%m/%Y %H:%M:%S")
            if start_waiting_datetime > this_waiter_start_waiting_datetime: continue
            end_waiting_datetime = datetime.strptime(waiter_info["end_waiting"], "%d/%m/%Y %H:%M:%S")
            total_waited_time += end_waiting_datetime - start_waiting_datetime
        number_waiter_processing_or_completed = len(queue_info["processing"]) + len(queue_info["completed"])
        number_waiter_waiting = 0
        for _, waiter_info in queue_info["waiting"].items():
            if category and waiter_info["type"] != category: continue
            start_waiting_datetime = datetime.strptime(waiter_info["start_waiting"], "%d/%m/%Y %H:%M:%S")
            if start_waiting_datetime > this_waiter_start_waiting_datetime: continue
            number_waiter_waiting += 1
        expected_waiting_time = (total_waited_time / number_waiter_processing_or_completed)*number_waiter_waiting if number_waiter_processing_or_completed > 0 else timedelta()
        
        
        response = {
            "status": "success",
            "message": f"The expected waiting time is {expected_waiting_time}",
        }
        return Response(response)
    
class QueueExpectedProcessingTimeAPIView(APIView):

    def get(self, request, queue_id):
        queue_info = cache.get(f"queue_{queue_id}")
        if queue_info is None:
            queue_creation_url = request.build_absolute_uri(f"/api/queues/create/")
            response = {
                "status": "error",
                "message": f"this queue id is not valid, please input a valid one or create a new queue in {queue_creation_url}"
            }
            return Response(response)

        category = request.GET.get("type", None)
        total_waited_time = timedelta()
        number_waiter_completed = 0
        for _, waiter_info in queue_info["completed"].items():
            if category and waiter_info["type"] != category: continue
            start_processing_datetime = datetime.strptime(waiter_info["start_processing"], "%d/%m/%Y %H:%M:%S")
            end_processing_datetime = datetime.strptime(waiter_info["end_processing"], "%d/%m/%Y %H:%M:%S")
            total_waited_time += end_processing_datetime - start_processing_datetime
            number_waiter_completed += 1
        expected_processing_time = total_waited_time / number_waiter_completed if number_waiter_completed > 0 else timedelta()
        
        
        response = {
            "status": "success",
            "message": f"The expected processing time is {expected_processing_time}",
        }
        return Response(response)