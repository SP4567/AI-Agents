```markdown
# PPO CartPole Starter

Minimal PPO implementation (PyTorch) for OpenAI Gym CartPole-v1.

Usage:
1. Create and activate a virtualenv (recommended).
2. Install requirements:
   pip install -r requirements.txt

3. Train:
   python train.py --env CartPole-v1 --seed 0 --total-timesteps 200000

4. Evaluate:
   python train.py --env CartPole-v1 --seed 0 --evaluate --model-path ppo_cartpole.pth

Notes:
- To target another Gym environment, change `--env` to any Gym env name. For continuous action spaces you will need to adapt the action distribution (use Gaussian instead of Categorical).
- Hyperparameters are conservative; for more complex games increase batch sizes, use vectorized environments, and consider GPU usage.
```