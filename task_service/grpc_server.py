import asyncio
import grpc
from concurrent import futures

import tasks_pb2
import tasks_pb2_grpc

from repository import TasksRepository

class TaskServiceServicer(tasks_pb2_grpc.TaskServiceServicer):
    async def GetTasks(self, request, context):
        tasks = await TasksRepository.find_all()
        tasks_proto = [
            tasks_pb2.Task(
                id=task.id,
                name=task.name,
                description=task.description or ""
            )
            for task in tasks
        ]
        return tasks_pb2.TaskList(tasks=tasks_proto)

async def serve():
    server = grpc.aio.server()
    tasks_pb2_grpc.add_TaskServiceServicer_to_server(TaskServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("gRPC server is running on port 50051")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
