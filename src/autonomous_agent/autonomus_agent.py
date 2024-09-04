import threading
import queue
import time
from .logger import logger


class AutonomousAgent:
    def __init__(self) -> None:
        self.inbox = queue.Queue()
        self.outbox = queue.Queue()
        self.behaviours = []
        self.handlers = {}
        self.isRunning = True
        self.name = "Default"

    def register_handler(self, msg_type, handler):
        logger.info(f"Registering Handler: {handler}")
        self.handlers[msg_type] = handler

    def register_behaviour(self, behaviour):
        self.behaviours.append(behaviour)
        logger.info(f"Behavior registered: {behaviour}")

    def __process_messages(self):
        while self.isRunning:
            try:
                logger.info(f"{self.name}:: Reading message...")
                message = self.inbox.get(timeout=1)
                if message:
                    logger.info(f"{self.name}:: Message found: {message}")
                    msg_type, data = message
                    if msg_type in self.handlers:
                        self.handlers[msg_type](data)
                    self.inbox.task_done()
                else:
                    logger.info(f"{self.name}:: Message not found!!")
            except queue.Empty:
                logger.info(f"{self.name}:: Queue is Empty...")
                pass

    def __process_behaviour(self):
        while self.isRunning:
            for behaviour in self.behaviours:
                logger.info(f"{self.name}:: Processing behaviour {behaviour}...")
                behaviour(self)
                time.sleep(2)

    def start_autonomous_agent(self, name):
        logger.info(f"Starting autonomous agent {name}...")
        self.name = name

        behaviour_thread = threading.Thread(
            target=self.__process_behaviour, daemon=True
        )
        handler_thread = threading.Thread(target=self.__process_messages, daemon=True)

        behaviour_thread.start()
        handler_thread.start()

    def stop_autonomous_agent(self):
        logger.info("Stopping autonomous agent...")
        self.isRunning = False

    def send_inbox_message(self, msg_type, data):
        logger.info(
            f"{self.name}:: Sending inbox message: {msg_type} with data: {data}"
        )
        self.inbox.put((msg_type, data))

    def send_outbox_message(self, msg_type, data):
        logger.info(
            f"{self.name}:: Sending outbox message: {msg_type} with data: {data}"
        )
        self.outbox.put((msg_type, data))

    def get_outbox_message(self):
        try:
            message = self.outbox.get_nowait()
            logger.info(f"{self.name}:: Getting outbox message: {message}")
            return message
        except queue.Empty:
            return None

    def get_name(self):
        return self.name
