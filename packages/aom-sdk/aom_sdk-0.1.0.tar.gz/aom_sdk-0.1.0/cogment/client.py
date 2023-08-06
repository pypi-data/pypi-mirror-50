from cogment.api.orchestrator_pb2 import (
    TrialStartRequest, TrialActionRequest, TrialEndRequest
)
from cogment.api.orchestrator_pb2_grpc import TrialStub
from cogment.api.common_pb2 import Action

from cogment.delta_encoding import DecodeObservationData

import grpc


class Session:
    def __init__(self, conn, trial_id, actor_id, actor_class,
                 initial_observation):
        self.connection = conn
        self.observation = initial_observation
        self.trial_id = trial_id
        self.actor_id = actor_id
        self.actor_class = actor_class

    def DoAction(self, action):
        assert isinstance(action, self.actor_class.action_space)

        # Send the update to the orchestrator
        update = self.connection.stub.Action(TrialActionRequest(
            trial_id=self.trial_id,
            actor_id=self.actor_id,
            action=Action(content=action.SerializeToString())))

        self.observation = DecodeObservationData(
            self.actor_class,
            update.observation.data,
            self.observation)

        # Return the latest observation
        return self.observation

    # Kill the trial
    def End(self):
        self.connection.stub.End(TrialEndRequest(trial_id=self.trial_id))


class _Connection_impl:
    def __init__(self, stub, settings):
        if not settings:
            raise Exception("missing settings")

        if not stub:
            raise Exception("missing grpc connection stub")

        self.stub = stub
        self.settings = settings

    def Start(self, actor_class, env_cfg=None):
        req = TrialStartRequest()

        if env_cfg:
            req.config.content = env_cfg.SerializeToString()

        rep = self.stub.Start(req)

        observation = DecodeObservationData(
            actor_class, rep.observation.data)

        return Session(
            self, rep.trial_id, rep.actor_id, actor_class, observation)


class Connection(_Connection_impl):
    def __init__(self, settings, endpoint=None, stub=None):
        channel = grpc.insecure_channel(endpoint)
        stub = TrialStub(channel)
        super().__init__(stub)
