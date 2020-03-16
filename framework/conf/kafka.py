from conf.configuration import Configuration
import json


class KafkaTopicConfiguration(Configuration):
    filename = 'kafka_topics.ini'

    @property
    def properties(self):
        self.props = super().properties
        # if type(self.props['default.topic.config']) ==  type(str):
        self.props['default.topic.config'] = \
            json.loads(self.props.get('default.topic.config', ''))
        return self.props
