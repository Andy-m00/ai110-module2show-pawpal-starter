from datetime import date, timedelta

import streamlit as st

from pawpal_system import Owner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
if "show_schedule" not in st.session_state:
    st.session_state.show_schedule = False

owner = st.session_state.owner

st.title("🐾 PawPal+")
st.markdown(
    """
PawPal+ helps you organize care tasks for your pets and build a daily schedule.
Your owner, pet, and task data stays available during this Streamlit session.
"""
)

owner.name = st.text_input("Owner name", value=owner.name, key="owner_name")

with st.expander("Add a pet", expanded=not owner.pets):
    with st.form("add_pet_form"):
        pet_name = st.text_input("Pet name")
        species = st.selectbox("Species", ["dog", "cat", "other"])
        breed = st.text_input("Breed")
        age = st.number_input("Age (years)", min_value=0, max_value=100, value=1)
        add_pet = st.form_submit_button("Add pet")

# this section adds a pet using method owner.add_pet. it also uses another function called find_pet() that returns a 
# pet object if its located in owner.pets. if the pet is not found, it will return NONE. 
# The method find_pet doubles as a convienint way to navigate 
# to specific pet objects to add or remove tasks to its dynamic lists of task objects.

    if add_pet:
        if not pet_name.strip():
            st.error("Enter a name for your pet.")
        elif owner.find_pet(pet_name.strip()) is not None:
            st.warning("A pet with that name already exists.")
        else:
            owner.add_pet(
                name=pet_name.strip(),
                species=species,
                breed=breed.strip(),
                age=int(age),
            )
            st.success(f"Added {pet_name.strip()}.")

# this section adds care tasks to a pet object. it uses a method in class Pet called create_task() to add tasks.
# it utilizes a st.selectbox and the find_pet() method to choose a specific pet to add tasks to. It loads the pet object
# into a variable called selected_pet. The create_task() method is called on the selected_pet object to add a task
# to its dynamic list of task objects. select boxes are utilized for choosing time of day and priorityto reduce user input errors.
# it also importanatly calls a function from scheduler class called scheduletask that immediately adds and organizes it into
# a daily schedule. If the task cannot be added to the schedule, it is removed from the pet's list of tasks and an error message is displayed.

if owner.pets:
    st.subheader("Add a care task")
    selected_pet_name = st.selectbox(
        "Pet",
        [pet.name for pet in owner.pets],
        key="selected_pet_name",
    )
    selected_pet = owner.find_pet(selected_pet_name)

    with st.form("add_task_form"):
        task_description = st.text_input("Task description", value="Morning walk")
        time_of_day = st.selectbox(
            "Time of day", ["morning", "afternoon", "evening"]
        )
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        recurrence_choice = st.selectbox(
            "Repeat",
            ["One time", "Every week", "Every day"],
        )
        day_of_week = st.selectbox(
            "Day of week",
            [
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ],
        )
        add_task = st.form_submit_button("Add task")

    if add_task:
        if not task_description.strip():
            st.error("Enter a description for the task.")
        elif selected_pet is not None:
            recurrence = {
                "One time": "once",
                "Every week": "weekly",
                "Every day": "daily",
            }[recurrence_choice]
            scheduled_date = (
                owner.scheduler.next_date_for_weekday(day_of_week)
                if recurrence == "once"
                else None
            )
            task = selected_pet.create_task(
                time_of_day=time_of_day,
                duration=int(duration),
                task_description=task_description.strip(),
                priority=priority,
                pet_name_class=selected_pet.name,
                recurrence=recurrence,
                day_of_the_week=day_of_week if recurrence != "daily" else None,
                scheduled_date=scheduled_date,
            )
            if not owner.scheduler.task_is_due(task, owner.scheduler.schedule_date):
                st.success("Task saved for its selected day.")
            elif owner.scheduler.scheduleTask(task):
                st.success("Task added to the current schedule.")
            else:
                selected_pet.tasks.remove(task)
                st.error(
                    f"Not enough available time in the {time_of_day} for this task."
                )
########################################################################################################
########################################################################################################
########################################################################################################

    st.subheader("Remove a care task")
    if selected_pet.tasks:
        if "remove_task_widget_version" not in st.session_state:
            st.session_state.remove_task_widget_version = 0
        remove_task_key = (
            f"remove_task_selected_{selected_pet.name}_"
            f"{st.session_state.remove_task_widget_version}"
        )

        with st.form("remove_task_form"):
            selected_task_index = st.selectbox(
                "Select a task to remove:",
                options=range(len(selected_pet.tasks)),
                format_func=lambda index: (
                    f"{selected_pet.tasks[index].task_description} "
                    f"({selected_pet.tasks[index].time_of_day}, "
                    f"{selected_pet.tasks[index].duration} min)"
                ),
                index=None,
                placeholder="Choose a task to remove",
                key=remove_task_key,
            )
            remove_task = st.form_submit_button("Remove task")

        if remove_task and selected_task_index is None:
            st.warning("Select a task to remove.")
        elif remove_task:
            selected_task = selected_pet.tasks[selected_task_index]
            if owner.scheduler.removeTask(selected_task, selected_pet):
                st.session_state.remove_task_widget_version += 1
                st.success(f"Removed task '{selected_task.task_description}'.")
                st.rerun()
            else:
                st.error(f"Failed to remove task '{selected_task.task_description}'.")
    else:
        st.info("No tasks available to remove.")
   
else:
    st.info("Add a pet before creating care tasks.")

#######################################################################################################
#######################################################################################################
#######################################################################################################

st.divider()
st.subheader("Daily schedule")
today_column, tomorrow_column = st.columns(2)
if today_column.button("Today's schedule"):
    st.session_state.schedule_failures = owner.scheduler.generate_schedule(
        date.today()
    )
    st.session_state.show_schedule = True
if tomorrow_column.button("Tomorrow's schedule"):
    st.session_state.schedule_failures = owner.scheduler.generate_schedule(
        owner.scheduler.schedule_date + timedelta(days=1)
    )
    st.session_state.show_schedule = True

if st.session_state.show_schedule:
    if st.session_state.get("schedule_failures"):
        st.error(
            "Some tasks could not fit in the available time: "
            + ", ".join(
                task.task_description
                for task in st.session_state.schedule_failures
            )
        )
    if owner.scheduler.daily_schedule:
        rows = owner.scheduler.view_schedule()
        st.table(rows)
        st.caption(
            f"Schedule for {owner.scheduler.whatDayIsIt.title()} "
            f"({owner.scheduler.schedule_date:%Y-%m-%d})"
        )
        st.caption(
            "Remaining minutes — "
            + ", ".join(
                f"{period}: {minutes}"
                for period, minutes in owner.scheduler.available_minutes.items()
            )
        )
    else:
        st.info("Add a care task to build your daily schedule.")

#################################################################################################################
#################################################################################################################


    st.subheader("Mark a care task as complete")

    all_tasks = [
        task
        for task in owner.scheduler.daily_schedule
        if not task.completion_status
    ]
    if all_tasks:
        if "mark_complete_widget_version" not in st.session_state:
            st.session_state.mark_complete_widget_version = 0
        mark_complete_key = (
            f"mark_complete_task_{st.session_state.mark_complete_widget_version}"
        )
        with st.form("mark_complete_form"):
            selected_task_index = st.selectbox(
                "Select a task to mark as complete:",
                options=range(len(all_tasks)),
                format_func=lambda index: (
                    f"{all_tasks[index].pet_name_class}-"
                    f"{all_tasks[index].task_description} "
                    f"({all_tasks[index].time_of_day}, "
                    f"{all_tasks[index].duration} min, "
                    f"Complete: {all_tasks[index].completion_status})"
                ),
                index=None,
                placeholder="Choose a task to mark complete",
                key=mark_complete_key,
            )
            mark_complete = st.form_submit_button("Mark as complete")

        if mark_complete and selected_task_index is None:
            st.warning("Select a task to mark as complete from uncomplted tasks")
        elif mark_complete:
            selected_task = all_tasks[selected_task_index]
            if selected_task.markscomplete():
                if selected_task.recurrence == "once":
                    selected_pet = owner.find_pet(selected_task.pet_name_class)
                    if selected_pet is not None and selected_task in selected_pet.tasks:
                        selected_pet.tasks.remove(selected_task)
                st.session_state.mark_complete_widget_version += 1
                st.success(f"Marked task '{selected_task.task_description}' as complete.")
                st.rerun()
            else:
                st.error(f"Failed to mark task '{selected_task.task_description}' as complete.")
    else:
        st.info("No tasks available to mark as complete.")
   