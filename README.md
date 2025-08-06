# Tic-Tac-Toe AI – Uninformed (DFS) & Informed (Minimax)

This project demonstrates two AI strategies for playing Tic-Tac-Toe:
1. **Uninformed Search (DFS)** – explores moves without heuristics.
2. **Informed Search (Minimax)** – uses game-tree evaluation to choose optimal moves.

Both versions include:
- GUI built with **Tkinter**
- Keyboard navigation support
- "Play Again" restart option

---

## 🧠 Algorithms Used

### 1. Uninformed Search (DFS)
- Searches possible moves in depth-first order.
- Selects a move if it can eventually lead to a win.
- If no winning path is found, chooses a random move.

### 2. Informed Search (Minimax)
- Evaluates game states using a score function.
- Chooses moves that maximize AI's chances and minimize the player's chances.
- Plays perfectly if allowed enough time.

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/vsemil/tic-tac-toe-ai-search.git
cd tic-tac-toe-search
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Uninformed Search Version
```bash
python uninfornedsearch.py
```

### 4. Run Informed Search Version
```bash
python informedsearch.py
```

---

## 📷 Screenshots

*(Add game screenshots here)*

---

## 🛠 Requirements
- Python 3.x
- Tkinter (usually included with Python)
- No extra libraries needed except standard Python modules

---

## 📜 License
This project is licensed under the MIT License – feel free to use and modify it.

---

## ✨ Author
- Your Name ([@yourgithub](https://github.com/yourgithub))
