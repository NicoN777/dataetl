from conf.builder import get_configuration
from message.kafkie import Kafka

if __name__ == '__main__':
   # kafka_consumer = Kafka(get('kafka', 'ORDERS'))
   # kafka_consumer.consume()
   kafka_producer = Kafka(get_configuration('kafka', 'ORDERS').properties)
   test_data = """{"id":1,
  "customerName":"Nicolas Nunez",
  "shippingAddress":"3600 Bristol Motor Pass",
  "products":[
    {"id":19092,
      "brand":"Mossy Oak",
      "name":"Mini Pocket Knife",
      "description":"Useful Knife for everyday activities",
      "price":12.9,
      "reviews":[
        {"id":1,
          "title":"Best in the West",
          "body":"Bought this little f***r the other day, no ragrets!",
          "date":1581535506251,
          "likes":10,
          "useful":5},
        {"id":2,
          "title":"Looks are not just it",
          "body":"Aside from looking amazing, this knife can really cut",
          "date":1581535506251,"likes":3,"useful":10}]},
    {"id":1840,
      "brand":"Apple",
      "name":"AirPods",
      "description":"Wireless Earbuds",
      "price":150.8,
      "reviews": [
        {"id":3,
          "title":"Convenient",
          "body":"Easy to carry, sound quality is good.",
          "date":1581535506251,
          "likes":2,
          "useful":40},
        {"id":4,
          "title":"I'm the boss",
          "body":"I can pretend I'm in a meeting whenever someone talks to me and I don't want to respond or socialize!",
          "date":1581535506251,
          "likes":100,
          "useful":99}
      ]
    }
  ],
  "total":163.7,
  "date":1581535506251
}"""

   import json
   test_data = test_data.replace('\n', '')
   json_payload = json.dumps(test_data)
   # js = json.loads(test_data)
   # key = js['id']
   # value = js
   # key = json_payload['id']
   value = json_payload
   kafka_producer.produce(key=None, value=value)