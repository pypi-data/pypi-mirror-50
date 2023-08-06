from abc import ABC, abstractmethod

from cogment.api.environment_pb2_grpc import EnvironmentServicer as Servicer
from cogment.api.environment_pb2 import EnvStartRequest, EnvStartReply, EnvUpdateReply
from cogment.api.common_pb2 import Feedback, ObservationData
from cogment.utils import list_versions

from types import SimpleNamespace, ModuleType
from typing import Any, Dict


class Actor:
    def __init__(self, actor_class, actor_id):
        self.actor_class = actor_class
        self.actor_id = actor_id
        self._feedback = []

    def send_feedback(self, time, value, confidence, user_data=None):
        self._feedback.append((time, value, confidence, user_data))


class Trial:
    def __init__(self, id, settings):
        self.id = id
        self.actors = SimpleNamespace(all=[])
        self.settings = settings

        actor_id = 0
        for actor_class, count in self.settings.environment.actors:
            actor_list = []
            for i in range(count):
                actor = Actor(actor_class, actor_id)
                actor_list.append(actor)
                self.actors.all.append(actor)
                actor_id += 1

            setattr(self.actors, actor_class.name, actor_list)


def create_action_data(settings):
    actions_by_actor_id = []
    actions_by_actor_class = SimpleNamespace()

    for actor_class, count in settings.environment.actors:
        actions_list = [actor_class.action_space() for _ in range(count)]

        actions_by_actor_id.extend(actions_list)
        setattr(actions_by_actor_class, actor_class.name, actions_list)

    return actions_by_actor_class, actions_by_actor_id


class Environment(ABC):
    VERSIONS: Dict[str, str]

    def __init__(self, trial: Trial):
        self.trial = trial

    def start(self, config):
        return self.trial.settings.environment.default_observation()

    @abstractmethod
    def update(self, actions):
        pass


class EnvService(Servicer):
    def __init__(self, env_class, settings):
        assert issubclass(env_class, Environment)

        # We will be managing a pool of environments, keyed by their trial id.
        self._envs: Dict[str, Trial] = {}
        self._env_config_type = settings.environment.config
        self._env_class = env_class
        self.settings: ModuleType = settings

        actions_by_actor_class, actions_by_actor_id = create_action_data(self.settings)

        self.actions_by_actor_class = actions_by_actor_class
        self.actions_by_actor_id = actions_by_actor_id
        self.tick_id = 0

        print("Environment service started")

    # The orchestrator is requesting a new environment
    def Start(self, request, context):
        try:
            trial_id = request.trial_id
            if not trial_id:
                raise Exception("You must send a trial_id")
            if trial_id in self._envs:
                raise Exception("trial already exists")

            print(f"spinning up new environment: {trial_id}")

            # Instantiate the fresh environment
            trial = Trial(trial_id, self.settings)

            config = None
            if request.HasField("config"):
                if self._env_config_type is None:
                    raise Exception("This environment isn't expecting a config")

                config = self._env_config_type()
                config.ParseFromString(request.config.content)

            instance = self._env_class(trial)
            initial_observation = instance.start(config)

            self._envs[trial.id] = (instance, trial)

            # Send the initial state of the environment back to the client
            # (orchestrator, normally.)
            reply = EnvStartReply()
            reply.observation_set.tick_id = 0
            reply.observation_set.timestamp.GetCurrentTime()

            reply.observation_set.observations.append(ObservationData(
                content=initial_observation.SerializeToString(),
                snapshot=True
            ))

            reply.observation_set.actors_map.extend([0] * len(trial.actors.all))

            return reply
        except Exception as e:
            print(f'Start failure: {e}')
            raise

    # The orchestrator is ready for the environemnt to move forward in time.
    def Update(self, request, context):
        try:
            try:
                instance, trial = self._envs[request.trial_id]
            except KeyError as err:
                raise Exception("trial does not exists")

            len_actions = len(request.action_set.actions)
            len_actors = len(self.actions_by_actor_id)
            if len_actions != len_actors:
                raise Exception(f"Received {len_actions} actions but have {len_actors} actors")

            for i, action in enumerate(self.actions_by_actor_id):
                action.ParseFromString(request.action_set.actions[i])

            # Advance time
            delta = instance.update(self.actions_by_actor_class)

            # TODO: handle request.reply_with_snapshot

            # Send the delta back to the orchestrator.
            reply = EnvUpdateReply()
            self.tick_id += 1
            reply.observation_set.tick_id = self.tick_id
            reply.observation_set.timestamp.GetCurrentTime()

            reply.observation_set.observations.append(ObservationData(
                content=delta.SerializeToString(),
                snapshot=False
            ))

            reply.observation_set.actors_map.extend([0] * len(trial.actors.all))

            for actor in trial.actors.all:
                for fb in actor._feedback:
                    re = Feedback(
                        actor_id=actor.actor_id,
                        tick_id=fb[0],
                        value=fb[1],
                        confidence=fb[2]
                    )
                    if fb[3] is not None:
                        re.content = fb[3].SerializeToString()

                    reply.feedbacks.append(re)

                actor._feedback = []

            return reply
        except Exception as e:
            print(f'Update failure: {e}')
            raise

    def Version(self, request, context):
        try:
            return list_versions(self._env_class)
        except Exception as e:
            print(f'Version failure: {e}')
            raise
