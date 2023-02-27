import gym
import os
import mujoco_py
from agent import Agent
from train import Train
from play import Play
import requests # added 22.05.26

#ENV_NAME = "Ant"
ENV_NAME = "Laikago"
#ENV_NAME = "Walker2d"
#ENV_NAME = "Humanoid"

TRAIN_FLAG = False
#TRAIN_FLAG = True
test_env = gym.make(ENV_NAME + "-v2")

n_states = test_env.observation_space.shape[0]
action_bounds = [test_env.action_space.low[0], test_env.action_space.high[0]]
n_actions = test_env.action_space.shape[0]

n_iterations = 10000 #500
lr = 3e-5 #3e-4
epochs = 10
clip_range = 0.1 # 0.2
mini_batch_size = 256 # 64
T = 2048

if __name__ == "__main__":
    print(f"number of states:{n_states}\n"
          f"action bounds:{action_bounds}\n"
          f"number of actions:{n_actions}")

    #if not os.path.exists(ENV_NAME): #erased 22.04.30(for not to generate file)
        #os.mkdir(ENV_NAME)
        #os.mkdir(ENV_NAME + "/logs")

    env = gym.make(ENV_NAME + "-v2")

    agent = Agent(n_states=n_states,
                  n_iter=n_iterations,
                  env_name=ENV_NAME,
                  action_bounds=action_bounds,
                  n_actions=n_actions,
                  lr=lr)
    if TRAIN_FLAG:
        trainer = Train(env=env,
                        test_env=test_env,
                        env_name=ENV_NAME,
                        agent=agent,
                        horizon=T,
                        n_iterations=n_iterations,
                        epochs=epochs,
                        mini_batch_size=mini_batch_size,
                        epsilon=clip_range)
        trainer.step()

    player = Play(env, agent, ENV_NAME)
    player.evaluate()

"""
def main5(): # added 22.05.26
    send_line_notify('Successfully conducted!')

def send_line_notify(notification_message): # added 22.05.26
    #LINEに通知する
    line_notify_token = '4VfnrNL6S3GOX9R8JYn1wPCNyzzfQxkbzR1UtpKvuNl'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

if __name__ == "__main__":
    main5()
"""
