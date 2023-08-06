# Copyright 2019 Age of Minds inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import grpc
import time
from distutils.util import strtobool
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from grpc_reflection.v1alpha import reflection

from cogment.actor_class import ActorClass
from cogment.version import __version__

from cogment.api.environment_pb2_grpc import add_EnvironmentServicer_to_server
from cogment.api.agent_pb2_grpc import add_AgentServicer_to_server


from cogment.delta_encoding import _apply_delta_replace


ENABLE_REFLECTION_VAR_NAME = 'AOM_GRPC_REFLECTION'
DEFAULT_PORT = 9000
MAX_WORKERS = 10


# General aom_framework error
class Error(Exception):
    pass


# Error that occured while configuring the aom_framework
class ConfigError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class DataTypes:
    def __init__(self, *args, **kwargs):
        self.env_state = kwargs.get('env_state', None)
        self.human_action = kwargs.get('human_action', None)
        self.agent_action = kwargs.get('agent_action', None)
        self.env_config = kwargs.get('env_config', None)
        self.env_state_delta = kwargs.get('env_state_delta', None)
        self.state_collapse_fn = kwargs.get('state_collapse_fn', None)


# A Grpc endpoint serving an aom service
class GrpcServer:

    def __init__(self, service_type, data_types, port=DEFAULT_PORT):
        from cogment.agent_service import AgentService
        from cogment.env_service import EnvService
        from cogment.utils import list_versions

        print("Versions:")
        for v in list_versions(service_type).versions:
            print(f'  {v.name}: {v.version}')

        self._port = port
        self._grpc_server = grpc.server(ThreadPoolExecutor(max_workers=MAX_WORKERS))

        # Register service
        if issubclass(service_type, Agent):
            self._service_type = _services_pbs._AGENT
            add_AgentServicer_to_server(AgentService(service_type, data_types), self._grpc_server)
        elif issubclass(service_type, Environment):
            self._service_type = _services_pbs._ENVIRONMENT
            add_EnvironmentServicer_to_server(EnvService(service_type, data_types), self._grpc_server)
        else:
            raise ConfigError('Invalid service type')

        # Enable grpc reflection if requested
        if strtobool(os.getenv(ENABLE_REFLECTION_VAR_NAME, 'false')):
            SERVICE_NAMES = (
                self._service_type.full_name,
                reflection.SERVICE_NAME,
            )
            reflection.enable_server_reflection(SERVICE_NAMES, self._grpc_server)

        self._grpc_server.add_insecure_port(f'[::]:{port}')

    def serve(self):
        self._grpc_server.start()
        print(f"{self._service_type.full_name} service listening on port {self._port}")
        try:
            while True:
                time.sleep(24*60*60)
        except KeyboardInterrupt:
            self._grpc_server.stop(0)
