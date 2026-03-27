---
name: dealing-with-the-unexpected
description: Handle unexpected situations where the Minds system does not appear to be working as expected. Use when you encounter behavior that seems to contradict what your docs and prompts and skills say should happen, or when something seems broken and you are unsure how to proceed.
---

The Minds system is still very new, and under active construction, and as a result, you may encounter situations where the system does not seem to be working as expected, or where the behavior seems to contradict what your docs and prompts and skills say should happen.

When you encounter such a situation, your best course of action is usually to submit a bug report to the developers so they can investigate and fix the underlying issue.
Use the `submit-mngr-bug-report` skill to do this **after** collecting as much information about the failure as possible.
You should provide as much detail as possible about the unexpected behavior you observed, what you expected to happen instead, and any relevant context (eg, what events you received, what tools and skills you used, etc).

As soon as you've decided to go collect this information, you should at least *try* to use the `send-message-to-user` skill to notify the user that you have encountered an unexpected issue and are investigating it.
This is not strictly required, but it can help keep the user informed and manage their expectations.

Note that this is one of the few cases where you should do the work **yourself**, rather than delegating to a sub agent via the `delegate-task-to-agent` skill (because the issue is with the system itself, so delegating might not work, and delegating is asynchronous, and you don't want to change the state of the system if you are currently in an error state).

Once the bug report is submitted, you should notify the user, and send them the link (if available) to the bug report so they can track the issue.
After that, you should wait for further instructions from the user on how to proceed.
