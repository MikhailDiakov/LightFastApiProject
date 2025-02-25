import asyncio
import grpc
import logging
import argparse
import os
import time

from rich.console import Console
from rich.table import Table

import tasks_pb2
import tasks_pb2_grpc

logging.basicConfig(level=logging.INFO)
console = Console()

async def get_tasks(server_address: str):
    async with grpc.aio.insecure_channel(server_address) as channel:
        stub = tasks_pb2_grpc.TaskServiceStub(channel)
        try:
            response = await stub.GetTasks(tasks_pb2.Empty(), timeout=5)
            return response.tasks
        except grpc.aio.AioRpcError as e:
            logging.error("gRPC error occurred: %s", e)
            return []

def display_tasks(tasks):
    os.system('cls' if os.name == 'nt' else 'clear')

    table = Table(title="Task List")

    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="green")

    if tasks:
        for task in tasks:
            table.add_row(str(task.id), task.name, task.description)
    else:
        table.add_row("N/A", "No tasks", "No data available")

    console.print(table)

async def periodic_get_tasks(server_address: str, interval: int):
    while True:
        try:
            tasks = await get_tasks(server_address)
            display_tasks(tasks)
        except grpc.aio.AioRpcError as e:
            logging.error(f"Failed to get tasks: {e}")
            logging.info("Retrying in 5 seconds...")
        await asyncio.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description="gRPC client for TaskService")
    parser.add_argument('--server', default='task_service:50051', help='Server address (default: task_service:50051)')
    parser.add_argument('--interval', type=int, default=10, help='Polling interval in seconds (default: 10)')
    args = parser.parse_args()

    logging.info(f"Attempting to connect to gRPC server at {args.server}...")
    asyncio.run(periodic_get_tasks(args.server, args.interval))

if __name__ == '__main__':
    main()
