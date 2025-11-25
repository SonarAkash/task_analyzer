# Smart Task Analyzer

A Python/Django application that prioritizes tasks using a weighted scoring algorithm. This tool helps users identify "what to work on next" by balancing urgency, importance, and effort.

## 🚀 Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SonarAkash/task_analyzer.git
    cd task_analyzer
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Start the server:**
    ```bash
    python manage.py runserver
    ```
    Access the application at `http://127.0.0.1:8000/`.

---

## 🧠 Algorithm Design

The core logic resides in `tasks/scoring.py`. I implemented the **Strategy Pattern** to allow the sorting logic to adapt to different user needs.

### The Formula
The base score is calculated as:
`Score = (Urgency × W1) + (Importance × W2) + (Effort Bonus × W3) + (Dependency × W4)`

### Design Decisions & Trade-offs
1.  **Inverted Effort Score:** Instead of penalizing high effort, I calculate `(10 / estimated_hours)`. This rewards small tasks ("Quick Wins") without heavily punishing large projects.
2.  **Urgency Curve:** Simple linear sorting fails for overdue tasks. I implemented a curve where overdue tasks gain exponential points per day late (`score += 100 + days_late * 5`), ensuring they always jump to the top.
3.  **Stateless API:** The `analyze` endpoint accepts a JSON payload and returns results without requiring a DB write. This makes the tool faster for "what-if" analysis.

### Handling Critical Edge Cases
* **Missing Due Dates:** Tasks with no deadline are treated as having 0 urgency but are still scored on Importance/Effort.
* **Overdue Tasks:** Automatically flagged as critical (Red visual indicator).
* **Invalid Data:** Implemented robust type conversion and Django validators to ensure only clean data enters the scoring engine.

---


## ✅ Bonus Challenges Attempted
* **Unit Tests:** comprehensive tests in `tasks/tests.py` verifying all strategies.
* **Visual Priority Indicators:** UI changes color (Red/Yellow/Green) based on calculated score.
* **Input Sanitization:** Frontend prevents selecting past dates for new tasks.

## 🔮 Future Improvements
With more time, I would implement:
* **Dependency Graph Visualization:** A visual node graph to show circular dependencies.
* **Eisenhower Matrix:** A 2D grid view mapping Urgency vs. Importance.
* **User Accounts:** To allow users to save and retrieve their specific task history.