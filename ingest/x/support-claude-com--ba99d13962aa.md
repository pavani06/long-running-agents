---
url: "https://support.claude.com/en/articles/16761192-preserved-thinking-changing-how-the-messages-api-handles-thinking-blocks-to-protect-against-distillation"
key: "ba99d13962aa"
status: "ok"
final_url: "https://support.claude.com/en/articles/16761192-preserved-thinking-changing-how-the-messages-api-handles-thinking-blocks-to-protect-against-distillation"
method: "trafilatura"
content_hash: "57ef8eae511946d0cbb0823001b1ad83bf3c2043"
text_len: 5088
fetched: "2026-09-19"
---

With Claude Fable 5.1, we're changing how the Messages API handles thinking blocks to protect against distillation. A thinking block is a record of the reasoning Claude may produce while working on a response. New API accounts for Fable 5.1 will no longer be able to edit the context around a thinking block, such as the messages, tools, or system prompt, during a multi-turn conversation.
Modifying this prior context has legitimate applications, which we continue to support using the adjustments outlined below. However, such modifications are also a common and publicly documented technique for industrial-scale illicit distillation, which is prohibited by our Usage Policy and Terms of Service.
Here's what changes: the API will now verify that a thinking block is sent back with the same system prompt, tools, and messages that produced it, and will return an error if they don't match. In order for modified requests to succeed, developers may opt-in to instead have the thinking blocks removed from such requests; the model will respond without seeing the thinking block. For Fable 5.1, preserved thinking applies to new API accounts only, although this update will apply to all accounts in future model releases.
In this article, we share details on why we're doing this and the adjustments you can make to minimize disruption.
What are thinking blocks?
Claude produces reasoning steps before providing its final answer. On the API, these are returned to the user as "thinking blocks." In a multi-turn conversation, API users send these blocks back with each exchange (along with the system prompt, tools, and earlier messages), so that Claude has full conversational context.
What’s changing?
For impacted accounts (see below) on Fable 5.1, the API will return an error if the system prompt, tools, or messages preceding a prior thinking block have been modified.
To avoid an error message, you may opt into "non-strict" mode. In this mode, the request will go through, but the affected thinking blocks will be dropped from what the model sees. This allows you to continue your conversation or task uninterrupted despite the prior turns’ thinking not being shown to the model. When this happens, the API response will tell you which blocks were dropped.
Why are we making this change?
Altering the earlier turns of a conversation is a common technique used in illicit distillation campaigns, which aim to extract the capabilities of advanced models—especially thinking—to train another model, without authorization. Distillation is often employed on an industrial scale, using thousands of fake accounts. We encrypt Claude's thinking blocks to prevent this, but by editing the conversation before a thinking block, a user could get Claude to decrypt and print its reasoning. Systems trained this way can inherit capabilities they wouldn’t otherwise have, without inheriting the safeguards that we've built to prevent a broad range of misuse like cyberattacks and weapons development.
This change aims to make distillation campaigns more difficult to execute. It builds on existing anti-distillation measures like enhanced distillation classifiers and restrictions on transferring sessions or reasoning from more advanced models to less capable models with weaker safeguards.
What does this mean for API integrations?
Certain integrations—particularly those that involve rewriting earlier turns mid-conversation, like context compaction and injected system reminders—may need adjustment.
Here are the resources to help guide you through this update:
- The preserved thinking documentation covers where the change does and does not apply.
- The Fable 5.1 migration guide has a full checklist for the necessary updates.
- The Fable 5.1 prompt guide covers behavioral differences and prompting patterns that help you draw on Fable 5.1's full capabilities.
If the guidance above doesn't cover your use case, please reach out to our support team. If you work with an account team, you can also reach out to them for support with updating more complex integrations.
There are additional benefits to keeping thinking blocks consistent: it means that the API can reuse cached prompts more often, which reduces costs and response time.
Who will this impact?
On Fable 5.1, this update applies to new API accounts created after August 31, 2026 12:00:00 AM UTC. Specifically, it affects new Claude Platform organizations, Amazon Bedrock accounts, Google Cloud Vertex AI projects, and Microsoft Azure Foundry projects created on or after August 31, 2026.
We're taking a phased approach to enforcement, starting with new accounts, where we see the highest concentration of distillation-related abuse. Existing accounts won't be affected for Fable 5.1, which gives developers time to make their harnesses and integrations compatible with this update. Preserved thinking will apply to all users for future models.
If you use Claude Code, Claude Cowork, or Claude.ai, there's nothing you need to change; those products handle thinking blocks for you. Models other than Fable 5.1 are not affected.
