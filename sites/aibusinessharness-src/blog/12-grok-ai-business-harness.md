---
title: Grok as One Option Inside an AI Business Harness: What Grok Bot Covers and What It Doesn't
slug: grok-ai-business-harness
meta_title: Grok AI Business Harness: What Grok Bot Covers
description: Grok Bot ships a cloud computer, Auto-review and Enterprise audit controls. See which AI harness pieces it covers and which you still build.
keyword: Grok AI business harness
date: 2026-10-30
category: Platforms
image_alt: Diagram comparing what Grok Bot supplies (cloud computer and app sign-in, model-based Auto-review, Enterprise-only controls) with what a business harness still adds (scoped permissions, exact-action approval, verification, duplicate protection, a business record)
excerpt: Grok Bot comes with more built-in controls than most agent products. It still isn't a complete business harness. Here's where the line falls, and how to use Grok without overtrusting it.
---

Grok is a capable model, and Grok Bot is one of the more complete agent products on the market. Neither one is the harness.

An [AI business harness](/ai-business-harness/) is the operating layer around *any* model: the scoped connections, permissions, approval gates, verification, recovery, duplicate protection and records that let AI do real business work without acting as an unsupervised employee. The model generates and chooses steps. The harness decides what is allowed, what needs a person, and what gets written down.

Grok Bot covers part of that layer. This guide shows which part, what you still have to design yourself, and how to start without overtrusting it.

## The short answer

- **Grok Bot supplies:** a persistent cloud computer, sign-in to the apps you connect, approval prompts, a model-based review step called Auto-review, and (on the Enterprise plan only) network, audit and action-recording controls.
- **The harness still adds:** minimum permissions per workflow, a human approving the *exact* customer-facing action, checks that the action actually worked, protection against doing it twice, and a business record of who approved what.
- **The rule stays the same whatever the model:** AI prepares, people approve what matters, and every important step is verifiable.

## Two ways to use Grok in a business

**The Grok API.** You call Grok from your own code and give it a short list of tools. Your code, not the model, enforces permissions, approvals and logging. This is the most controllable path and fits workflows with clean APIs, like a CRM or a scheduling system. (See [how to connect AI to existing business software](/blog/connect-ai-to-existing-business-software/).)

**Grok Bot.** xAI's managed agent product. Each user account has one persistent cloud computer that the user's Bots share; Bots sign into websites and apps the way a person would, run scheduled routines, and keep working after you close your laptop. It's useful when a tool has no API, which is the trade-off covered in [browser automation versus API integrations](/blog/ai-browser-automation-vs-api-integrations/).

Either way, Grok is the reasoning layer. The harness is what you build around it.

## What Grok Bot already covers

Here's how Grok Bot maps to the [nine components of a business harness](/ai-business-harness/#components), based on xAI's published documentation as of October 2026:

| Harness component | Grok Bot | What that means for you |
|---|---|---|
| Connections | Built in | Bots sign into the apps you connect, including ones without an API |
| Permissions | Partly | A Bot acts as the signed-in account; you still decide which accounts and how much access |
| State and memory | Partly | Bots share one cloud computer per user; separate clients need separate setups |
| Validation and rules | You add | Business rules (is the estimate still open?) are yours to define |
| Human approval | Partly | Approval prompts exist; Auto-review is a model, not a person |
| Recovery | You add | Timeouts and uncertain results need a defined response |
| Duplicate protection | You add | Nothing stops the same email going out twice unless you design for it |
| Audit | Enterprise only | Audit logs and Action Recording are Enterprise features |
| Orchestration | Partly | Routines and Bot-to-Bot handoffs help sequence the work |

## Three details that change how you set it up

### 1. Auto-review is a model, not a human approval

When a Bot wants to take a sensitive action, Grok Bot can ask you to approve it once, always allow it, or deny it. Separately, **Auto-review** uses a review model to screen shell commands, app calls, computer use, automation writes and delegation, and can let an action proceed, require approval or block it.

That's a useful safety net. But xAI's own documentation describes Auto-review as model-based and says it should complement other controls, not replace them. Outside Enterprise, a team member can switch it off. For customer-facing actions such as a quote, a booking or an email, keep a person [approving the exact action](/blog/human-approval-in-ai-workflows/) before it runs.

### 2. The strongest controls are Enterprise-only

Network Controls (limiting which sites a Bot can reach), enforced Auto-review, team review rules, audit logs and Action Recording are all Enterprise features. On the Premium plan or a self-serve Teams plan, you don't get them. On self-serve Teams, Grok Bot is switched on for every member by default, and a team without a network policy allows all network access.

If you're a small business on Premium or Teams, plan to supply these controls in your workflow design rather than assuming the product provides them.

### 3. Audit logs don't show what the Bot did

On Enterprise, audit logs cover admin, security and sign-in events, plus control-plane events such as creating a Bot or changing access. What a Bot actually did inside your tools is captured by a separate setting, **Action Recording**, which is off by default, keeps 90 days of history, and doesn't appear on the Audit Log page.

Even with both turned on, those are product records. A business still needs its own record of the decision: which customer, which estimate, what was drafted, who approved it and whether it was delivered. That's what [an AI activity log](/blog/what-to-log-ai-agent-business-work/) is for.

## What the harness still has to add

Whatever plan you're on, these stay your responsibility:

1. **Scoped permissions.** Sign each Bot into only the accounts its job needs, with the least access that works. A follow-up Bot needs the estimates list and a drafts folder, not your bank account.
2. **Exact-action approval.** A person approves the specific message, recipient and timing. If any of those change, it goes back for approval.
3. **Verification and reconciliation.** After an action, check the other system: did the booking actually save? If the result is uncertain, mark it uncertain and check before retrying.
4. **Duplicate protection.** Track what has already been sent or booked so a retry doesn't create a second email or a double booking.
5. **A business record.** Log the trigger, the data used, the decision, the approver and the verified result, kept for as long as your business needs it.
6. **Client separation.** If you run Bots for more than one business, keep their accounts, credentials, memory and logs apart.

## An example: estimate follow-up with Grok Bot

*Illustrative only; actual behavior depends on your tools and testing.*

A plumbing company sends estimates through its job software, and quotes older than five days often go unanswered.

1. A scheduled Grok Bot routine opens the estimates list each morning and finds open quotes older than five days.
2. It checks each one is still open and hasn't already been followed up.
3. It drafts a short follow-up for each and puts the drafts in a review queue. It does not send anything.
4. The office manager approves, edits or rejects each exact draft.
5. Approved messages are sent, the job record is checked to confirm the send, and the outcome is logged.

Grok Bot does the clicking and drafting. The harness decides what counts as "open," who approves, how sends are confirmed and what gets recorded. The same design works with Grok, another model or a mix. For more on this workflow, see [AI estimate follow-up](/blog/ai-estimate-follow-up-workflow/).

## What it costs (as of October 2026)

- **Grok Bot** has no separate price. It's included from the Premium tier of The X Subscription ($30 per month) upward, on Super and Ultra, and on Teams and Enterprise seats. Free and Plus plans don't include it.
- **The Grok API** is billed per token. xAI's flagship Grok 4.7 lists at $2 per million input tokens and $6 per million output tokens for prompts under 200,000 tokens; the whole request bills at double that rate once a prompt reaches 200,000. Built-in tools such as web search and code execution are billed per call on top.
- **Designing and running the harness** is separate work. It's the part that decides whether the workflow is safe to use with customers.

Prices change often; check xAI's current pricing before you budget.

## Should you standardize on Grok?

Use Grok where it fits the workflow. Its strengths are competitive API pricing, a ready-made agent with a cloud computer that can work inside tools without APIs, and real Enterprise controls for larger teams.

Don't make the model choice the safety plan. Keep the harness rules the same no matter which model is underneath, so you can switch or mix models later without redesigning how approvals, verification and records work. (If the terms are still fuzzy, start with [AI model vs. agent vs. harness](/blog/ai-model-vs-agent-vs-harness/).)

## Frequently asked questions

### Is Grok Bot an AI business harness?

Partly. It supplies connections, a cloud computer, approval prompts, model-based Auto-review and, on Enterprise, network and audit controls. Scoped permissions, exact-action human approval, verification, duplicate protection and a business record still have to be designed and managed.

### Does Grok Bot's Auto-review count as human approval?

No. Auto-review is a review model that screens risky actions. It's a useful safety layer, but customer-facing actions should still go to a person who approves the exact action.

### Which Grok Bot plan includes audit logs?

Audit logs, Action Recording, Network Controls and enforced Auto-review are Enterprise-only as of October 2026. Premium and self-serve Teams plans don't include them.

### Can I use the same harness with Grok, Claude or GPT?

Yes. A harness is model-agnostic. The permissions, approval gates, verification and records stay the same, and the model underneath can change.

## Start with one workflow

Pick one repeated task, define the finish line, measure how it runs today, and keep customer-facing actions under review while you test. The [30-day AI workflow pilot](/blog/30-day-ai-workflow-pilot/) lays out the steps week by week.

*Sources: xAI documentation for [Grok Bot approvals and Auto-review](https://docs.x.ai/grok-bot/approvals-security-and-privacy.md) and the [Grok Bot security FAQ](https://docs.x.ai/grok-bot/security-faq); [xAI API pricing](https://x.ai/api). Product features and prices are as published in October 2026 and may change.*
