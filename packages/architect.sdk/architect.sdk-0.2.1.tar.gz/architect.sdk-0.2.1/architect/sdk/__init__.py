# -*- coding: utf-8 -*-

import glob
import importlib
import json
import os
import sys
import urllib.parse

try:
    import requests

    class ArchitectSession(requests.Session):

        def __init__(self, base_url=None):
            self.base_url = base_url
            super().__init__()

        def request(self, method, url, *args, **kwargs):
            """Send the request after generating the complete URL."""
            if self.base_url:
                url = urllib.parse.urljoin(self.base_url, url)
            return super().request(method, url, *args, **kwargs)

except ImportError:
    requests = None

try:
    import grpc
except ImportError:
    grpc = None


try:
    ARCHITECT = json.loads(os.environ['ARCHITECT'])
except KeyError:
    ARCHITECT = {}


_services = {}
_datastores = {}


class ArchitectService:
    def __init__(self, service_name, config):
        self.service_folder = service_name.replace('-', '_')
        self.service_module = service_name.replace('-', '_').replace('/', '.')
        self.config = config
        self._client = None
        self._defs = None
        self._grpc_pb = None

    def _namespace_import(self, match):
        module_regex = '*_{}.py'.format(match)
        modules = glob.glob(os.path.join(os.getcwd(), 'architect_services', self.service_folder, module_regex))
        grpc_module = modules[0].split(os.sep)[-1].replace('.py', '')
        namespace = self.service_module.split('.')[0]
        m = sys.modules.pop(namespace, None)
        sys.path.insert(0, os.path.join(os.getcwd(), 'architect_services'))
        module = importlib.import_module('{}.{}'.format(self.service_module, grpc_module))
        sys.path = sys.path[1:]
        if m:
            sys.modules[namespace] = m
        return module

    @property
    def grpc_pb(self):
        if self._grpc_pb is None:
            self._grpc_pb = self._namespace_import('pb2_grpc')
        return self._grpc_pb

    @property
    def defs(self):
        if self._defs is None:
            self._defs = self._namespace_import('pb2')
        return self._defs

    @property
    def client(self):
        if self._client is None:
            if self.config['api'] == 'rest':
                if requests is None:
                    raise Exception('Include requests in your requirements.txt')
                self._client = ArchitectSession('{}:{}'.format(self.config['host'], self.config['port']))
            elif self.config['api'] == 'grpc':
                if grpc is None:
                    raise Exception('Include grpcio in your requirements.txt')
                channel = grpc.insecure_channel('{}:{}'.format(self.config['host'], self.config['port']))
                self._client = self.grpc_pb.ArchitectStub(channel)
            else:
                raise NotImplementedError('Unsupported api type {}'.format(self.config['api']))
        return self._client


class Notifier:
    def __init__(self, notification):
        self.notification = notification

    def subscriptions(self):
        subscribers = []
        for subscriber_name, subscriber_config in self.notification.items():
            subscribers.append({
                'name': subscriber_name,
                **subscriber_config,
                **service(subscriber_name).config
            })
        return subscribers


def service(service_name):
    service = _services.get(service_name)
    if service is None:
        try:
            config = ARCHITECT[service_name]
        except KeyError:
            raise Exception('Service {} is required but has not been started'.format(service_name))
        _services[service_name] = service = ArchitectService(service_name, config)

    return service


def datastore(datastore_name):
    datastore = _datastores.get(datastore_name)
    if datastore is None:
        datastores = current_service().config.get('datastores', {})
        try:
            datastore = datastores[datastore_name]
        except KeyError:
            raise Exception('Datastore {} is required but has not been started'.format(datastore_name))
        _datastores[datastore_name] = datastore
    return datastore


def notification(event_name):
    subscriptions = current_service().config.get('subscriptions', {})
    try:
        notification = subscriptions[event_name]
    except KeyError:
        raise Exception('{} event not found on service'.format(event_name))
    return Notifier(notification)


def current_service():
    current_service = service(os.environ['ARCHITECT_CURRENT_SERVICE'])
    if current_service.config['api'] == 'grpc':
        current_service.Servicer = current_service.grpc_pb.ArchitectServicer
        current_service.add_servicer = current_service.grpc_pb.add_ArchitectServicer_to_server
    return current_service
