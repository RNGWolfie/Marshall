# Marshall

Marshall is a Rocket League bot built with RLBot.

The project focuses on building an autonomous Rocket League agent using
behavior-based decision making, specialized controllers, and eventually
reinforcement learning.

## Current Features

- Ball tracking
- Ground navigation
- Wall ball tracking
- Goal-oriented positioning
- Boost management
- Basic steering and throttle control
- Opponent goal detection

## Architecture

Marshall is organized into several systems:

- `behaviors/` — High-level decisions
- `controllers/` — Low-level control
- `maneuvers/` — Discrete actions
- `utility/` — Game information and shared utilities
- `src/` — RLBot configuration
- `bot.py` — Main bot entry point

## Roadmap

- [ ] Behavior/utility decision system
- [ ] Improved shooting
- [ ] Defensive behavior
- [ ] Wall play
- [ ] Ball prediction
- [ ] Aerial play
- [ ] Recovery system
- [ ] Reinforcement learning
- [ ] PPO training
- [ ] 3D perception

## Requirements

- Python
- RLBot
- Rocket League

## Status

Marshall is actively under development.