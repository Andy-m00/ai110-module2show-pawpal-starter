"""Class skeleton for the PawPal+ model described in ``uml.mmd``."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Owner:
    name: str
    preferences: dict[str, str] = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)
    scheduler: Scheduler | None = None

    def addPet(self, _pet: Pet) -> None:
        pass

    def scheduleWalk(self) -> None:
        pass

    def viewDailyTaskSchedule(self) -> None:
        pass

    def planCare(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[DogTasks | CatTasks | RabbitTasks] = field(default_factory=list)


@dataclass
class Scheduler:
    dog_tasks: list[DogTasks] = field(default_factory=list)
    cat_tasks: list[CatTasks] = field(default_factory=list)
    rabbit_tasks: list[RabbitTasks] = field(default_factory=list)

    def scheduleTask(self) -> None:
        pass

    def viewDailyTaskSchedule(self) -> None:
        pass


@dataclass
class DogTasks:
    def groom(self) -> None:
        pass

    def walk(self) -> None:
        pass

    def enrichment(self) -> None:
        pass

    def meds(self) -> None:
        pass

    def feeding(self) -> None:
        pass


@dataclass
class CatTasks:
    def nailTrimming(self) -> None:
        pass

    def enrichment(self) -> None:
        pass

    def meds(self) -> None:
        pass

    def feeding(self) -> None:
        pass


@dataclass
class RabbitTasks:
    def gardenTime(self) -> None:
        pass

    def meds(self) -> None:
        pass

    def feeding(self) -> None:
        pass