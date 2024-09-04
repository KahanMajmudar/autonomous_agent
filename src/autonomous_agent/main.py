import random
import time
import threading
from .autonomus_agent import AutonomousAgent
from .logger import logger


word_to_find = "hello"
random_words = [
    "hello",
    "sun",
    "world",
    "space",
    "moon",
    "crypto",
    "sky",
    "ocean",
    "universe",
    "human",
]


def hello_filter_handler(message):
    logger.info(f"Inside filter: {message}")
    if word_to_find in message:
        logger.info("Filter word found")
    else:
        logger.info(f"Filter not found in message: {message}")


def random_word_gen_behaviour(autonomous_agent):
    words = random.sample(random_words, 2)
    logger.info(f"Words selected: {words}")
    message = " ".join(words)
    autonomous_agent.send_outbox_message("random_word_gen", message)


def init_messages(agent_to_send, agent_to_receive):
    if agent_to_receive.isRunning:
        logger.info(
            f"Agent {agent_to_receive.get_name()} is running, sending init messsage..."
        )
        message = agent_to_send.get_outbox_message()
        if message:
            logger.info(f"Init found: {message}")
            agent_to_receive.send_inbox_message(*message)
        else:
            logger.info("No message found to send")
        time.sleep(1)


def main():
    logger.info("Setting up autonomous agents")
    autonomous_agent_one = AutonomousAgent()
    autonomous_agent_two = AutonomousAgent()

    logger.info("Setting up autonomous agent one's handler and behaviour")
    autonomous_agent_one.register_handler("random_word_gen", hello_filter_handler)
    autonomous_agent_one.register_behaviour(random_word_gen_behaviour)

    logger.info("Setting up autonomous agent two's handler and behaviour")
    autonomous_agent_two.register_handler("random_word_gen", hello_filter_handler)
    autonomous_agent_two.register_behaviour(random_word_gen_behaviour)

    time.sleep(2)

    autonomous_agent_one.start_autonomous_agent("One")
    autonomous_agent_two.start_autonomous_agent("Two")

    threads = []

    thread_agent_two = threading.Thread(
        target=init_messages(autonomous_agent_two, autonomous_agent_one),
    )
    threads.append(thread_agent_two)

    thread_agent_one = threading.Thread(
        target=init_messages(autonomous_agent_one, autonomous_agent_two),
    )
    threads.append(thread_agent_one)

    thread_agent_two.start()
    thread_agent_one.start()

    for thread_obj in threads:
        thread_obj.join()

    time.sleep(6)

    logger.info("Stopping autonomous agent one")
    autonomous_agent_one.stop_autonomous_agent()
    logger.info("Stopping autonomous agent two")
    autonomous_agent_two.stop_autonomous_agent()


if __name__ == "__main__":
    main()
