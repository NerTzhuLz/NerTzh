# OpenAI Build Week — annex

Official page: [https://openai.devpost.com/](https://openai.devpost.com/)

## Deadlines (critical)

| Item | When |
|------|------|
| Free Codex credits request (Resources tab) | **Fri Jul 17, 2026 @ 12:00 PM PT** |
| Project submission | **Tue Jul 21, 2026 @ 5:00 PM PT** |

## How to participate (official steps)

1. Read [Official Rules](https://openai.devpost.com/rules).
2. Install the **Devpost Hackathons Plugin** in ChatGPT (desktop/mobile).
3. OpenAI account + **request free Codex credits** (Resources tab) before the credit deadline.
4. Docs: [GPT-5.6](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6), [Codex quickstart](https://learn.chatgpt.com/docs/quickstart).
5. Pick a **track**, build with **Codex + GPT-5.6**, submit.

Plugin entry (ChatGPT): use the Devpost Hackathons plugin from the event page CTA.

## Tracks (pick one)

1. **Apps for your life** — consumer / everyday.
2. **Work and productivity** — teams, workflows, analytics, ops.
3. **Developer tools** — testing, DevOps, agents, security.
4. **Education** — students, teachers, orgs.

Suggested for this repo (`NertzMetalEngine`): **Work and productivity** (live market metrics / trading ops analytics) **or** **Developer tools** if you frame agentic trading metrics tooling.

## What judges want

- **Technological implementation** — real use of Codex; non-trivial working code.
- **Design** — coherent product experience, not only a PoC.
- **Potential impact** — clear audience + problem solved.
- **Quality of the idea** — creative + domain understanding.

## Submission package (must-have)

- [ ] Working project (runnable)
- [ ] Category / track selected
- [ ] Project description
- [ ] Demo video **&lt; 3 min** public YouTube — show it working; audio must cover **how you used Codex AND GPT-5.6**
- [ ] Code repo URL (public, or private shared with `testing@devpost.com` **and** `build-week-event@openai.com`)
- [ ] **README**: setup, sample data if needed, run instructions
- [ ] Highlight where Codex accelerated work and key decisions with GPT-5.6
- [ ] **`/feedback` Codex Session ID** (session where most core functionality was built) on the form
- [ ] If plugin/devtool: install instructions + way for judges to test without full rebuild

## Local notes for this repo (no locks)

- **No model hardcode** — use any model available on your Codex/ChatGPT plan.
- Trading default: `ENV=demo` unless you switch to mainnet on purpose.
- Optional clean shell: `scripts/openai_dev_shell.sh` (does not delete keys from disk).

## Useful links

- Event: https://openai.devpost.com/
- Rules: https://openai.devpost.com/rules
- Dates: https://openai.devpost.com/details/dates
- API platform (docs hub): https://openai.com/api/
- API base (if you call OpenAI from code): `https://api.openai.com/v1`
