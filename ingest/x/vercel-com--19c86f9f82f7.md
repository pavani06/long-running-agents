---
url: "https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway"
key: "19c86f9f82f7"
status: "ok"
final_url: "https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway"
method: "trafilatura"
content_hash: "d63b051f82017ec1f4d205476b29038a9b9f9111"
text_len: 2444
fetched: "2026-09-18"
---

Jev from TypeSafe AI is now available on AI Gateway.
Jev is a probabilistic decision model for software: state goes in, typed Choice, Score, and Boolean answers come out.
Regular language models generate text one token at a time, which the application then parses and validates. Jev evaluates all declared questions in parallel and returns typed answers plus probabilities directly. That removes unnecessary text generation and makes it straightforward to automate clear cases while routing uncertain ones to review.
TypeSafe reports Jev was up to 193.6x faster and 444.6x cheaper than LLMs on its workflow evaluations. Example use cases include:
- Choosing the next tool or subagent in an agent loop
- Deciding whether to continue, retry, ask the user, or stop
- Scoring urgency or risk before an action
- Verifying model outputs and enforcing guardrails.
AI SDK 7 exposes Jev through the experimental evaluate API. Choice selects an option, Score grades an ordered rubric, and Boolean estimates the probability of true. Install the current AI SDK (AI SDK 7.0.105 onwards supports the evaluate API):
pnpm add ai@latest
Each evaluation specifies:
- model : the evaluation model to call,
- state : the shared string, object, or array to evaluate, and
- questions : a map of named decisions to make about that state.
Call the model with typesafe-ai/jev. This example turns one support case into a queue, priority, and refund-review decision, with uncertain routing sent for manual review:
import { experimental_evaluate as evaluate } from 'ai';
const result = await evaluate({  model: 'typesafe-ai/jev',  state: 'The support agent issued a full refund to the customer.',  questions: {    refunded: {      type: 'boolean',      instructions: 'Was a refund issued?',    },  },  providerOptions: {    gateway: { zeroDataRetention: true },  },});
console.log(result.answers.refunded);
The result preserves question IDs and Choice keys. TypeSafe reports separate Choice and Score confidence in result.providerMetadata.typesafe.confidence. Calibrate probabilities and confidence against labeled examples from your workflow.
Jev supports Zero Data Retention and No Training, enabled per request in the example. Evaluation calls also appear in logs and custom reporting, count toward budgets, and accept other Gateway provider options in the same providerOptions.gateway object.
Read the documentation on evaluation models on AI Gateway for more details.
