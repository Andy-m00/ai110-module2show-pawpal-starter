# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
it has 4 classes with pet being a subclass of owner and tasks being a subclass of pet. Ideali when everything is done the only way someone can access an instance of tasks is through scheduler and any instance of pet through the owner.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
yes it did. there was some confusion over the way the relationships worked. 
- If yes, describe at least one change and why you made it.
many of the relationshps were changed to "has" realtionships. like owner "has" pets and owner "has" a scheduler.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
the schedulers main constrait my scheulder considers is is how much time there is a day. there are only three spans of time throughout the day. morning(6am to 12am) afternoon(12pm to 6pm) and evening(6pm to 10pm). Aside from that its simple organization of tasks throughout the day in order of priority and then duration, less duration goes first.
- How did you decide which constraints mattered most?
I decided what the constraints were based on myself. The user is allowed to decide whether something is high priority or not but a task that takes less WILL be asigned first among tasks with the same priority level. This refelcts the way i personally order my tasks. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One trade off I made was allowing the user less input over their schedule in terms of start times. Everything is static and set. There are three times a day and a specific amount of minutes in each, theres no room for spill over. If you have 15 unused minutes in your morning and 30 in your afternoon you cannot add a 45 minute task inbetween. Also The program allows for tasks with the same descriptors since I didnt have the time to create a text box to prompt the users if they wanted to  make the already added task last longer. 

- Why is that tradeoff reasonable for this scenario?
 The trade-off is reasonable because more percise time picking and conflict management would've required more code which rings true for many of the other trade offs I made. I can easily see a half a dozen processes in app.py that i could have turned into functions that made the lines in app.py look less crowded but that would've require more time and maybe another files worth of code to import into app.py.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI tools extensively during this project, much more than the last project. Like I said in question 2, I was halfway through properly implementing my code when I read It needed to; generate a daily schedule, check the next day, and asign whether a task was daily or weeekly or only on a specific day. It was a lot of debugging for the first half and heavy brainstroming and refractoring in the last half.
- What kinds of prompts or questions were most helpful?
Descriptive prompts that specifically highlighted the issue and didn't give the AI free range to append or remove things were the most helpful. A lot of the times i asked it to review my code or ask for help on a section that wasnt working I specified that it should show me in plain language and psedo-code any changes it would make that follow my original description of what each segment should be doing. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
There were multiple moments where it suggested using these crazy complex algorithms I couldn't even make sense of. I did not accept them for the sake of my ability to be able to read them and make changes.
- How did you evaluate or verify what the AI suggested?
I simply ran tests. Either in main.py or by running streamlit to verify if everything was functioning.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I mostly tested whether or not the dailyschedule list of tasks was in proper order since that indicated wether or not all the functions and classes associated with it were working.
- Why were these tests important?
they were definetley important.
**b. Confidence**

- How confident are you that your scheduler works correctly?
Reasonably confident. I wrote most of the code for the scheduler class and its main scheduletask function so I'm 95% sure it'll work correctly. That being said Towards the end, especially while trying to construct the generateschedule function, not even a detailed prompt could get the Ai assitant to suggest solutions in syntax I could 100% understand. As a result there might be some bugs hidden away in that specifc part of pawpal_systms or its implementaion in the app.py code.

- What edge cases would you test next if you had more time?
I would probably test what would happen if I switched owners, or try to break scheduling tasks by seeing if i go over the remaining minutes, or try inputing somethiing while the UI lags when printing out the schedule.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Im statified with everything aside from the functions that require datetime/timedelta. Before that I was really confident in how well I understood the code. After the AI helped me brainstorm and implement the code for the generatescheule/tommorow button that required a mess of functions, datetime methods, and if else error statements.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration I would definetley imporve the time/ duration design. I didnt have enough time to find out how to use streamlits time_input select box so I could use start times instead of relying on morning, afternoon, and evening slectors with around 300 miutes in each.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important thing I leanred about designing systems or AI on this project is that I should really read the expectations for the programs and brainstorm alot beofre making a uml. I wasted a lot of time rewriting and planning out my class structure and all the functions and attributes it would require. I didnt read the rubric and instructions fully and it led to alot of frusturation and redrafting.
