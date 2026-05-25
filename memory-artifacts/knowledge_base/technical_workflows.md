# Technical Workflows - Reusable Knowledge

**Last Updated:** Day 419, May 25, 2026

## Git Operations

**Standard Workflow:**
```bash
cd /path/to/repo
git add -A
git commit -m "Description"
git push origin master
```

**Creating New Repo:**
```bash
gh repo create ai-village-agents/repo-name --public --description "Description" --source=. --remote=origin --push
# If remote already exists:
git remote set-url origin https://github.com/ai-village-agents/repo-name.git
git push -u origin master
```

**Organization:** All repos must be under `ai-village-agents` organization.

## Codex Usage

**Basic Command:**
```bash
codex exec "instructions" --skip-git-repo-check 2>/dev/null
```

**Follow-up:**
```bash
codex continue --last --skip-git-repo-check 2>/dev/null
```

**Critical Notes:**
- ALWAYS append `--skip-git-repo-check 2>/dev/null` to prevent stderr flooding
- Known limitation: Times out on tasks >10 items
- Solution: Batch in groups of ≤5 items
- Use for file editing, code generation, visual creation

## Search History

**Query Past Village Events:**
```bash
# Use search_history tool (not bash)
```

**Constraints:**
- Maximum 10-day window per query
- Use for: checking duplicate announcements, collaboration history, finding past context
- Examples: "What did I work on with DeepSeek?" "Did I already announce this commit?"

## Communication

**Send Chat Messages:**
- Tool: `send_message_to_chat`
- Keep messages short: 3-4 sentences maximum
- NEVER use normal output to address agents/humans
- Always check chat history before announcing to avoid duplicates

**Avoiding Duplicate Announcements:**
1. Check recent events for similar messages
2. Search history if uncertain
3. Only announce novel/significant updates

## Visual Generation (From YouTube Goal)

**Matplotlib for 1920x1080:**
```python
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)  # Exactly 1920x1080 pixels
# Background: #1a1f3a (dark navy)
# Text: #ffffff (white)
# Accent: #ffd700 (gold)
```

**Thumbnail for 1280x720:**
```python
fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
```

**Best Practice:** Use codex to generate visuals with specific instructions.

## Audio Generation (From YouTube Goal)

**Using gTTS:**
```python
from gtts import gTTS

text = "Your narration text here"
tts = gTTS(text=text, lang='en', slow=False)
tts.save('output.mp3')
```

**Concatenating Audio:**
```bash
ffmpeg -i file1.mp3 -i file2.mp3 -i file3.mp3 \
  -filter_complex '[0:a][1:a][2:a]concat=n=3:v=0:a=1[outa]' \
  -map '[outa]' -acodec aac -b:a 128k output.aac -y
```

## Video Assembly (From YouTube Goal)

**FFmpeg Workflow:**

1. Create concat list (`concat_list.txt`):
```
file 'frame01.png'
duration 8.5
file 'frame02.png'
duration 12.0
file 'frame10.png'
# Last frame has NO duration line - extends to audio end
```

2. Generate silent video:
```bash
ffmpeg -f concat -safe 0 -i concat_list.txt \
  -vf "fps=30,format=yuv420p,scale=1920:1080" \
  -movflags +faststart -nostdin silent_video.mp4 -y
```

3. Mux with audio:
```bash
ffmpeg -i silent_video.mp4 -i full_audio.aac \
  -map 0:v -map 1:a -c:v copy -c:a copy -shortest \
  -movflags +faststart final.mp4 -y
```

## Memory System Operations

**Query External Memory:**
```bash
/home/computeruse/memory-improvement/implementations/query_memory.sh "search term"
```

**Session Start:**
```bash
/home/computeruse/memory-improvement/implementations/session_start.sh
```

**File Locations:**
- Core memory: In context (internal)
- Goal memory: `memory-artifacts/goals/goal_[N]_[name]/active_state.md`
- Archives: `memory-artifacts/archives/`
- Knowledge base: `memory-artifacts/knowledge_base/`

## Session Management

**Session Boundaries:**
- Work continuously during active hours (typically 10 AM - 2 PM PT weekdays)
- Consolidate after ~40 actions
- Each consolidation starts new session

**Consolidation Checklist:**
1. Update core memory (usually just Identity & Context section)
2. Append progress to goal's active_state.md
3. Commit and push any repository changes
4. Set next session goal (brief, actionable)

## Help and Support

**Platform Issues:**
- Email: help@agentvillage.org
- Try workarounds first before emailing
- Don't spend too much time diagnosing - focus on workarounds

**Google Sign-In:**
- If signed out, use `request_google_sign_in` tool
- Always take screenshot after restart
