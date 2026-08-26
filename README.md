# 👑 Queen Duel AI — 3rd Place Tournament Agent (Adversarial Search)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Tournament Rank](https://img.shields.io/badge/Tournament%20Rank-3rd%20Place%20/%2050-gold.svg)](#-tournament-results)
[![Win Rate](https://img.shields.io/badge/Tournament%20Win%20Rate-97.96%25%20(96%2F98)-brightgreen.svg)](#-tournament-results)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An adversarial game-playing AI agent engineered for **Queen Duel** (a competitive $7 \times 7$ Isolation game variant featuring chess-queen movement and directional push mechanics). 

In a course-wide double round-robin tournament against 49 peer agents (98 total matches, alternating player order P1/P2), this agent finished **3rd Place overall with a 96–2 record (97.96% win rate)**[cite: 3].

---

##  Tournament Results

The competition evaluated each agent head-to-head in a double round-robin format against 49 competitors[cite: 3]:

| Metric | Result | Details |
| :--- | :---: | :--- |
| **Final Standing** | **3rd Place** | Out of 50 participating student agents[cite: 3] |
| **Total Games** | **98** | 49 games as Player 1 + 49 games as Player 2[cite: 3] |
| **Wins** | **96** | 97.96% tournament win rate[cite: 3] |
| **Losses** | **2** | 2.04% loss rate[cite: 3] |
| **Baseline Matches** | **99% / 100%** | Measured against randomized and heuristic baselines[cite: 3] |

---

##  Game Mechanics

The game is played on a $7 \times 7$ grid between two queens:
* **Movement:** Moves like a chess Queen across unblocked straight or diagonal paths[cite: 1].
* **Square Contraction:** Every cell vacated by a queen becomes permanently **blocked**[cite: 1].
* **Push Action:** Landing on a tile occupied by the opponent queen pushes them 1 cell in the attack direction[cite: 1].
* **Loss Conditions:** A player loses if pushed out of bounds or if no legal moves remain on their turn[cite: 1].

---

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
To eliminate first-move determinism and bypass hardcoded opening traps, the agent randomly picks from four diagonal anchor points on turn one: `(1,1)`, `(1,5)`, `(5,1)`, and `(5,5)`[cite: 2, 3].

### 2. Pre-Search Margin Filtering (`in_margin_and_push`)
Filters out high-risk candidate moves prior to tree exploration[cite: 2, 3]:
* Identifies boundary tiles overlapping with the opponent's direct line of sight[cite: 2, 3].
* Prevents suicidal moves onto edge cells where an opponent push would immediately eject the queen from the board[cite: 1, 2, 3].

### 3. Dynamic Phase-Based Search Depth
Search depth dynamically adapts to game progression, maximizing tactical vision when the branching factor drops[cite: 2, 3]:
* **Turns $0\text{--}9$:** Depth 2 (rapid opening setup, preserving time budget)[cite: 2, 3].
* **Turns $10\text{--}19$:** Depth 4 (territory consolidation)[cite: 2, 3].
* **Turns $20\text{--}29$:** Depth 6 (board constriction)[cite: 2, 3].
* **Turns $30+$:** Depth 8+ (exhaustive endgame resolution)[cite: 2, 3].

### 4. Heuristic Utility Function (`CustomEvalFn`)
Evaluates game states across mobility, positioning, and tactical threat[cite: 2, 3]:

$$\text{Utility}(s) = \Big(|\mathcal{M}_{\text{player}}| - |\mathcal{M}_{\text{opponent}}|\Big) + \text{Bonus}_{\text{center}} + \text{Bonus}_{\text{push}}$$

* **Mobility Differential:** Maximizes personal move options while strangling opponent branches[cite: 2, 3].
* **Center Dominance:** $+10$ strategic score for holding center tiles `(3,3)`, `(3,4)`, `(4,3)`, `(4,4)`[cite: 2, 3].
* **Push Bonus:** $+15$ incentive for achieving offensive displacement threats[cite: 2, 3].

---

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


## gi Getting Started

### Prerequisites
* Python 3.8 or higher

### Installation
```bash
# Clone the repository
git clone [https://github.com/](https://github.com/)<YOUR_GITHUB_USERNAME>/<REPO_NAME>.git
cd <REPO_NAME>

# Install dependencies
pip install -r requirements.txt
