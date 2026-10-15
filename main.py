"""Testing page for implementation and backend logic."""
from datetime import date, timedelta

from pawpal_system import Owner, Scheduler, Pet, Task  

owner = Owner(name="Jordan")
pet = owner.add_pet(name="Mochi", species="dog", breed="Shiba Inu", age=3)


if owner.find_pet("Mochi") is None:
    pet = owner.add_pet(name="Mochi", species="dog", breed="Shiba Inu", age=3)
    print(f"Added {pet.name}.")
else:
    print("A pet named Mochi already exists.")

if owner.find_pet("akira") is None:
    pet = owner.add_pet(name="akira", species="cat", breed="Siamese", age=2)
    print(f"Added {pet.name}.")
else:
    print(f"A pet named {pet.name} already exists.")     

if owner.find_pet("rockhudson") is None:
    pet = owner.add_pet(name="rockhudson", species="rabbit", breed="lionsmane", age=2)
    print(f"Added {pet.name}.")
else:
    print(f"A pet named {pet.name} already exists.")   


currentpet = owner.find_pet("Mochi")
currentpet.create_task("morning", 30, "walk", "high", "Mochi")
owner.scheduler.scheduleTask(currentpet.tasks[0])
currentpet.create_task("afternoon", 15, "feed", "medium", "Mochi")
owner.scheduler.scheduleTask(currentpet.tasks[1])
currentpet.create_task("evening", 10, "play", "low", "Mochi")
owner.scheduler.scheduleTask(currentpet.tasks[2])

print(f"Tasks for {currentpet.name}:")
for task in currentpet.tasks:
    print(f" - {task.task_description}, {task.duration} minutes, priority: {task.priority}")

currentpet = owner.find_pet("rockhudson")
currenttask = currentpet.create_task("morning", 60, "walk", "high", "rockhudson")
owner.scheduler.scheduleTask(currenttask)
currenttask = currentpet.create_task("afternoon", 5, "feed", "medium", "rockhudson")
owner.scheduler.scheduleTask(currenttask)
currenttask = currentpet.create_task("evening", 10
                                     , "play", "low", "rockhudson")
owner.scheduler.scheduleTask(currenttask)

print(f"Tasks for {currentpet.name}:")
for task in currentpet.tasks:
    print(f" - {task.task_description}, {task.duration} minutes, priority: {task.priority}")

print(f"\nDaily schedule for {owner.name}:")
for day_task in owner.scheduler.daily_schedule:
    print(f"Scheduled task: {day_task.task_description}, {day_task.duration} minutes, priority: {day_task.priority}")

owner.scheduler.generate_schedule(date.today())
schedule_view = owner.scheduler.view_schedule()
print(f"\nSchedule view for {owner.name}:")
print(schedule_view)
