---
name: manage-notes-source
description: Configure and read from the user's notes source (file, directory, or conversation thread). Use during onboarding to set up the notes input, and when processing notes into issues.
---

# Managing the notes source

The user's unstructured notes -- raw ideas, task descriptions, half-formed thoughts -- need to come from somewhere. This skill handles setting up and reading from that source.

## Supported sources

### Conversation thread (default)

The simplest option. The user pastes notes directly into a conversation. No setup needed -- just process whatever the user sends.

When the user sends raw notes in a conversation, treat them as input for the `triage-raw-notes` skill.

### File

A single file (e.g., `~/notes/backlog.txt`) that the user maintains. The mind reads from it and removes entries as they are processed.

Store the file path in memory during onboarding. When reading:

```bash
cat <file-path>
```

After an issue is created from an entry, remove that entry from the file (be surgical -- only remove the specific entry, don't reformat the rest).

### Directory

A directory of markdown or text files, each containing one or more notes. Store the directory path in memory.

## Setup (during onboarding)

Ask the user:

```
Where do your raw notes live?
A) I'll just paste them into our conversation
B) A file (tell me the path)
C) A directory of files (tell me the path)
D) Something else (describe)
```

Save the answer to memory. If it's a file or directory, verify it exists and is readable.

For conversation-based input, no further setup is needed. For file/directory sources, you may eventually want to set up a file watcher (delegate to a working agent to build one when the user wants it).

## Guidelines

- Start simple: conversation-based input works immediately with no setup
- Only build a file watcher if the user asks for one
- When removing entries from files, be precise -- only remove the exact entry that was processed
