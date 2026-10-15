from datetime import date

import pytest

from pawpal_system import Owner, Pet, Task


@pytest.fixture
def owner() -> Owner:
    return Owner(name="Jordan")


@pytest.fixture
def pet(owner: Owner) -> Pet:
    return owner.add_pet(name="Mochi", species="dog", breed="Shiba Inu", age=3)


def make_task(
    pet: Pet,
    *,
    time_of_day: str = "morning",
    duration: int = 30,
    description: str = "walk",
    priority: str = "high",
    recurrence: str = "daily",
    day_of_the_week: str | None = None,
    scheduled_date: date | None = None,
) -> Task:
    return pet.create_task(
        time_of_day=time_of_day,
        duration=duration,
        task_description=description,
        priority=priority,
        pet_name_class=pet.name,
        recurrence=recurrence,
        day_of_the_week=day_of_the_week,
        scheduled_date=scheduled_date,
    )


def test_owner_creates_scheduler_and_adds_pets(owner: Owner) -> None:
    assert owner.scheduler.owner is owner
    assert owner.find_pet("Mochi") is None

    pet = owner.add_pet("Mochi", "dog", "Shiba Inu", 3)

    assert owner.find_pet("Mochi") is pet
    assert owner.pets == [pet]


def test_pet_create_task_stores_and_returns_task(pet: Pet) -> None:
    task = make_task(pet, duration=15, description="feed")

    assert task in pet.tasks
    assert task.duration == 15
    assert task.task_description == "feed"
    assert task.completion_status is False


def test_task_completion_can_be_marked_and_reset(pet: Pet) -> None:
    task = make_task(pet)

    assert task.markscomplete() is True
    assert task.completion_status is True

    task.reset_completion()

    assert task.completion_status is False


@pytest.mark.parametrize(
    ("recurrence", "weekday", "scheduled_date", "expected"),
    [
        ("daily", None, None, True),
        ("weekly", "monday", None, True),
        ("weekly", "tuesday", None, False),
        ("once", None, date(2025, 1, 6), True),
        ("once", None, date(2025, 1, 7), False),
        ("never", None, None, False),
    ],
)
def test_task_is_due_for_recurrence(
    owner: Owner,
    pet: Pet,
    recurrence: str,
    weekday: str | None,
    scheduled_date: date | None,
    expected: bool,
) -> None:
    task = make_task(
        pet,
        recurrence=recurrence,
        day_of_the_week=weekday,
        scheduled_date=scheduled_date,
    )

    assert owner.scheduler.task_is_due(task, date(2025, 1, 6)) is expected


@pytest.mark.parametrize(
    ("weekday", "expected"),
    [
        ("monday", date(2025, 1, 6)),
        ("tuesday", date(2025, 1, 7)),
        ("sunday", date(2025, 1, 12)),
    ],
)
def test_next_date_for_weekday(weekday: str, expected: date) -> None:
    scheduler = Owner(name="Jordan").scheduler

    assert scheduler.next_date_for_weekday(weekday, date(2025, 1, 6)) == expected


def test_next_date_for_invalid_weekday_raises(owner: Owner) -> None:
    with pytest.raises(ValueError, match="Invalid weekday"):
        owner.scheduler.next_date_for_weekday("Funday", date(2025, 1, 6))


def test_schedule_task_rejects_task_not_due_today(pet: Pet, owner: Owner) -> None:
    owner.scheduler.schedule_date = date(2025, 1, 6)
    task = make_task(
        pet,
        recurrence="weekly",
        day_of_the_week="tuesday",
    )

    assert owner.scheduler.scheduleTask(task) is False
    assert owner.scheduler.daily_schedule == []


def test_schedule_task_sorts_by_time_priority_and_duration(
    pet: Pet, owner: Owner
) -> None:
    owner.scheduler.schedule_date = date(2025, 1, 6)
    evening = make_task(pet, time_of_day="evening", description="evening")
    low_priority = make_task(pet, description="low priority", priority="low")
    long_high_priority = make_task(pet, description="long", duration=30)
    short_high_priority = make_task(pet, description="short", duration=10)

    for task in (evening, low_priority, long_high_priority, short_high_priority):
        assert owner.scheduler.scheduleTask(task) is True

    assert owner.scheduler.daily_schedule == [
        short_high_priority,
        long_high_priority,
        low_priority,
        evening,
    ]


def test_schedule_task_rejects_work_over_time_period_capacity(
    pet: Pet, owner: Owner
) -> None:
    owner.scheduler.available_minutes["morning"] = 30
    task = make_task(pet, duration=31)

    assert owner.scheduler.scheduleTask(task) is False
    assert owner.scheduler.daily_schedule == []
    assert owner.scheduler.available_minutes["morning"] == 30


def test_schedule_task_does_not_duplicate_scheduled_task(
    pet: Pet, owner: Owner
) -> None:
    task = make_task(pet, duration=20)

    assert owner.scheduler.scheduleTask(task) is True
    assert owner.scheduler.scheduleTask(task) is True
    assert owner.scheduler.daily_schedule == [task]
    assert owner.scheduler.available_minutes["morning"] == 339


def test_generate_schedule_resets_capacity_and_task_completion(
    pet: Pet, owner: Owner
) -> None:
    task = make_task(pet, duration=20)
    task.markscomplete()

    failed_tasks = owner.scheduler.generate_schedule(date(2025, 1, 6))

    assert failed_tasks == []
    assert owner.scheduler.schedule_date == date(2025, 1, 6)
    assert owner.scheduler.whatDayIsIt == "monday"
    assert owner.scheduler.daily_schedule == [task]
    assert task.completion_status is False
    assert owner.scheduler.available_minutes["morning"] == 339


def test_generate_schedule_returns_due_tasks_that_exceed_capacity(
    pet: Pet, owner: Owner
) -> None:
    task = make_task(pet, duration=360)

    assert owner.scheduler.generate_schedule(date(2025, 1, 6)) == [task]
    assert owner.scheduler.daily_schedule == []


def test_remove_task_restores_capacity_for_scheduled_task(
    pet: Pet, owner: Owner
) -> None:
    task = make_task(pet, duration=25)
    owner.scheduler.scheduleTask(task)

    assert owner.scheduler.removeTask(task, pet) is True
    assert pet.tasks == []
    assert owner.scheduler.daily_schedule == []
    assert owner.scheduler.available_minutes["morning"] == 359


def test_remove_task_returns_false_for_task_not_owned_by_pet(
    pet: Pet, owner: Owner
) -> None:
    task = make_task(pet)
    pet.tasks.remove(task)

    assert owner.scheduler.removeTask(task, pet) is False


def test_view_schedule_formats_scheduled_task(pet: Pet, owner: Owner) -> None:
    task = make_task(
        pet,
        time_of_day="afternoon",
        duration=15,
        description="feeding",
        recurrence="weekly",
        day_of_the_week="monday",
    )
    task.markscomplete()
    owner.scheduler.generate_schedule(date(2025, 1, 6))

    assert owner.scheduler.view_schedule() == [
        {
            "Pet": "Mochi",
            "Time": "afternoon",
            "Task": "feeding",
            "Duration": 15,
            "Scheduled date": "2025-01-06",
            "Day of week": "monday",
            "Repeats": "weekly on monday",
            "Complete": False,
        }
    ]