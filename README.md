#  Queen Duel AI 

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Tournament Rank](https://img.shields.io/badge/Tournament%20Rank-3rd%20Place%20/%2050-gold.svg)](#-tournament-results)
[![Win Rate](https://img.shields.io/badge/Tournament%20Win%20Rate-97.96%25%20(96%2F98)-brightgreen.svg)](#-tournament-results)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An adversarial game-playing AI agent engineered for **Queen Duel** (a competitive $7 \times 7$ Isolation game variant featuring chess-queen movement and directional push mechanics). 

In a course-wide double round-robin tournament against 49 peer agents (98 total matches, alternating player order P1/P2), this agent finished **3rd Place overall with a 96–2 record (97.96% win rate)**.


##  Tournament Results

The competition evaluated each agent head-to-head in a double round-robin format against 49 competitors:

| Metric | Result | Details |
| :--- | :---: | :--- |
| **Final Standing** | **3rd Place** | Out of 50 participating student agents |
| **Total Games** | **98** | 49 games as Player 1 + 49 games as Player 2 |
| **Wins** | **96** | 97.96% tournament win rate |
| **Losses** | **2** | 2.04% loss rate |
| **Baseline Matches** | **99% / 100%** | Measured against randomized and heuristic baselines |


##  Game Mechanics

The game is played on a $7 \times 7$ grid between two queens:
* **Movement:** Moves like a chess Queen across unblocked straight or diagonal paths.
* **Square Contraction:** Every cell vacated by a queen becomes permanently **blocked**.
* **Push Action:** Landing on a tile occupied by the opponent queen pushes them 1 cell in the attack direction.
* **Loss Conditions:** A player loses if pushed out of bounds or if no legal moves remain on their turn.


##  Architecture & Strategic Design

                               +-------------------------------+
                               |      CustomPlayer.move()      |
                               +---------------+---------------+
                                               |
                      +------------------------+------------------------+
                      |                                                 |
              [Symmetric Opening Anchors]                     [Dynamic Search Depth]
              - (1,1), (1,5), (5,1), (5,5)                    - Move < 10  -> Depth 2
                                                            - Move 10-20 -> Depth 4
                                                            - Move 20-30 -> Depth 6
                                                            - Move > 30  -> Depth 8+
                                                                        |
                                                     +------------------+------------------+
                                                     |        in_margin_and_push()         |
                                                     | (Pre-Search Danger Move Filter)     |
                                                     +------------------+------------------+
                                                                        |
                                                     +------------------+------------------+
                                                     |     Alpha-Beta Pruning Search       |
                                                     +------------------+------------------+
                                                                        |
                                               +------------------------+------------------------+
                                               |                                                 |
                                 [Move Flexibility Ordering]                              [CustomEvalFn]
                                 - Forecast-based branch ranking                          - Mobility differential
                                                                                          - Center-square bonus
                                                                                          - Immediate push bonus



### 1. Symmetric Opening Randomization
To eliminate first-move determinism and bypass hardcoded opening traps, the agent randomly picks from four diagonal anchor points on turn one: `(1,1)`, `(1,5)`, `(5,1)`, and `(5,5)`.

### 2. Pre-Search Margin Filtering (`in_margin_and_push`)
Filters out high-risk candidate moves prior to tree exploration:
* Identifies boundary tiles overlapping with the opponent's direct line of sight.
* Prevents suicidal moves onto edge cells where an opponent push would immediately eject the queen from the board.

### 3. Dynamic Phase-Based Search Depth
Search depth dynamically adapts to game progression, maximizing tactical vision when the branching factor drops:
* **Turns $0\text{--}9$:** Depth 2 (rapid opening setup, preserving time budget).
* **Turns $10\text{--}19$:** Depth 4 (territory consolidation).
* **Turns $20\text{--}29$:** Depth 6 (board constriction).
* **Turns $30+$:** Depth 8+ (exhaustive endgame resolution).

### 4. Heuristic Utility Function (`CustomEvalFn`)
Evaluates game states across mobility, positioning, and tactical threat:

$$\text{Utility}(s) = \Big(|\mathcal{M}_{\text{player}}| - |\mathcal{M}_{\text{opponent}}|\Big) + \text{Bonus}_{\text{center}} + \text{Bonus}_{\text{push}}$$

* **Mobility Differential:** Maximizes personal move options while strangling opponent branches.
* **Center Dominance:** $+10$ strategic score for holding center tiles `(3,3)`, `(3,4)`, `(4,3)`, `(4,4)`.
* **Push Bonus:** $+15$ incentive for achieving offensive displacement threats.


##  Repository Structure

```plaintext
.
├── player_submission.py        # CustomPlayer, CustomEvalFn, and Alpha-Beta logic
├── game.py                     # Board representation and game engine
├── test_players.py             # RandomPlayer and HumanPlayer baseline classes
├── player_submission_tests.py  # Local battle simulator and testing suite
└── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules for Python builds
└── requirements.txt                   

```

## Getting Started

### Prerequisites
* Python 3.8 or higher

### Installation

```bash
# Clone the repository
git clone https://github.com/zagreus813/queen-duel-alphabeta-agent.git
cd queen-duel-alphabeta-agent

# Install dependencies
pip install -r requirements.txt
```
