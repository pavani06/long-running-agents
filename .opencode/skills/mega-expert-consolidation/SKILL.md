---
name: mega-expert-consolidation
description: "Consolidate multiple specialist agents into one customer-facing mega expert. Phase 1: build one agent per specialty (financing, advisory, buying, insurance, trade-in), each benchmarked against the best individual human expert on EVERY dimension that matters. Phase 2: fuse the certified specialists behind a single unified customer interface with an internal domain classifier and fusion layer — no specialist handoffs, no tier queues, no deflection bot. Use when designing a customer-facing agent that spans multiple expert domains, when specialist teams fragment the customer experience, when deciding between one generalist agent vs many specialists, or when a deflection/support bot is proposed for a complex-sales journey. Triggers: 'mega expert', 'mega-expert', 'specialist consolidation', 'specialist fragmentation', 'deflection bot', 'beat the best human', 'superhuman agent', 'fuse specialist agents', 'unified customer interface', 'single customer-facing agent', 'specialist handoff', 'one agent per specialty', 'benchmark against best human', 'generalist vs specialist agent', 'fragmented customer experience', '15 specialists 15 teams'."
license: MIT
compatibility: opencode
metadata:
  version: 1.0.0
  audience: all-agents
  workflow: agent-architecture
  priority: medium
  source: "Kavak's Playbook for Rebuilding a Company Around AI — analysis 2026-08-30 (pattern classified Missing, integration Medium)"
---

## What I Do

I replace specialist fragmentation and deflection-first automation with a two-phase consolidation contract:

1. **Certify** — one agent per specialty, each independently benchmarked against the best human expert ever hired in that specialty, on every dimension that matters (conversion, CSAT, approval accuracy, quote quality). The bar is superhuman per-domain, not "good enough" (`...-analysis.md:27` — "the bar is outperforming the best human ever hired on every dimension that matters").
2. **Fuse** — only certified specialists enter a fusion layer behind ONE customer-facing agent (the mega expert). The customer never sees a handoff, a queue, or a restart of their story (`...-analysis.md:89` — "first build an agent that beats each individual expert, then fuse them into a single 'mega expert' that faces the customer").

The customer-facing surface is the mega expert alone; specialists become internal organs, consulted by an internal domain classifier. Source problem: "15 specialist teams fragment the customer experience" (`...-patterns.yaml:77`).

## When to Use Me

Load this skill when:

- Designing a customer-facing agent that must span multiple expert domains (financing + advisory + insurance + trade-in in one conversation)
- The current architecture routes customers between specialist teams/agents/queues, and each handoff loses context
- Deciding "one generalist agent vs. many specialist agents" for a complex, multi-domain, long-cycle journey
- A deflection bot or FAQ/support agent is proposed as the customer face for a complex-sales or high-ticket flow
- Setting the acceptance bar for a domain agent: "beat the best human on every dimension" instead of "pass a task eval"
- Merging N existing specialist agents into a single interface without losing per-domain expertise

Do NOT use when:

- The domain is genuinely single-specialty with no cross-domain customer journey — a certified specialist agent alone is enough; fusion adds machinery for nothing
- The "fusion" would merge PROMPTS instead of agents — one dense mega-prompt is the anti-pattern named at `docs/canonical/goal-atomicity-split.md:92` ("Scales agent work by decomposition instead of by dense mega-prompts")
- No per-domain best-human baseline can be measured — without the benchmark harness, "certified" is a claim, not a gate
- The goal is orchestration reliability across independent agents — that is multi-agent fault tolerance, confirmed adjacent-but-different in the classification justification
- The work is physical-world boundary support — see the Sidekick pattern instead

## The Anti-Pattern

```
ANTI-PATTERN: Specialist fragmentation + deflection bot as the customer face.
15 specialists in 15 teams; easy queries get canned replies, everything
else gets routed queue-to-queue with context loss at every hop.

Scenario (source: ...-analysis.md:89, :148, :157):
  Customer asks: "Is this car + this loan right for me, and what's my
  trade-in worth?"
  Deflection bot: FAQ match fails (cross-domain query).
  Router: assigns to "advisory" queue. Customer retells history.
  Advisory agent: "financing question — transferring you."
  Financing team: "we don't see the trade-in quote, restart please."
  15 teams, 15 handoffs, zero full-context answers.

Consequence:
  - Customer experience fragments; context resets at every internal boundary
  - The bar collapses to "good enough on easy problems" — the deflection bot
    (patterns.yaml:157 — "Rejects easy-problem 'good enough' deflection bots")
  - No agent ever owns conversion/LTV; each team owns its own KPI silo
  - Superficial KPIs (calls handled, minutes, deflection count) hide that
    conversion broke (...-analysis.md:160)
```

Wrong code — deflection bot plus specialist handoff queues:

```python
from dataclasses import dataclass

# WRONG: "good enough" deflection first, human-ish escalation second,
# and a customer-visible handoff graph between specialist teams.

@dataclass
class DeflectionBot:
    faq: dict[str, str]

    def handle(self, query: str) -> str | "Escalation":
        if canned := self.faq.get(query.strip().lower()):
            return canned                      # resolves only easy problems
        return self.escalate(query)

    def escalate(self, query: str) -> "Escalation":
        team = "advisory" if "car" in query else "financing"
        return Escalation(queue=team, summary=query[:200])  # truncated context


@dataclass
class Escalation:
    queue: str
    summary: str


@dataclass
class SpecialistTeamHandoff:
    """Each team has its own system, its own KPI, and its own amnesia."""
    current_team: str

    def transfer(self, customer, next_team: str) -> Escalation:
        customer.history = None                # context resets every hop
        return Escalation(queue=next_team, summary="re-qualify customer")

# Failure mode: the customer face IS the routing graph. No single agent is
# accountable for conversion, and no specialist is measured against the
# best human — only against "did the queue drain".
```

## The Pattern

```
Customer ──> [ Mega Expert (single customer-facing interface) ]
                 │  internal domain classifier (no customer-visible routing)
                 ├─> financing specialist  (certified > best human)
                 ├─> advisory specialist   (certified > best human)
                 ├─> buying specialist     (certified > best human)
                 ├─> insurance specialist  (certified > best human)
                 └─> trade-in specialist   (certified > best human)
                 │
                 └─> fusion layer: reconciles opinions under portfolio
                     constraints, emits ONE coherent answer + ONE next action
```

Correct code — specialists with per-domain best-human benchmarks, a classifier, a fusion layer, and one interface:

```python
from dataclasses import dataclass, field
from enum import Enum

# ---- Phase 1: per-specialty certification against the best human ----

@dataclass(frozen=True)
class BenchmarkDimension:
    name: str            # "conversion", "csat", "quote_accuracy", ...
    best_human: float    # baseline from the best human ever hired in-domain
    weight: float = 1.0  # dimensions are all mandatory; weight is for reporting


@dataclass
class SpecialistAgent:
    domain: str                                  # "financing", "trade_in", ...
    dimensions: list[BenchmarkDimension]
    latest_scores: dict[str, float] = field(default_factory=dict)

    def eval_scores(self, run_eval) -> dict[str, float]:
        """run_eval(domain) -> {dimension_name: agent_score}."""
        self.latest_scores = run_eval(self.domain)
        return self.latest_scores

    def min_margin(self) -> float:
        """Weakest margin over the best-human baseline across dimensions."""
        return min(
            self.latest_scores.get(d.name, float("-inf")) - d.best_human
            for d in self.dimensions
        )

    def certified(self, run_eval) -> bool:
        self.eval_scores(run_eval)
        # ALL dimensions, not an average: superhuman means no regression
        # on any dimension that matters (...-analysis.md:27).
        return self.min_margin() >= 0.0


# ---- Internal routing: the classifier never faces the customer ----

class DomainClassifier:
    """Maps one customer turn to the specialist domains it touches.
    Cross-domain turns are normal (car + loan + trade-in in one sentence)."""

    def __init__(self, domains: list[str]):
        self.domains = domains

    def involved(self, customer_query: str, context: "CustomerContext") -> list[str]:
        # deterministic rule-based first version; learned later if needed
        hits = [d for d in self.domains if self._mentions(d, customer_query, context)]
        return hits or ["advisory"]  # default organ, not a human queue

    def _mentions(self, domain: str, query: str, context) -> bool:
        keywords = {
            "financing": ["loan", "rate", "payment", "apr", "credit"],
            "advisory": ["car", "model", "fit", "recommend"],
            "buying": ["price", "discount", "stock", "deliver"],
            "insurance": ["coverage", "policy", "warranty"],
            "trade_in": ["trade", "trade-in", "my car worth"],
        }
        return any(k in query.lower() for k in keywords.get(domain, []))


# ---- Phase 2: fusion behind ONE customer-facing agent ----

@dataclass
class CustomerContext:
    customer_id: str
    history: list[str] = field(default_factory=list)
    portfolio_constraints: dict[str, float] = field(default_factory=dict)


@dataclass
class SpecialistOpinion:
    domain: str
    answer_fragment: str
    confidence: float
    portfolio_impact: float   # e.g. risk delta for the lending portfolio


@dataclass
class MegaExpertReply:
    answer: str                # ONE coherent answer, fused
    next_action: str           # ONE next action, fused
    contributing_domains: list[str]


class FusionPolicy(Enum):
    HIGHEST_CONFIDENCE = "highest_confidence"
    PORTFOLIO_CONSTRAINED = "portfolio_constrained"  # default: per-customer
    # optimization bounded by portfolio health (...-analysis.md:115)


class UncertifiedFusionError(RuntimeError):
    """Raised when fusion is attempted without a fully certified roster."""


@dataclass
class MegaExpert:
    """The ONLY object the customer talks to. Specialists are internal.

    Construction goes ONLY through MegaExpert.from_certified(): the
    certification is machinery, not a promise. A MegaExpert without a
    complete certified roster cannot exist (and handle() re-checks).
    """
    specialists: dict[str, SpecialistAgent]
    certified_domains: frozenset[str]      # proof: every domain beat best human
    classifier: DomainClassifier
    policy: FusionPolicy = FusionPolicy.PORTFOLIO_CONSTRAINED

    @classmethod
    def from_certified(cls, specialists: dict[str, SpecialistAgent],
                       run_eval, classifier: DomainClassifier,
                       policy: FusionPolicy = FusionPolicy.PORTFOLIO_CONSTRAINED,
                       ) -> "MegaExpert":
        # Fusion gate: every organ beat the best human first — proven now.
        failed = sorted(d for d, s in specialists.items()
                        if not s.certified(run_eval))
        if failed:
            raise UncertifiedFusionError(f"uncertified specialties: {failed}")
        return cls(specialists=specialists,
                   certified_domains=frozenset(specialists),
                   classifier=classifier, policy=policy)

    def _gate(self, domain: str) -> None:
        if domain not in self.certified_domains:
            raise UncertifiedFusionError(f"domain not certified: {domain}")

    def consult(self, domain: str, query: str, ctx: CustomerContext
                ) -> SpecialistOpinion:
        self._gate(domain)
        # thin adapters over the specialist agent's tool/API surface
        return SpecialistOpinion(
            domain=domain,
            answer_fragment=self._infer(domain, query, ctx),
            confidence=self._score(domain, query, ctx),
            portfolio_impact=self._risk_delta(domain, ctx),
        )

    def handle(self, customer_query: str, ctx: CustomerContext) -> MegaExpertReply:
        if len(self.certified_domains) != len(self.specialists):
            raise UncertifiedFusionError("roster incomplete: rebuild via from_certified")
        domains = self.classifier.involved(customer_query, ctx)
        opinions = [self.consult(d, customer_query, ctx) for d in domains]
        chosen = self._fuse(opinions, ctx)
        return MegaExpertReply(
            answer=self._compose(chosen),
            next_action=self._next_action(chosen, ctx),
            contributing_domains=[o.domain for o in chosen],
        )

    def _fuse(self, opinions: list[SpecialistOpinion],
              ctx: CustomerContext) -> list[SpecialistOpinion]:
        if self.policy is FusionPolicy.HIGHEST_CONFIDENCE:
            return [max(opinions, key=lambda o: o.confidence)]
        # PORTFOLIO_CONSTRAINED: drop opinions that breach portfolio limits,
        # then keep the highest-confidence survivor per domain.
        viable = [
            o for o in opinions
            if o.portfolio_impact <= ctx.portfolio_constraints.get(o.domain, float("inf"))
        ]
        return viable or opinions  # never bounce the customer to a queue

    def _score(self, domain: str, query: str, ctx: CustomerContext) -> float:
        self._gate(domain)
        # confidence = weakest live margin over the best-human baseline
        return self.specialists[domain].min_margin()

    def _compose(self, opinions: list[SpecialistOpinion]) -> str:
        ranked = sorted(opinions, key=lambda o: -o.confidence)
        return " ".join(o.answer_fragment for o in ranked)

    def _next_action(self, opinions: list[SpecialistOpinion],
                     ctx: CustomerContext) -> str:
        lead = max(opinions, key=lambda o: o.confidence)
        return f"propose via {lead.domain}: {lead.answer_fragment}"

    def _infer(self, domain: str, query: str, ctx: CustomerContext) -> str:
        # adapter: in production, calls the specialist agent's inference
        # endpoint with the FULL customer history, never a truncated summary
        return f"[{domain}] draft for {query!r} over {len(ctx.history)} turns"

    def _risk_delta(self, domain: str, ctx: CustomerContext) -> float:
        # adapter: in production, reads the pricing/risk API
        return ctx.portfolio_constraints.get(f"{domain}_risk_delta", 0.0)

# Contract: customer -> MegaExpert.handle(). There is no other public entry
# point, no queue type, and no handoff object anywhere in the customer path.
```

The mega expert is a fusion of **agents**, each keeping its own eval surface — not a single dense prompt. The classifier routes intents internally at outcome granularity (one outcome per intent stays intact, per `docs/canonical/goal-atomicity-split.md:92`).

## Implementation Rules

**Classifier rules**

1. The domain classifier is INTERNAL. Any routing the customer can perceive (transfers, "let me connect you", queue positions) is a defect of this pattern.
2. One turn may involve multiple domains — return a list, never force a single queue.
3. Start rule-based and deterministic; only learn the classifier if rule-based routing measurably fails in evals.

**Benchmark harness rules**

4. Per specialty, enumerate EVERY dimension that matters to the business outcome (conversion, LTV, CSAT, quote accuracy) — source: `...-analysis.md:27`. Missing a dimension means the certification is incomplete, not passed.
5. The baseline is the best human ever hired in that domain, not the average team member and not last quarter's bot.
6. Certification is `all(dimensions)`, never a weighted average. A specialist that wins conversion but loses CSAT is not certified.
7. Re-run the full harness on every model change — the fusion is only as certified as its weakest current model.

**Fusion sequencing rules**

8. Sequence is fixed: certify EVERY specialist first, then fuse. Fusing before certification locks the customer face onto unproven organs.
9. `MegaExpert.certified()` must hold in CI before the fused interface ships or re-ships.
10. The fusion layer must reconcile under portfolio constraints (per-customer optimization bounded by portfolio health, `...-analysis.md:115`) and emit exactly ONE answer and ONE next action per turn.
11. Specialists never talk to the customer and never talk to each other as a substitute for fusion — peer handoff graphs are the fragmentation this pattern deletes.
12. Cross-domain misses found in production become regression cases on the FUSED agent (the fusion layer is what failed), not only on the specialist.

## Integration With This Repo

This pattern was classified **Missing** with **integration_value: Medium** — "NOT_FOUND in any form (doc, code, skill, or curriculum). The mechanism — one agent per specialty benchmarked against the best individual human, then fused into a single customer-facing mega expert — has no coverage" (`...-classification.yaml:326-328`, entry "Mega-Expert Consolidation"). This skill is the first artifact covering it. Connection points:

- **`docs/canonical/persona-based-documentation.md:23`** — "When a team has specialists in different domains, their expertise is not systematically captured in durable documentation surfaces that agents can load." The classification reads this as "specialists as documentation sources, not as agents to fuse" (`...-classification-batch-2.md:70`). Integration: persona NFR docs are the training/eval material each `SpecialistAgent` loads; this skill consumes that capture step and adds the missing agent-fusion half.
- **`docs/canonical/goal-atomicity-split.md:92`** — "Scales agent work by decomposition instead of by dense mega-prompts -- one outcome per intent". Guardrail for this skill: fusion happens between certified agents with an intent-granularity classifier, never by merging prompts into one dense mega-prompt (the only prior "mega" usage in canonical, per `...-classification-batch-2.md:71`).
- **`docs/system-of-record.md:172-299`** — active canonical table has no consolidation/fusion entry (confirmed in the classification justification); **`docs/system-of-record.md:33-65`** — skills table had no consolidation skill. This skill fills both rows when registered.
- **`curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md:719`** — "OBJETIVO: Construir relacionamento de longo prazo." The KODA customer journey is the concrete case: a single customer-facing agent spanning the full sales journey, which batch-2 flags as the integration target ("relevant to the KODA case... and to Level 4 / multi-agent coordination content as a design rationale (unified expert vs. specialist fragmentation with handoffs)", `...-classification-batch-2.md:74`).
- Adjacent-but-different patterns confirmed in the classification justification (do not conflate): multi-agent fault tolerance (orchestration reliability) and split-brain planning review (separate rubrics).

## Quality Gates

- [ ] Every specialty has a `SpecialistAgent` with enumerated `BenchmarkDimension`s covering every business dimension; no dimension without a `best_human` baseline
- [ ] Certification is MACHINERY, not a promise: `MegaExpert` is constructible only via `MegaExpert.from_certified(...)`; direct construction without a fully certified roster raises `UncertifiedFusionError`, and `handle()` re-checks the roster before every reply
- [ ] `certified()` gate implemented per specialist and on the fused `MegaExpert`; CI blocks shipping the interface when any specialist regresses below best-human on ANY dimension
- [ ] Benchmark harness re-runs on model change (full re-certification, weakest-model rule)
- [ ] Exactly ONE public entry point in the customer path (`handle`); grep the customer-facing module for queue/transfer/handoff types — must return zero matches
- [ ] Classifier returns multi-domain lists for cross-domain turns; no forced single-queue fallback to humans
- [ ] Fusion emits exactly one answer and one next action per turn, reconciled under `portfolio_constraints`
- [ ] Success metric is the business outcome (conversion, LTV, CSAT), not call counts or deflection volume — "measuring number of calls or minutes on call gives signal without truth" (`...-analysis.md:160`)
- [ ] Production cross-domain failures become regression cases against the fused agent
- [ ] No prompt-merging shortcut: fusion composes outputs of certified agents; the dense mega-prompt anti-pattern is checked against `docs/canonical/goal-atomicity-split.md:92`

## References

- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:27` — superhuman bar: "outperforming the best human ever hired on every dimension that matters (conversion, LTV, customer experience)"
- `...-analysis.md:89` — the pattern statement: ~15 specialists in 15 teams; "first build an agent that beats each individual expert, then fuse them into a single 'mega expert' that faces the customer"
- `...-analysis.md:115` — portfolio constraints bounding per-customer personalization
- `...-analysis.md:126` — outcome evidence: sales agents (not support agents) delivered tripled NPS/CSAT and 2.1x conversion
- `...-analysis.md:148` — architecture selector: superhuman bar builds mega-expert, "good enough" bar builds deflection bot
- `...-analysis.md:157`, `:160` — failure modes: ChatGPT bolt-on trap; superficial KPI measurement
- `...-patterns.yaml:77-78` — problem/mechanism pair for the pattern entry
- `...-patterns.yaml:156-157` — benefit/cost: mega-expert architectures vs. rejected deflection bots
- `...-classification.yaml:315-335` — entry "Mega-Expert Consolidation": classification Missing, integration_value Medium, evidence `docs/canonical/persona-based-documentation.md:23` and `docs/canonical/goal-atomicity-split.md:92`, NOT_FOUND justification with searched locations
- `...-classification-batch-2.md:70-74` — specialist-docs-not-agent-fusion reading; only-"mega"-usage check; KODA/Level-4 integration rationale
- `docs/system-of-record.md:33-65` (skills table), `:172-299` (canonical table) — absence of prior coverage, per the classification justification
- `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md:719` — KODA long-term relationship objective (cited in the same classification file, entry "Agent-Per-Customer with Persistent Cross-Channel Memory")
