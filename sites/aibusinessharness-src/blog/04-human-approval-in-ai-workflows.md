---
title: Human Approval in AI Workflows: What Should Stay Under Review?
slug: human-approval-in-ai-workflows
meta_title: Human Approval in AI Workflows: A Practical Guide
description: Learn where AI workflows should run automatically, where human approval belongs, and which business actions should stay off-limits to AI.
keyword: human approval AI workflows
category: Safety and control
image_alt: Human approval checkpoint in an AI business workflow before an external action is completed
excerpt: Approval gates are one of the controls that make AI workflows safer to use with customers. The trick is putting them in the right places, so you keep control without becoming the bottleneck.
---

Human approval is one of the controls that makes AI workflows safer to use with customers and business records. The challenge is placing it at the right points.

Require review for every tiny step, and the workflow becomes slow and frustrating. Remove review entirely, and a single wrong recipient, price or record update can create a much bigger problem.

The practical approach: **put human approval where a mistake would be expensive, hard to reverse, or visible to someone outside the business, and avoid interrupting low-risk internal work.**

Before assigning any action to a tier, confirm the workflow has a defined purpose, limited permissions, test data, logging and a stop condition. "No approval required" never means "no controls required." (New to the idea? Start with [what an AI business harness is](/blog/what-is-an-ai-business-harness/).)

## A three-tier framework

Sort every action in a workflow into one of three tiers.

### Tier 1: Let it run

Actions that are internal, reversible and low-risk.

- Reading and categorizing incoming inquiries
- Summarizing a long email thread
- Tagging records or adding internal notes
- Building a daily list of open items
- Drafting messages into a drafts folder

If one of these goes wrong, the issue is usually easy to detect and correct before it reaches a customer or changes an important record. These actions can run without individual approval, but only once the workflow has been scoped, permissioned, tested and logged.

### Tier 2: Prepare, then approve

Actions that a customer or partner will see, or that change important records.

- Sending any external email or text
- Updating prices, quotes or job details
- Changing a customer's status in the CRM
- Scheduling or cancelling appointments

The AI does the preparation (finding the right record, drafting the message, filling in the details) and a person makes the final call. This is where most of the time savings live: the human spends ten seconds reviewing instead of ten minutes producing.

### Tier 3: Off-limits

Actions the workflow should never take, approval or not.

- Moving money or issuing refunds
- Deleting records permanently
- Changing passwords, permissions or security settings
- Making contractual commitments

These should be excluded from the workflow's permissions entirely, not treated as actions the AI may request and a person may approve. The safest permission is the one that was never granted.

## Designing a good approval step

An approval gate only works if reviewing is fast and easy. Good ones share a few traits:

**Everything needed to decide is on one screen.** The draft, the customer, the last interaction, and why the AI suggested this action.

**Approve, edit and reject are all one click.** If editing means starting over, people will rubber-stamp instead.

**Rejections are captured.** When someone rejects a draft, a short reason ("wrong tone," "already called them") becomes feedback that improves the workflow.

**Nothing sits forever.** Pending approvals that go stale should escalate or expire, not silently pile up.

## Watch out for approval fatigue

If a reviewer approves fifty identical drafts a day without changes, two things are true: the workflow is working well, and the reviewer has stopped really reading. That's the moment to consider lighter review for that specific action, and only that action. For example, a business might spot-check a sample of items or review a daily digest. The right sampling rate depends on the workflow's risk, error rate and consequences.

### Reducing review deliberately

Reduced review should be an explicit operational decision, documented with an owner, a threshold, a sampling method and a rollback condition:

1. Track approval and edit rates for the action over several weeks.
2. Agree on a threshold that justifies less review.
3. Keep logging and spot-checking after the change.
4. Move it back to full review if quality slips. Your [AI activity log](/blog/what-to-log-ai-agent-business-work/) is how you'll know.

## A worked example

Here's an inquiry-handling workflow, like the [AI email assistant](/blog/ai-email-assistant-small-business/) setup, with gates placed by tier:

| Step | Tier | Who acts |
|---|---|---|
| Read new inquiry and classify it | 1 | AI |
| Look up customer history | 1 | AI |
| Draft a reply in the drafts folder | 1 | AI |
| Flag urgent requests to the owner | 1 | AI |
| Send the reply | 2 | Person approves |
| Update the CRM status | 2 | Person approves |
| Offer a discount | 3 | Never automated |

The result: the owner opens their drafts each morning to find replies already written, reviews them in minutes, and sends. No AI ever speaks to a customer unsupervised.

## The principle behind it

Human approval isn't a sign that AI can't be trusted. It's how trust gets built. Every approved draft is evidence. Over time, that evidence tells you, with data instead of hope, which actions are ready for more independence.

That's the model we use at AI Business Harness: AI prepares, your team decides, and the record shows exactly how well it's working. [Tell us about a workflow](/#contact) you'd like to bring under control.
