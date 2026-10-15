"""Class skeleton for the PawPal+ model described in ``uml.mmd``."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Owner:
    name: str
    preferences: dict[str, str] = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)
    scheduler: Scheduler = field(init=False)

    def __post_init__(self) -> None:
        self.scheduler = Scheduler(owner=self)

    def find_pet(self, name: str) -> Pet | None:
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def add_pet(self, name: str, species: str, breed: str, age: int) -> Pet:
        pet = Pet(name=name, species=species, breed=breed, age=age)
        self.pets.append(pet)
        return pet

@dataclass
class Task:
    pet_name_class: str
    time_of_day: str
    duration: int
    task_description: str
    priority: str
    recurrence: str
    day_of_the_week: str | None
    scheduled_date: date | None = None
    completion_status: bool = False

    def markscomplete(self) -> bool:
        self.completion_status = True
        return self.completion_status

    def reset_completion(self) -> None:
        self.completion_status = False

@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def create_task(
        self,
        time_of_day: str,
        duration: int,
        task_description: str,
        priority: str,
        pet_name_class: str,
        recurrence: str = "daily",
        day_of_the_week: str | None = None,
        scheduled_date: date | None = None,
    ) -> Task:
        task = Task(
            time_of_day=time_of_day,
            duration=duration,
            task_description=task_description,
            priority=priority,
            pet_name_class=pet_name_class,
            recurrence=recurrence,
            day_of_the_week=day_of_the_week,
            scheduled_date=scheduled_date,
        )
        self.tasks.append(task)

        return task


@dataclass
class Scheduler:
    owner: Owner
    schedule_date: date = field(default_factory=date.today)
    whatDayIsIt: str = field(
        default_factory=lambda: date.today().strftime("%A").lower()
    )
    daily_schedule: list[Task] = field(default_factory=list)
    available_minutes: dict[str, int] = field(default_factory=lambda: {
        "morning": 359,
        "afternoon": 299,
        "evening": 300,
    })

    def task_is_due(self, task: Task, schedule_date: date) -> bool:
        weekday = schedule_date.strftime("%A").lower()

        if task.recurrence == "daily":
            return True
        if task.recurrence == "weekly":
            return task.day_of_the_week == weekday
        if task.recurrence == "once":
            return task.scheduled_date == schedule_date
        return False

    def next_date_for_weekday(
        self, weekday: str, start_date: date | None = None
    ) -> date:
        weekday_numbers = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }
        if weekday not in weekday_numbers:
            raise ValueError(f"Invalid weekday: {weekday}")

        start_date = start_date or date.today()
        days_ahead = (weekday_numbers[weekday] - start_date.weekday()) % 7
        return start_date + timedelta(days=days_ahead)

    def scheduleTask(self, task: Task) -> bool:
        if not self.task_is_due(task, self.schedule_date):
            return False
        if task in self.daily_schedule:
            return True

        time_order = {"morning": 0, "afternoon": 1, "evening": 2}
        priority_order = {"high": 0, "medium": 1, "low": 2}
        remaining = self.available_minutes[task.time_of_day]
        if task.duration > remaining:
            return False

        new_time = time_order[task.time_of_day]
        new_priority = priority_order[task.priority.strip().lower()]

        for index, scheduled_task in enumerate(self.daily_schedule):
            scheduled_time = time_order[scheduled_task.time_of_day]
            scheduled_priority = priority_order[scheduled_task.priority.strip().lower()]

            if scheduled_time > new_time:
                self.daily_schedule.insert(index, task)
                break

            if scheduled_time < new_time:
                continue

            if scheduled_priority > new_priority:
                self.daily_schedule.insert(index, task)
                break

            if (
                scheduled_priority == new_priority
                and scheduled_task.duration > task.duration
            ):
                self.daily_schedule.insert(index, task)
                break
        else:
            self.daily_schedule.append(task)

        self.available_minutes[task.time_of_day] -= task.duration
        return True

    def generate_schedule(self, schedule_date: date) -> list[Task]:
        self.schedule_date = schedule_date
        self.whatDayIsIt = schedule_date.strftime("%A").lower()
        self.daily_schedule.clear()
        self.available_minutes = {
            "morning": 359,
            "afternoon": 299,
            "evening": 300,
        }

        failed_tasks = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.recurrence in {
                    "daily",
                    "weekly",
                } and self.task_is_due(task, schedule_date):
                    task.reset_completion()

                if self.task_is_due(task, schedule_date):
                    if not self.scheduleTask(task):
                        failed_tasks.append(task)

        return failed_tasks

    def removeTask(self, task: Task, pet: Pet) -> bool:
        if task not in pet.tasks:
            return False

        pet.tasks.remove(task)

        if task in self.daily_schedule:
            self.daily_schedule.remove(task)
            if task.time_of_day in self.available_minutes:
                self.available_minutes[task.time_of_day] += task.duration
            return True

        return True

    def view_schedule(self):
        return [
            {
                "Pet": task.pet_name_class,
                "Time": task.time_of_day,
                "Task": task.task_description,
                "Duration": task.duration,
                "Scheduled date": self.schedule_date.isoformat(),
                "Day of week": self.whatDayIsIt,
                "Repeats": (
                    f"weekly on {task.day_of_the_week}"
                    if task.recurrence == "weekly"
                    else task.recurrence
                ),
                "Complete": task.completion_status,
            }
            for task in self.daily_schedule
        ]
        
