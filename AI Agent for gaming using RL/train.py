#!/usr/bin/env python3
"""
Minimal PPO implementation (PyTorch) for OpenAI Gym (CartPole example)
WITH visualization utilities added.
"""

import argparse
try:
    import gymnasium as gym
except Exception:
    import gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
import time
import os
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _unpack_reset(reset_out):
    if isinstance(reset_out, (tuple, list)):
        return reset_out[0]
    return reset_out


def _step_env(env, action):
    out = env.step(action)
    if len(out) == 5:
        obs, r, term, trunc, info = out
        return obs, r, term or trunc, info
    return out


class ActorCritic(nn.Module):
    def __init__(self, obs_dim, action_dim, hidden_size=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU()
        )
        self.policy = nn.Linear(hidden_size, action_dim)
        self.value = nn.Linear(hidden_size, 1)

    def forward(self, x):
        x = self.net(x)
        return self.policy(x), self.value(x).squeeze(-1)


class PPO:
    def __init__(self, obs_dim, action_dim, lr=3e-4,
                 clip_epsilon=0.2, value_coef=0.5, ent_coef=0.01):
        self.model = ActorCritic(obs_dim, action_dim).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.clip_epsilon = clip_epsilon
        self.value_coef = value_coef
        self.ent_coef = ent_coef

    def select_action(self, obs):
        obs = np.asarray(obs, dtype=np.float32)
        obs_t = torch.tensor(obs).unsqueeze(0).to(device)
        logits, value = self.model(obs_t)
        dist = Categorical(logits=logits)
        action = dist.sample()
        return (
            int(action.item()),
            dist.log_prob(action).item(),
            value.item(),
            dist.entropy().item()
        )

    def evaluate_actions(self, obs, actions):
        logits, values = self.model(obs)
        dist = Categorical(logits=logits)
        return dist.log_prob(actions), dist.entropy(), values

    def update(self, batch, epochs=4, minibatch_size=64):
        obs = torch.tensor(batch['obs'], device=device)
        actions = torch.tensor(batch['actions'], device=device)
        old_logp = torch.tensor(batch['log_probs'], device=device)
        returns = torch.tensor(batch['returns'], device=device)
        adv = torch.tensor(batch['advantages'], device=device)

        adv = (adv - adv.mean()) / (adv.std() + 1e-8)

        N = obs.size(0)
        for _ in range(epochs):
            perm = torch.randperm(N)
            for i in range(0, N, minibatch_size):
                idx = perm[i:i+minibatch_size]

                logp, ent, values = self.evaluate_actions(
                    obs[idx], actions[idx]
                )

                ratio = (logp - old_logp[idx]).exp()
                surr1 = ratio * adv[idx]
                surr2 = torch.clamp(
                    ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon
                ) * adv[idx]

                policy_loss = -torch.min(surr1, surr2).mean()
                value_loss = (returns[idx] - values).pow(2).mean()
                loss = policy_loss + self.value_coef * value_loss - self.ent_coef * ent.mean()

                clip_frac = ((ratio > 1 + self.clip_epsilon) |
                             (ratio < 1 - self.clip_epsilon)).float().mean()

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), 0.5)
                self.optimizer.step()

        print(f"PPO update | adv μ={adv.mean():.3f} σ={adv.std():.3f} | clip_frac={clip_frac:.2f}")


def compute_gae(next_value, rewards, masks, values, gamma=0.99, lam=0.95):
    values = np.append(values, next_value)
    gae = 0
    returns = np.zeros_like(rewards)
    for t in reversed(range(len(rewards))):
        delta = rewards[t] + gamma * values[t+1] * masks[t] - values[t]
        gae = delta + gamma * lam * masks[t] * gae
        returns[t] = gae + values[t]
    return returns, returns - values[:-1]


def collect_trajectories(env, agent, batch_size):
    obs, rewards, values, logp, actions, masks = [], [], [], [], [], []
    state = _unpack_reset(env.reset())
    steps = 0

    while steps < batch_size:
        a, lp, v, _ = agent.select_action(state)
        next_state, r, done, _ = _step_env(env, a)

        obs.append(state)
        rewards.append(r)
        values.append(v)
        logp.append(lp)
        actions.append(a)
        masks.append(0.0 if done else 1.0)

        state = next_state
        steps += 1
        if done:
            state = _unpack_reset(env.reset())

    with torch.no_grad():
        _, next_v = agent.model(
            torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
        )

    returns, adv = compute_gae(
        next_v.item(),
        np.array(rewards),
        np.array(masks),
        np.array(values)
    )

    return dict(
        obs=np.array(obs, dtype=np.float32),
        actions=np.array(actions),
        log_probs=np.array(logp),
        returns=returns,
        advantages=adv
    )


def evaluate(env, agent, render=False):
    obs = _unpack_reset(env.reset())
    done, total = False, 0
    while not done:
        a, _, _, _ = agent.select_action(obs)
        obs, r, done, _ = _step_env(env, a)
        total += r
        if render:
            env.render()
    return total


def visualize_value(agent):
    angles = np.linspace(-0.2, 0.2, 100)
    values = []
    for a in angles:
        obs = torch.tensor([0, 0, a, 0]).float().unsqueeze(0).to(device)
        with torch.no_grad():
            _, v = agent.model(obs)
        values.append(v.item())
    plt.plot(angles, values)
    plt.xlabel("Pole Angle")
    plt.ylabel("V(s)")
    plt.title("Critic Value Function")
    plt.show()


def visualize_policy(agent):
    print("\nPolicy probabilities:")
    for a in [-0.1, 0.0, 0.1]:
        obs = torch.tensor([0, 0, a, 0]).float().unsqueeze(0).to(device)
        with torch.no_grad():
            logits, _ = agent.model(obs)
            probs = torch.softmax(logits, dim=-1)
        print(f"angle={a:+.2f} → left={probs[0,0]:.2f}, right={probs[0,1]:.2f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', default='CartPole-v1')
    parser.add_argument('--total-timesteps', type=int, default=200000)
    parser.add_argument('--batch-size', type=int, default=2048)
    parser.add_argument('--evaluate', action='store_true')
    args = parser.parse_args()

    env = gym.make(args.env, render_mode="human" if args.evaluate else None)
    agent = PPO(env.observation_space.shape[0], env.action_space.n)

    eval_rewards = []
    steps = 0

    while steps < args.total_timesteps:
        batch = collect_trajectories(env, agent, args.batch_size)
        agent.update(batch)
        steps += args.batch_size

        r = evaluate(env, agent)
        eval_rewards.append((steps, r))
        print(f"[{steps}] Eval return: {r}")

    steps_, rewards_ = zip(*eval_rewards)
    plt.plot(steps_, rewards_)
    plt.xlabel("Timesteps")
    plt.ylabel("Return")
    plt.title("Learning Curve")
    plt.show()

    visualize_value(agent)
    visualize_policy(agent)


if __name__ == "__main__":
    main()
