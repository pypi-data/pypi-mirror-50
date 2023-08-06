class ActorClass:
    def __init__(self, name, action_space, observation_space,
                 observation_delta, observation_delta_apply_fn, reward_space):
        self.name = name
        self.action_space = action_space
        self.observation_space = observation_space
        self.observation_delta = observation_delta
        self.observation_delta_apply_fn = observation_delta_apply_fn
        self.reward_space = reward_space
