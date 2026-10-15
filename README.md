# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output


| pet name | time     | task        | duration | scheduled date | day of the week | repeats | complete |
| Akira    | morning  | feeding     | 20       | 2026-10-14     | wednesday       | daily   | False    |
| Mench    | morning  | walk        | 30       | 2026-10-14     | wednesday       | daily   | False    |
| Akira    | afternoon| outside time| 30       | 2026-10-14     | wednesday       | daily   | False    |
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
`==================================================== test session starts =====================================================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\avaca\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 22 items                                                                                                            

test_pawpal.py ......................                                                                                   [100%]

===================================================== 22 passed in 0.08s =====================================================``

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s)  | Notes |
|---------|-----------           |-------|
| Task sorting      |scheduleTasks()|  by priority then duration. |

| Filtering         |remove(), removetask(), markscomplete()| selectbox dislays uncompleted tasks using a buffer variable all_tasks that deletes a task from its list once its marksed as complete|

| Conflict handling | schedule task(), find_pet(),| error if pet exists or if there arent enough minutes let in morning, afternoon,or evening. adding two tasks with the same description is allowed. The scheduler just assumes your doing the same task for an extra amount of time. |

| Recurring tasks  | next_date_for_weekday(), task_is_due(), scheduletasks(), task| it uses a simple but hard to read generate_schedule() function that  returns a list of tasks by taking the day values that the user was prompted for and comparing it to value whatdayisit in scheduler reseting the comppletion status.|

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. type in your name.
2. use selectboxes and text input boxes to add pet in expander.
3. add task form box requires alot of input from time of the day, weekly, daily, or just one weekday specifically. It assumes your day starts at 6am and ends at 10pm. morning is from 6am to 12pm, afternoon is from 12pm to 6pm, and evening is from 6pm to 10pm. use selectbox to change to which pet youd like to add a task for
4. press todays schdule to print out a table and use box undernaeth it to mark tasks as complete
5. pressing tommorows schedule will iterate through the tasks youve designated. you can always press today schedule to return to your current day.
6. additionally theres a remove tasks box that allows you to remove tasks from a pets task list. it works in tandem with the pet name selectbox for you to navigate to that pets tasks.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
