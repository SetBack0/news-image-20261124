# Project goal — make.fun news-image-20261124

## Objective
Build the entry for make.fun's bounty **"Sum up 24 November's world news in one image"**
(https://make.fun/bounty/news-image-20261124): one image that sums up the
world's news of **Tuesday 24 November 2026**. Prize: $100 USDC, top 50 entries
(1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20).

## Deliverables (in this repo, on branch `main`)
1. `main.ts` (Node 22, standard library only, no network) **or** `main.py`
   (Python 3.13, stdlib only) at the repo root. It writes one image to
   `/output/entry.png`. Run locally with:
   `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts`
   (or the Python equivalent — if you use Python, update the README's Run
   command to match).
2. `entry.png` — the image itself, held in the repo. The simplest valid
   program copies it to `/output/entry.png`; a program may also draw it.

## The image
- PNG or JPEG, at most 1 MiB and 1024×1024 px.
- It must sum up the events that happened, or were first reported, on
  **24 November 2026** (any time zone), **name that date in the image**, and
  cover the day's most consequential stories across regions and fields.
- It is judged by an AI image judge against other entries, pairwise, by what
  the image itself shows (the judge has no news feed). Legible at ~300 px
  across; no garbled text, no smears.
- Do not copy another entry's image or a news photo/artwork you have no right
  to license. The entry is your own work.

## Hard rules (breaking these = rejected entry, no prize)
- Work in a **recorded session** (Claude Code, Codex, Cursor, Superbot, or
  Muse with session files + usage rows). A session handed over afterwards or
  pasted from chat takes **no paid place**.
- Your session must start **at or after 2026-11-24 00:00 UTC**.
- Write the program yourself in this repo. Do not copy the kit's starter
  files. The entrypoint needs at least one line you authored; revise it at
  least twice (two separate assistant messages writing/editing it).
- The program runs twice in a sandbox with no network (1 CPU, 512 MB, 60 s);
  **both runs must write identical bytes**.
- Keep the repo public, keep its MIT license, never rewrite history so the
  submitted commit disappears.

## Hand back to the supervisor
1. Push your work to `main` (or tell the supervisor the branch/commit).
2. Hand over your **session transcript files** and **usage records** (token
   counts per assistant message) for every session that touched this repo,
   plus the **run record**: your opening prompt, harness + version, provider,
   model, effort, and the MCP servers used.
3. Say which run command the entry uses (Node or Python).

## Deadline
Entries close **2026-11-26 00:00 UTC (08:00 Beijing, Nov 26)**. Results within
1 day of the deadline (due Dec 10 at the latest). Max 10 submissions/day, 20
total; the last submission before the deadline is the final entry.
