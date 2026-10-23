# Output writing contract

Use this single authority when drafting or revising human-readable CLI/chat
explanations, change summaries, progress/validation reports, OpenSpec, README,
tutorials, documentation, Issue/PR text, and questions asking the user to decide.

## Language and authority

Default to **Traditional Chinese** for human-facing prose, including text drafted
by Luna or other models. An explicit user language request or the selected
project's required document language takes precedence. Keep skill instructions
and management templates in English. Preserve identifiers, commands, code,
raw logs, JSON, status codes, units, and normative schema terms verbatim;
explain them beside the original when needed.

Assume basic software-engineering knowledge and no familiarity with this change.
Help the reader understand the behavior, reason, impact, and evidence limits.
Requirements and acceptance come from approved OpenSpec; implementation claims
come from the actual diff, source, tests, and raw evidence. Preserve existing
PR/Issue templates, diagrams, checklist states, lifecycle gates, and publication
authorization. Ordinary CLI answers need only the structure their question needs.

Source location: docs/output.md. Installed location:
.agents/workflow-kit/docs/output.md. Resolve through workflow project context.
Standalone skill copies need this resource and a valid pointer to it.

## Draft, inspect, revise

1. Identify the reader, document purpose, and what they must understand or do
   from confirmed context. Ask only about missing information that affects the
   content; reuse settled answers.
2. Choose the applicable format below, retain its template, and draft. For long
   content, lead with the conclusion, reason, and necessary action; follow with
   mechanisms, details, and evidence. Put limitations that change a decision
   beside that decision. Short answers can stay short.
3. Read as a newcomer, repair the concrete problems below, and compare the
   revision with the governing spec, diff, or source. Finish when purpose,
   rationale, applicable actions, and supporting evidence are findable and all
   material conditions, exceptions, and unknowns remain explicit. Report gaps.

The agent performs this process without CLM or an external scoring service.
These instructions alone establish neither model-specific quality nor reader
comprehension. When a substantial rewrite or unfamiliar tone needs a concrete
example, read [Traditional Chinese examples](output-examples.zh-TW.md).

## Decision questions

Apply this contract to chat questions and question-tool titles/options alike.
Before a consequential question, explain its purpose and give one relevant
example. Ask one unresolved decision with 2-3 distinguishable options, an explicit
recommendation with tradeoffs, and optional free-text notes/alternatives. Use
plain language; explain unfamiliar terms before asking the reader to choose.
Follow the interview's existing facet/count limits and save its answer. Reuse
settled answers and existing authorization; a clearer layout is not a new
approval gate. Keep meaningful uncertainty rather than forcing a false choice.

## Meaning and cohesion

- **Terminology:** explain the situation and purpose before introducing an
  unfamiliar term. Keep a stable name for each concept; retain technical names
  where the reader needs them to navigate code or operate the system.
- **Continuity:** build from the previous sentence's subject or result, then add
  new information. Make causal, temporal, and conditional relationships explicit;
  name ambiguous referents. Explain why a topic change matters. Use parallel
  phrasing for parallel ideas and natural repetition of key terms.
- **Rationale:** connect the observed problem or trigger, the actual change, and
  its user/reviewer impact. Name who does what under which conditions. Separate
  observations from suspected causes and expected benefits from measured results.
- **Evidence:** connect each conclusion to accessible evidence and its scope.
  Distinguish tests added, tests run, CI passed, human acceptance, and reviewer
  approval. For failure, explain what remains unproven, its delivery impact, and
  the next action. Label unsupported technical claims [Needs Verification].

## Layered presentation

Use coherent paragraphs with one developed point each. Keep required context
near the claim. Use tables for genuine comparisons or mappings, numbered steps
for ordered actions, and diagrams when they clarify relationships or data flow.
Replace wide tables or paragraph-sized cells with sections. Use descriptive
headings, sparse emphasis, parallel list items, and shallow nesting; avoid
fragmenting connected reasoning into isolated sentences or repeating summaries.

Put long evidence in later sections, supported details blocks, or descriptive
links. In terminals without folding, use a short explanation plus a document
link. Keep paths and commands copyable, label code blocks by language, and inspect
long rendered output in the available interface. Preserve necessary complexity;
shorter text is not automatically easier to understand.

## Format-specific focus

| Output | Reader's immediate need | Supporting content as applicable |
|---|---|---|
| CLI: what a change does | Improved situation and behavior | Reason, key flow, delivered scope |
| CLI: progress/results | Verified result and remaining work | Evidence, limits, actionable next step |
| OpenSpec | Situation, required behavior, acceptance | Boundaries, exceptions, design rationale, unresolved decisions; preserve schema and normative terms |
| README | Purpose, audience, quickest valid entry | Prerequisites, setup/use, success checks, limitations, detailed links |
| Tutorial/documentation | Learning goal or task | Ordered actions, checkable examples, expected results, failures and recovery |
| Issue | Observable problem and impact | Reproduction, expected behavior, acceptance, unconfirmed assumptions |
| PR | Actual behavior change and rationale | Reading entry, flow, dependencies, validation and acceptance status |

Write unadopted Issue alternatives as proposals. Describe the final PR diff;
keep intended outcomes distinct from delivered behavior.

## Nine article practices, adapted

Select by purpose; these are not nine mandatory sections or a scoring gate.

| Article practice | Engineering application |
|---|---|
| Reader relevance | Answer the current reader's question or task |
| Keyword research | Use searchable feature names and established terms; routine engineering prose needs no separate SEO work |
| Outline | Arrange necessary information within the existing template |
| Opening | State the problem, result, or purpose with factual value |
| Images | Add a diagram, screenshot, or example when it explains the task |
| Heading tags | Use meaningful heading levels in long documents; short answers need no forced headings |
| Internal/external links | Connect specs, related instructions, and primary evidence |
| Conclusion | Resolve a long discussion when useful; avoid repeating a short answer |
| Call to action | State a real next action or review focus without adding approval gates |

## Delivery check

Before delivery, revise until:

- The opening answers the current question; the reader and purpose are clear.
- Terms, referents, sentence relationships, paragraph focus, and change rationale
  can be followed without guessing or unsupported causal claims.
- Format-specific needs are covered: instructions include success checks,
  specifications retain testable acceptance, and PRs retain their approved layout.
- The reader can grasp the result before looking up details; layout avoids
  excessive emphasis, fragmented paragraphs, and unreadable tables.
- Rewriting preserves meaning, identifiers, commands, quantities, exceptions,
  diagram relationships, checkboxes, and actual verification/acceptance states.

This check supports writing; tests, code review, and human acceptance retain
separate responsibilities. Structural checks and working links do not prove
understanding. Assess effectiveness using real drafts and reader feedback,
including whether readers can explain the purpose, flow, and evidence.

## Sources and limits

[GMU: Cohesion and Coherence](https://writingcenter.gmu.edu/writing-resources/general-writing-practices/cohesion-and-coherence)
informs continuity, referents, parallel phrasing, and familiar-to-new information.
[AI Hero: Writing for Agents](https://www.aihero.dev/skills-writing-for-agents)
informs concise instructions, explicit pointers, conditional references, and
completion criteria; its reader is the agent. Human-facing language/layout rules
come from user-confirmed requirements and are a separate application.
[Nine article practices](https://notonlyblogger.com/how-to-write-the-perfect-blog-post/)
inform the adapted table, not universal engineering or SEO requirements.
