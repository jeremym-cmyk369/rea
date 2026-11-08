# Grok Bot Agent Teams — Vetted Starting Points

Research notes for the AI Business Harness (Nov 7, 2026). This is a list of links and how to import each one. No outside code is copied into this repo.

## What Grok Bot is

xAI's Grok Bot (early beta, launched Aug 11, 2026) gives you named, always-on agents. Each agent has its own cloud computer (browser, files, terminal), shared plugins (Gmail, GitHub, Calendar and others) and routines. It only comes back to you when something needs approval. Access comes with paid Cursor plans or a linked SuperGrok subscription. Check X Premium pricing in your own account before you pay.

## Confirmed repos

| # | Project | Repo | Status | Use it for |
|---|---------|------|--------|------------|
| 1 | Agent Org Chart | https://github.com/serenakeyitan/agent-org-chart | Real, ~125 stars | **Start here.** Ready-made teams for Marketing, Sales/SDR, Support, Engineering |
| 2 | Grok Bot Profiles | https://github.com/HAEGONG/grok-bot-profiles | Real, ~45 stars | Strict separation of duties: Spec Writer, Bug Reproducer, PR Producer, PR Verifier (no bot approves its own work) |
| 3 | multiBot | https://github.com/simo255/multiBot | Real, ~49 stars, new | A bot that creates other bots and hands heavy work to coding tools (Claude Code, Cursor, Codex). Wait until it's more proven |
| 4 | PhoneZero | https://github.com/function1st/PhoneZero | Reported by Grok, not yet reviewed | Phone calls through Telnyx that only go out after you approve. Relevant to the missed-call agent offer |

Not confirmed: Grok Factory, BOTROSTER, HyperGrok Trading Desk, "Grok Bot Second Brain", grokbot-x, Foreman (several unrelated projects share that name). Check the real URLs behind the t.co links before using any of them.

Trading tools (Cryptofeed, CCXT, Freqtrade, VectorBT, QuantStats) are real and well established, but they're **not relevant** to the business.

## How to import

In Grok Bot chat:

```
Import marketing from https://github.com/serenakeyitan/agent-org-chart
```

This creates a Project Manager plus Market Researcher, Product Marketer, Website Ops, Performance Marketer and Marketing Analyst.

For Grok Bot Profiles, create a new Bot and paste the profile's `SETUP.md` raw URL as instructed in that repo's README.

## First job (suggested)

Give the Marketing team **one** job: a monthly SEO report for Emerald Computers and Arizona Computer Recycling. Jeremy approves it before it goes to the client.

## Safety rules (always)

- Read the repo's code, or have Claude review it, before you install anything.
- Never paste passwords, API keys or login links into a bot chat.
- Human approval comes before anything is published, sent, merged or called.
- Bots never get write access to the live site files on Hostinger. No full-site deploys.
- Never use the Gmail account for outreach. Use jeremy@aibusinessharness.com only.
- Never delete anything from GitHub or Hostinger, and back everything up first.
- One AI per task. Claude, ChatGPT and Grok coordinate and don't overwrite each other's work.
