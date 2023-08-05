# coding: utf-8
import pika
import json
import logging
import threading
from datetime import datetime, date
from bson import ObjectId
from pika.exceptions import AMQPConnectionError

logger = logging.getLogger(__name__)


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'keys') and hasattr(obj, '__getitem__'):
            return dict(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(obj, date):
            # return obj.strftime('%Y-%m-%d')
            return obj.strftime('%Y-%m-%dT%H:%M:%S')  # mongodb的date类型为python的datetime类型
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def sub_run(subscribes, host='localhost'):
    """
    开始侦听消息
    :param host:
    :param extable:
    :return:
    """
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))

        channel = connection.channel()

        for exchange, callback in subscribes:
            channel.exchange_declare(exchange=exchange, exchange_type='fanout')
            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            channel.queue_bind(exchange=exchange, queue=queue_name)

            channel.basic_consume(queue=queue_name,
                                  on_message_callback=callback,
                                  auto_ack=True)

        logger.info(u'[INFO]:正在等待消息...')
        # channel.start_consuming()
        t = threading.Thread(target=channel.start_consuming)
        t.start()
        return t
    except AMQPConnectionError as err:
        logger.error(repr(err))


def register_queue(queue, host='localhost'):
    return sub_run(queue.callbacks, host)


def emit(exchange="", body=None, host="localhost"):
    if body is None:
        raise ValueError("信息内容不能为空")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()

    # 定义交换机并设定为"扇出"类型
    channel.exchange_declare(exchange=exchange,
                             exchange_type='fanout')
    # 定义默认的队列，使用随机列表
    result = channel.queue_declare(queue='', exclusive=True)

    queue_name = result.method.queue
    # 将信息发送到交换机
    channel.basic_publish(exchange=exchange,
                          routing_key=queue_name,
                          body=json.dumps(body, cls=CJsonEncoder))

    connection.close()


class Queue():
    callbacks = []

    def __call__(self, exchange=''):
        """
        当Queue对象被调用时，如@queue()执行的操作
        :param exchange_name:
        :return:
        """

        def _(func):
            self.callbacks.append((exchange, func))

        return _
