from model import Actor, Critic
from torch.optim import Adam
from torch import from_numpy
import numpy as np
import torch
from torch.optim.lr_scheduler import LambdaLR


class Agent:
    def __init__(self, env_name, n_iter, n_states, action_bounds, n_actions, lr):
        self.env_name = env_name
        self.n_iter = n_iter
        self.action_bounds = action_bounds
        self.n_actions = n_actions
        self.n_states = n_states
        self.device = torch.device("cpu")
        self.lr = lr

        self.current_policy = Actor(n_states=self.n_states,
                                    n_actions=self.n_actions).to(self.device)
        self.critic = Critic(n_states=self.n_states).to(self.device)

        self.actor_optimizer = Adam(self.current_policy.parameters(), lr=self.lr, eps=1e-5)
        self.critic_optimizer = Adam(self.critic.parameters(), lr=self.lr, eps=1e-5)

        self.critic_loss = torch.nn.MSELoss()

        self.scheduler = lambda step: max(1.0 - float(step / self.n_iter), 0)

        self.actor_scheduler = LambdaLR(self.actor_optimizer, lr_lambda=self.scheduler)
        self.critic_scheduler = LambdaLR(self.actor_optimizer, lr_lambda=self.scheduler)

    def choose_dist(self, state):
        state = np.expand_dims(state, 0)
        state = from_numpy(state).float().to(self.device)
        with torch.no_grad():
            dist = self.current_policy(state)

        # action *= self.action_bounds[1]
        # action = np.clip(action, self.action_bounds[0], self.action_bounds[1])

        return dist

    def get_value(self, state):
        state = np.expand_dims(state, 0)
        state = from_numpy(state).float().to(self.device)
        with torch.no_grad():
            value = self.critic(state)

        return value.detach().cpu().numpy()

    def optimize(self, actor_loss, critic_loss):
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        # torch.nn.utils.clip_grad_norm_(self.current_policy.parameters(), 0.5)
        # torch.nn.utils.clip_grad_norm_(self.critic.parameters(), 0.5)
        self.actor_optimizer.step()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        # torch.nn.utils.clip_grad_norm_(self.current_policy.parameters(), 0.5)
        # torch.nn.utils.clip_grad_norm_(self.critic.parameters(), 0.5)
        self.critic_optimizer.step()

    def schedule_lr(self):
        # self.total_scheduler.step()
        self.actor_scheduler.step()
        self.critic_scheduler.step()

    def save_weights(self, iteration, state_rms):
        torch.save({"current_policy_state_dict": self.current_policy.state_dict(),
                    "critic_state_dict": self.critic.state_dict(),
                    "actor_optimizer_state_dict": self.actor_optimizer.state_dict(),
                    "critic_optimizer_state_dict": self.critic_optimizer.state_dict(),
                    "actor_scheduler_state_dict": self.actor_scheduler.state_dict(),
                    "critic_scheduler_state_dict": self.critic_scheduler.state_dict(),
                    "iteration": iteration,
                    "state_rms_mean": state_rms.mean,
                    "state_rms_var": state_rms.var,
                    "state_rms_count": state_rms.count}, "./Pth/" + self.env_name + "_weights.pth") #modified 22.04.30

    def load_weights(self):
        #checkpoint = torch.load(self.env_name + "_weights.pth") #modified 22.04.30
        #checkpoint = torch.load("./Pth/pre-trained models/"+self.env_name + "_weights.pth") # modified 22.04.30
        #checkpoint = torch.load("./Pth/" + "Ant" + "_weightsNON_10000.pth") #modified 22.04.30
        #checkpoint = torch.load("./Pth/" + "Laikago23000" + "_weights.pth") #modified 22.04.30
        
        #checkpoint = torch.load("../Continuous-PPO-master/CheckPoint2" +"/"+self.env_name+"_CP10.31.18.49.8"+"/"+self.env_name+"15000_weights.pth") 
        checkpoint = torch.load("../Continuous-PPO-master/CheckPoint2" +"/"+self.env_name+"_CP11.1.2.15.47"+"/"+self.env_name+"200000_weights.pth") # jo=40 clean
        #checkpoint = torch.load("../Continuous-PPO-master/CheckPoint2" +"/"+self.env_name+"_CP11.4.11.37.5"+"/"+self.env_name+"10000_weights.pth") # jo=30 unclean form
        #checkpoint = torch.load("../Continuous-PPO-master/CheckPoint2" +"/"+self.env_name+"_CP11.6.13.33.46"+"/"+self.env_name+"60000_weights.pth") # jo=35 unclean
        #checkpoint = torch.load("../Continuous-PPO-master/CheckPoint2" +"/"+self.env_name+"_CP11.8.0.17.32"+"/"+self.env_name+"150000_weights.pth") # jo=40
        #checkpoint = torch.load("../Continuous-PPO-master/CheckPoint2" +"/"+self.env_name+"_CP11.9.23.59.20"+"/"+self.env_name+"30000_weights.pth") # jo=
        #checkpoint = torch.load("../Continuous-PPO-master/CheckPoint2" +"/"+self.env_name+"_CP11.19.14.5.51"+"/"+self.env_name+"40000_weights.pth") # 
        #checkpoint = torch.load("../Continuous-PPO-master/CheckPoint2" +"/"+self.env_name+"_CP11.20.3.24.35"+"/"+self.env_name+"20000_weights.pth") # 
        
        self.current_policy.load_state_dict(checkpoint["current_policy_state_dict"])
        self.critic.load_state_dict(checkpoint["critic_state_dict"])
        self.actor_optimizer.load_state_dict(checkpoint["actor_optimizer_state_dict"])
        self.critic_optimizer.load_state_dict(checkpoint["critic_optimizer_state_dict"])
        self.actor_scheduler.load_state_dict(checkpoint["actor_scheduler_state_dict"])
        self.critic_scheduler.load_state_dict(checkpoint["critic_scheduler_state_dict"])
        iteration = checkpoint["iteration"]
        state_rms_mean = checkpoint["state_rms_mean"]
        state_rms_var = checkpoint["state_rms_var"]

        return iteration, state_rms_mean, state_rms_var

    def set_to_eval_mode(self):
        self.current_policy.eval()
        self.critic.eval()

    def set_to_train_mode(self):
        self.current_policy.train()
        self.critic.train()
