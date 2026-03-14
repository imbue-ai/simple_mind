---
name: handle-events
description: Handle any event. Use to handle any event from a source that does not have a corresponding, more specific skill.
---

When you receive an event from an *unknown* source, eg, one that does not have a corresponding `handle-<source>` skill (and where none of your skills seem to apply), you should do the following:

1. Check if this source is already in your "ignored_sources.txt" file. If it is, simply ignore the event and do not notify the user (since you have already notified them about this source before and they chose to ignore it). If it is not, proceed to the next steps.
2. Use your `send-message-to-user` skill to notify the user that you received an event from an unknown source. Include the source name and any details you have about the event, and inform them that A) you will be ignoring future events of this type, and B) if they wish to handle such messages, they should tell you how to handle them.
3. Append the source name to the "ignored_sources.txt" file in the current directory (i.e., within the "thinking" folder), which is a simple text file where you keep track of sources that you are ignoring (one source name per line). This will help you avoid repeatedly notifying the user about the same unknown source in the future.
