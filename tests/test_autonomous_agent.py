import unittest
import time

from src.autonomous_agent.autonomus_agent import AutonomousAgent


class TestAutonomousAgent(unittest.TestCase):

    def test_message_handler(self):
        test_agent = AutonomousAgent()
        test_message = "hello world"

        def handler(message):
            self.assertIn("hello", message)

        test_agent.register_handler("test", handler)
        test_agent.send_inbox_message("test", test_message)

        test_agent.start_autonomous_agent("TestAgent")
        time.sleep(1)
        test_agent.stop_autonomous_agent()

    def test_behaviour_generation(self):
        test_agent = AutonomousAgent()

        def behaviour(agent):
            agent.send_outbox_message("test", "hello world")

        test_agent.register_behaviour(behaviour)
        test_agent.start_autonomous_agent("TestAgent")

        time.sleep(2)
        message = test_agent.get_outbox_message()
        self.assertIsNotNone(message)
        self.assertEqual(message, ("test", "hello world"))

        test_agent.stop_autonomous_agent()

    def test_integration_between_agents(self):
        test_agent1 = AutonomousAgent()
        test_agent2 = AutonomousAgent()

        received_message = []

        def handler(message):
            received_message.append(message)

        def behaviour(agent):
            agent.send_outbox_message("test", "hello universe")

        test_agent1.register_handler("test", handler)
        test_agent2.register_behaviour(behaviour)

        test_agent1.start_autonomous_agent("Agent1")
        test_agent2.start_autonomous_agent("Agent2")

        time.sleep(3)

        msg = test_agent2.get_outbox_message()
        if msg:
            test_agent1.send_inbox_message(*msg)

        time.sleep(1)  # Allow time for message processing

        test_agent1.stop_autonomous_agent()
        test_agent2.stop_autonomous_agent()

        self.assertIn("hello universe", received_message)


if __name__ == "__main__":
    unittest.main()
