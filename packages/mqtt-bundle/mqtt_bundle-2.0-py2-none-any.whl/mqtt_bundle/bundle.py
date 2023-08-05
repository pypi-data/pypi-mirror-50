from applauncher.kernel import KernelReadyEvent, Configuration, KernelShutdownEvent, Kernel, Event, ConfigurationReadyEvent, EventManager, KernelShutdownEvent
import inject
import threading
import paho.mqtt.client as mqtt
import logging


class MqttMessageEvent(Event):

    event_name = "mqtt.message"

    def __init__(self, client, userdata, message):
        self.client = client
        self.userdata = userdata
        self.message = message


class MqttTopicEvent(Event):
    event_name = "mqtt.topic_event"



class MqttTopicManager(object):
    """Not in the main bundle to split functionalities. The bundle will use this manager as a proxy"""

    def __init__(self, client: mqtt.Client):
        self.client = client
        self.events = {}

    def _consume_event(self, event):
        if event.message.topic in self.events:
            for subscriber_callback in self.events[event.message.topic]:
                subscriber_callback(event.message.payload)

    def subscribe(self, event, callback):
        self.events.setdefault(event.topic, []).append(callback)
        self.client.subscribe(event.topic)

    def publish(self, event, qos=0, retain=False):
        self.client.publish(event.topic, event.payload, qos, retain)


class MqttBundle(object):

    def __init__(self):

        self.config_mapping = {
            "mqtt": {
                "host": None
            }
        }

        self.logger = logging.getLogger("mqtt")
        self.client = mqtt.Client()
        self.client.on_message = self._on_message

        self.injection_bindings = {
            mqtt.Client: self.client
        }
        self.lock = threading.Lock()

        self.event_listeners = [
            (ConfigurationReadyEvent, self.configuration_ready),
            (KernelReadyEvent, self.kernel_ready),
            (KernelShutdownEvent, self.kernel_shutdown),
            (MqttMessageEvent, self.notify_topic_event)
        ]

    @inject.params(event_manager=EventManager)
    def _on_message(self, client, userdata, message, event_manager: EventManager):
        event_manager.dispatch(MqttMessageEvent(client, userdata, message))

    @inject.params(topic_manager=MqttTopicManager)
    def notify_topic_event(self, event, topic_manager: MqttTopicManager):
        try:
            topic_manager._consume_event(event)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e

    def kernel_shutdown(self, event):
        self.logger.info("Disconnecting from mqtt...")
        self.client.disconnect()
        self.client.loop_stop(force=False)
        self.lock.release()
        self.logger.info("Disconnected")


    @inject.params(kernel=Kernel)
    def kernel_ready(self, event, kernel):
        self.lock.acquire()
        kernel.run_service(lambda lock: lock.acquire(), self.lock)


    def configuration_ready(self, event):
        # First connect the topic manager to avoid lose messages
        self.injection_bindings[MqttTopicManager] = MqttTopicManager(self.client)
        config = event.configuration
        self.client.connect(config.mqtt.host)
        self.client.loop_start()
        self.logger.info("Connected to {host} and ready".format(host=config.mqtt.host))
