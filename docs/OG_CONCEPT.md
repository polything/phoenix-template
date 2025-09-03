# Content Pipeline / An **Autonomous Research-to-Publish System (with Prompts)**

*A guide written by [Harald Roine](https://www.linkedin.com/in/haraldroine/), CEO @ Buro Ventures*

[*👉 Learn how I can help you grow your B2B business.*](https://www.notion.so/23f90859d2b8801398d9cf840d022ee2?pvs=21)

### Objective

Create an end-to-end, largely autonomous content pipeline that transforms minimal client inputs into high-quality lead magnets, guides, posts, and emails tailored to the client’s service offering and audience. The pipeline includes deep market research, angle and asset generation, review gates, packaging per channel, and closed-loop learning via performance analytics.

### What this document contains

- Canonical definitions and variables used across prompts
- Required client inputs (the only manual inputs needed to run the pipeline)
- The full flow (stages, goals, inputs, outputs)
- Reusable prompts for each stage with variable placeholders and output contracts (schemas)
- Guardrails: style transfer, fact-check, compliance, claims policy, and self-critique
- Analytics loop: experimentation and continuous learning

---

## 1) Canonical definitions and variables

### 1.1 Glossary

- CLIENT: The company/person using this pipeline
- ICP: Ideal Customer Profile for the CLIENT’s offer
- OFFER: The CLIENT’s productized service(s) with positioning, price anchors, proof
- RESOURCE: Lead magnet/guide/assessment/checklist/tool produced to attract and nurture leads
- ANGLE: A specific narrative/perspective framing pain→solution→proof→CTA
- ASSET: Any content unit (post, email, landing page, guide, ad creative)
- PLATFORM: Distribution channel (LinkedIn, X, Email, Blog, YouTube community, etc.)
- VOICE PROFILE: Style baseline capturing tone, diction, cadence, and do/don’t rules
- CLAIM: Statement about outcomes/benefits that must be supported by proof or guarded language

### 1.2 Global dynamic variables

These variables are used by prompts throughout the pipeline.

```
{client_name}
{client_domain}
{client_summary}                # 1–3 paragraphs describing the client/company
{service_offering}              # Primary service(s) sold; include scope & exclusions
{target_markets}                # Industries/segments/geos served
{icp_profile}                   # Role(s), firmographics, psychographics, buying triggers
{differentiation}               # Why the client wins / unique wedges
{positioning_statement}         # “For X who need Y, we do Z better because …”
{proof_assets}                  # Links to case studies, testimonials, data, demos
{constraints}                   # Legal, claims, compliance constraints
{brand_tone}                    # Tone adjectives (e.g., precise, candid, credible)
{voice_examples}                # 2–5 canonical writing samples by the client
{priority_outcomes}             # What success means (MQLs, demos, replies, signups)
{priority_platforms}            # e.g., LinkedIn + Email; order by priority
{resource_themes}               # Initial ideas for lead magnets/tools/assessments
{competitor_list}               # 3–10 main competitors or alternates
{keywords_seed}                 # Optional SEO heads/long-tails
{region_policy}                 # Regional constraints (e.g., GDPR, US-only claims)
{banned_topics}                 # Topics to avoid
{content_cadence}               # Desired publishing cadence & mix (e.g., 3 posts/wk, 1 email/wk)

```

### 1.3 Output contract patterns

To make the pipeline composable, most prompts return JSON (plus optional prose). Common envelopes:

```
{
  "summary": string,
  "items": [ ... ],
  "risks": [ ... ],
  "references": [ { "title": string, "url": string, "note": string } ],
  "next_actions": [ ... ]
}

```

---

## 2) Required client inputs (single intake)

Provide once; the system reuses across the pipeline.

```
client_name
client_domain
client_summary
service_offering
target_markets
icp_profile
differentiation
positioning_statement
proof_assets
constraints
brand_tone
voice_examples (2–5 links or pasted text)
priority_outcomes
priority_platforms
resource_themes (initial)
competitor_list
keywords_seed (optional)
region_policy
banned_topics
content_cadence

```

---

## 3) System flow overview

### Stages

1. Intake → Canonical Brief
2. Market Recon (web/forums/reddit/news/competitors)
3. Pain/Jobs Synthesis & Opportunity Map
4. Resource Strategy (lead magnets/tools/assessments)
5. Angle Matrix & Campaign Themes
6. Content Ideation (asset backlog)
7. Outline Generation
8. Draft Generation
9. Voice & Style Transfer
10. Fact-check & Citation Pass
11. Compliance & Claims Guardrails
12. SEO/Structure Optimization (when relevant)
13. Channel Packaging (LinkedIn/X/Email/Blog)
14. Review & Approval (human-in-the-loop)
15. Scheduling & Publishing
16. Experiment Setup (A/B or Bandit)
17. Analytics & KPI Ingestion
18. Learning Loop (update Voice/Angles/Resources)

---

## 4) Prompts and procedures by stage

> All prompts are templates: replace {variables}. Maintain the requested output schemas for reliable automation.
> 

### 4.1 Canonical Brief Builder

Goal: Normalize the client’s intake into a single brief used by all downstream steps.

Prompt (System):

```
You are a senior content strategist. You will build a canonical brief from the inputs.
Return strictly in JSON with fields: summary, offering, icp, positioning, differentiation, constraints, tone, proof, goals, platforms.
```

Prompt (User):

```
Client Name: {client_name}
Domain: {client_domain}
Summary: {client_summary}
Service Offering: {service_offering}
ICP: {icp_profile}
Positioning: {positioning_statement}
Differentiation: {differentiation}
Constraints: {constraints}
Brand Tone: {brand_tone}
Proof Assets: {proof_assets}
Priority Outcomes: {priority_outcomes}
Priority Platforms: {priority_platforms}

```

Expected JSON:

```
{
  "summary": string,
  "offering": string,
  "icp": string,
  "positioning": string,
  "differentiation": string,
  "constraints": [string],
  "tone": [string],
  "proof": [ {"title": string, "url": string } ],
  "goals": [string],
  "platforms": [string]
}

```

### 4.2 Deep Market Recon (web + reddit + forums + news)

Goal: Map market sentiment, pains, JTBDs, triggers, language, and objections with sufficient depth that downstream strategy does not require additional manual research.

Method: Perform structured desk research across credible publications, industry blogs, conference talks, product review sites, community forums, and especially reddit threads where practitioners discuss real problems. Extract both quantitative signals (frequency/severity/recency) and qualitative quotes (verbatim language). Include contradictory viewpoints and acknowledge uncertainty where evidence is weak. Prefer primary sources over listicles, and avoid speculation.

Prompt (System):

```
You are a senior research analyst. Mine credible web sources, reddit threads, industry forums, Q&A sites, product review sites, and recent news.
Follow these rules:
1) For each insight/pain, include a short evidence note and a direct link. Whenever possible, include a short verbatim quote (<=200 chars) capturing the audience’s language.
2) Quantify where possible: assign severity (1-5) and frequency (1-5) based on the corpus you see; include a brief rationale.
3) Capture contradictory viewpoints and note uncertainty explicitly; do not invent facts.
4) Prefer sources within the last 18 months; include older seminal sources only if still authoritative.
5) Include emerging triggers (regulatory, economic, platform changes) that explain “why now”.
6) Avoid marketing fluff; use practitioner language.

Return strictly in JSON with keys: insights, pains, JTBDs, triggers, keywords, objections, references. Keep it machine-parseable.

```

Prompt (User):

```
Client & Offering Context: {client_summary} | {service_offering}
ICP Context: {icp_profile}
Seed Keywords (optional): {keywords_seed}
Competitors to include: {competitor_list}
Exclude topics: {banned_topics}
Region policy: {region_policy}

```

Expected JSON:

```
{
  "insights": [ {"statement": string, "evidence": string, "source_url": string} ],
  "pains": [ {"pain": string, "who": string, "impact": string, "source_url": string} ],
  "JTBDs": [ {"job": string, "success_metric": string} ],
  "triggers": [ {"event": string, "why_now": string} ],
  "keywords": [string],
  "objections": [ {"objection": string, "likely_from": string} ],
  "references": [ {"title": string, "url": string, "note": string} ]
}

```

### 4.3 Synthesis & Opportunity Map

Goal: Convert raw research into prioritized opportunities that align to OFFER fit and likelihood of impact.

Method: Cluster pains and jobs into coherent opportunity areas. Score opportunities with a transparent formula and explain the reasoning so a reader can audit the decision. Connect opportunities to value hypotheses that the client can credibly deliver.

Prompt (System):

```
Synthesize the research into an opportunity map aligned to the client’s offering.
For each opportunity cluster, compute a priority score using this formula (1-5 scale for each factor):
PRIORITY = severity * frequency * revenue_impact * offer_fit
Include the component scores and a 1-2 sentence rationale.
Return JSON fields: themes, opportunity_clusters (with scores and rationale), suggested_resources, risks, references.
Use research data only; do not assume capabilities beyond the provided OFFER.

```

Prompt (User):

```
Client: {client_name}
Offering: {service_offering}
Research JSON:
{research_json}

```

Expected JSON:

```
{
  "themes": [string],
  "opportunity_clusters": [
    {"name": string, "pains": [string], "icp_segment": string, "value_hypothesis": string, "prioritization": "high|med|low"}
  ],
  "suggested_resources": [ {"title": string, "type": string, "angle": string} ],
  "risks": [string],
  "references": [ {"title": string, "url": string} ]
}

```

### 4.4 Resource Strategy (Lead Magnets/Tools/Assessments)

Goal: Define concrete resources aligned to high-priority opportunity clusters that genuinely solve a piece of the ICP’s problem and create a clean bridge to the OFFER.

Method: For each resource, specify the promise, the outline, the minimal data needed to personalize or score, and the delivery format. Ensure no “bait-and-switch”: the resource must stand alone as useful. List how the resource will capture consent (form fields) and what qualifies as an MQL versus a simple subscriber. Include validation questions to confirm fit.

Prompt (System):

```
Design a resource strategy of 3–6 assets (lead magnets, assessments, tools, checklists) that solve high-priority pains without bait-and-switch.
For each resource include: title, type, target ICP subsegment, explicit promise, outline (sections), data_required (for personalization/scoring), delivery format, CTA ladder (from low-friction to sales), form_fields (with required/optional), mql_criteria, and 2 validation questions that ensure the user is a fit.
Return JSON only; be concrete and avoid genericities.

```

Prompt (User):

```
Client: {client_name}
Offering: {service_offering}
Opportunity Map JSON:
{opportunity_json}
Existing Resource Themes: {resource_themes}
Constraints: {constraints}

```

Expected JSON:

```
{
  "resources": [
    {
      "title": string,
      "type": "guide|tool|assessment|checklist|template",
      "target_icp": string,
      "promise": string,
      "outline": [string],
      "data_required": [string],
      "delivery": "pdf|notion|sheet|webapp",
      "cta_ladder": ["subscribe", "book_call", "start_trial"]
    }
  ]
}

```

### 4.5 Angle Matrix & Campaign Themes

Goal: Generate angles mapped to pains/JTBDs with proofs and CTAs that match funnel stage and platform norms.

Method: Create angles using varied hook styles (data-led, contrarian, story, step-by-step, mistake-to-avoid, teardown). For each angle, define the narrative arc, specify proof types (case data, 3rd‑party stat, demo), objections to preempt, and an appropriate CTA (subscribe, download, reply, book). Map platform fit and note any platform-specific adjustments.

Prompt (System):

```
Create an Angle Matrix tied to ICP pains and resource promises.
Each angle must include: name, hook (clearly labeled style: data|contrarian|story|how-to|mistake|teardown), narrative (3-5 sentences), proof (list of verifiable items), objection-handling (1-2 key objections with rebuttal), CTA (funnel appropriate), and platform_fit (LinkedIn/X/Email/Blog) with notes.
Return JSON only.

```

Prompt (User):

```
Client: {client_name}
ICP: {icp_profile}
Resources JSON:
{resources_json}
Proof Assets: {proof_assets}
Tone: {brand_tone}
Priority Platforms: {priority_platforms}

```

Expected JSON:

```
{
  "angles": [
    {
      "name": string,
      "hook": string,
      "narrative": string,
      "proof": [string],
      "objection": string,
      "cta": string,
      "platform_fit": ["LinkedIn","X","Email","Blog"]
    }
  ]
}

```

### 4.6 Content Ideation (Backlog)

Goal: Produce a backlog of assets per angle and platform with a clear purpose, effort estimate, owner, and acceptance criteria.

Method: For each angle and platform, propose specific assets with working titles, objectives, talking points, and add operational metadata: effort_estimate (S/M/L), owner_role (writer|designer|engineer), priority_score (1-100 from angle priority and business goals), measurement_plan (primary/secondary metrics and guardrails), and acceptance_criteria (what must be true to mark as done).

Prompt (System):

```
Generate a backlog of content assets per angle and platform.
For each item produce: type, working title, target ICP, platform, objective metric (CTR|Replies|MQLs|Signups), key talking points, priority_score (1-100), effort_estimate (S|M|L), owner_role, measurement_plan (primary, secondary, guardrails), and acceptance_criteria.
Return JSON only.

```

Prompt (User):

```
Angles JSON:
{angles_json}
Cadence: {content_cadence}
Outcomes: {priority_outcomes}

```

Expected JSON:

```
{
  "backlog": [
    {
      "type": "post|email|thread|blog|landing|ad",
      "title": string,
      "platform": "LinkedIn|X|Email|Blog",
      "target_icp": string,
      "objective": "CTR|Replies|MQLs|Signups",
      "talking_points": [string],
      "angle_ref": string,
      "priority_score": number,
      "effort_estimate": "S|M|L",
      "owner_role": "writer|designer|engineer",
      "measurement_plan": {"primary": string, "secondary": string, "guardrails": [string]},
      "acceptance_criteria": [string]
    }
  ]
}

```

### 4.7 Outline Generation

Goal: Create structured outlines before drafting that are tailored to the asset type and platform, including word-count guidance and section purposes.

Method: Use asset-type templates:

- LinkedIn post: Hook (≤2 lines), Context, Proof/Example, Lesson, CTA.
- X thread: Hook tweet, 5–10 body tweets each with 1 idea, Close CTA.
- Email: Subject options (3), Preheader, Opening pattern (problem/promise), Body sections (story or steps), CTA, P.S.
- Blog: H1, Intro (pain+promise), H2 sections with bullets/examples, Summary/Checklist, CTA.

Prompt (System):

```
Create a concise, logical outline tailored to the asset type and platform using appropriate structure templates.
For each section, state its purpose and suggested word count range. Include an explicit CTA.
Return JSON only.

```

Prompt (User):

```
Asset Brief:
{"title": "{title}", "type": "{type}", "platform": "{platform}", "talking_points": {talking_points}, "angle": {angle_json}}
Voice Examples: {voice_examples}
Tone: {brand_tone}

```

Expected JSON:

```
{
  "outline": [ {"heading": string, "purpose": string, "word_count": string, "bullets": [string] } ],
  "cta": string
}

```

### 4.8 Draft Generation

Goal: Produce first-pass drafts faithful to outline and angle that read clearly, avoid empty filler, and include concrete examples.

Method: Write at a target reading level (Grade 7–9 unless otherwise specified). Prefer short sentences, active voice, and concrete specifics. Insert examples, numbers, or mini-teardowns where appropriate. Avoid superlatives without proof. Preserve structure and headings from the outline. Mark places where citations are implied with [REF: n].

Prompt (System):

```
Write a first draft strictly following the outline structure and angle intent.
Constraints:
- Reading level: Grade 7–9 unless domain requires higher.
- Short sentences, active voice, specific examples.
- No vague hype; qualify any claim and prefer numbers.
Return in Markdown. Include [REF: n] markers where a citation is implied.

```

Prompt (User):

```
Outline JSON:
{outline_json}
Angle Excerpt:
{angle_excerpt}
Platform: {platform}
Tone: {brand_tone}
Voice Examples: {voice_examples}
Constraints: {constraints}

```

Expected Output: Markdown draft

### 4.9 Voice & Style Transfer

Goal: Align draft to client’s voice.

Prompt (System):

```
Rewrite the draft to match the target Voice Profile and Tone while preserving facts and structure.
Return Markdown only. Do not add new claims.

```

Prompt (User):

```
Draft (Markdown):
{draft_markdown}
Voice Profile Examples: {voice_examples}
Tone: {brand_tone}
Banned Topics: {banned_topics}

```

### 4.10 Fact-check & Citation Extraction

Goal: Validate claims and surface citations.

Prompt (System):

```
Identify any factual claims in the draft. For each, return either a credible source URL or recommend revised guarded language.
Return JSON with: citations, flagged_claims, suggested_revisions.

```

Prompt (User):

```
Draft (Markdown):
{draft_markdown}
Existing References (if any): {references_json}
Region Policy: {region_policy}

```

Expected JSON:

```
{
  "citations": [ {"text": string, "url": string, "note": string} ],
  "flagged_claims": [string],
  "suggested_revisions": [ {"original": string, "revised": string} ]
}

```

### 4.11 Compliance & Claims Guardrails

Goal: Enforce constraints and safe language.

Prompt (System):

```
Review the draft for compliance and risky claims given constraints. Apply suggested revisions where appropriate.
Return Markdown with inline [CITATION] links and revised guarded language.

```

Prompt (User):

```
Draft (Markdown):
{draft_markdown}
Fact-check JSON:
{factcheck_json}
Constraints: {constraints}
Region Policy: {region_policy}

```

### 4.12 SEO/Structure Optimization (blog/guide only)

Goal: Add structure and metadata for organic performance.

Prompt (System):

```
Optimize headings, add meta title/description, suggest internal anchors, and add FAQ schema candidates. Do not add new claims.
Return JSON: meta, headings, anchors, faq.

```

Prompt (User):

```
Content (Markdown):
{content_markdown}
Seed Keywords: {keywords_seed}
Client Domain: {client_domain}

```

Expected JSON:

```
{
  "meta": {"title": string, "description": string},
  "headings": [string],
  "anchors": [ {"text": string, "target": string} ],
  "faq": [ {"q": string, "a": string} ]
}

```

### 4.13 Channel Packaging

Goal: Fit the asset to platform best practices and constraints.

Prompt (System):

```
Transform the content into platform-specific variants (LinkedIn single post, X thread, Email, Blog intro excerpt) with appropriate length, formatting, and CTA.
Return JSON: variants[], each with platform, title, body_md, cta.

```

Prompt (User):

```
Approved Content (Markdown):
{approved_markdown}
Platforms: {priority_platforms}
Goals: {priority_outcomes}

```

Expected JSON:

```
{
  "variants": [
    { "platform": "LinkedIn", "title": string, "body_md": string, "cta": string },
    { "platform": "X", "title": string, "body_md": string, "cta": string },
    { "platform": "Email", "title": string, "body_md": string, "cta": string },
    { "platform": "Blog", "title": string, "body_md": string, "cta": string }
  ]
}

```

### 4.14 Review & Approval

Goal: Human check for voice alignment and risk.

Prompt (System):

```
Summarize the key differences between the approved content and the Voice Profile, flagging any mismatches or risks in 5 bullets. Return plain text.

```

Prompt (User):

```
Approved Content:
{approved_markdown}
Voice Profile Examples:
{voice_examples}
Constraints: {constraints}

```

### 4.15 Scheduling & Publishing (metadata)

Goal: Provide scheduling metadata and UTM params.

Prompt (System):

```
For each platform variant, produce publishing metadata: best day/time (ICP timezone), UTM params (utm_source, utm_medium, utm_campaign, utm_content), and recommended hashtags (if applicable). Return JSON only.

```

Prompt (User):

```
Variants JSON:
{variants_json}
ICP Timezone/Region: {region_policy}
Campaign Name: {campaign_name}

```

Expected JSON:

```
{
  "schedule": [
    {"platform": "LinkedIn", "best_time": string, "utm": {"source": string, "medium": string, "campaign": string, "content": string}, "hashtags": [string]},
    {"platform": "X", "best_time": string, "utm": {...}, "hashtags": [string]},
    {"platform": "Email", "best_time": string, "utm": {...} }
  ]
}

```

### 4.16 Experiment Setup (A/B or Bandit)

Goal: Define variants, success metrics, allocation strategy, and minimum sample requirements suitable for the platform and goal.

Method: Choose a test design based on expected traffic. If low traffic, prefer A/B with equal allocation and longer run. If moderate traffic, use epsilon-greedy or UCB with a small exploration rate (e.g., 0.1). Define the primary success metric unambiguously (CTR, Replies, Open Rate, Clicks) and include a stopping rule (min impressions or time window). Ensure ethical constraints (no misleading hooks).

Prompt (System):

```
Create 2–3 hook/intro variants for the platform with clear success metrics and an appropriate test plan (A/B or Bandit).
Include: metric (one), allocation strategy (AB_equal|epsilon_greedy|UCB), exploration_rate (if bandit), min_sample (per variant), stopping_rule (impressions/time), and guardrails (max negative deltas prompting early stop).
Return JSON only.

```

Prompt (User):

```
Platform: {platform}
Variant Base (body): {body_md}
Goal Metric: {goal_metric}

```

Expected JSON:

```
{
  "metric": "CTR|Replies|OpenRate|Clicks",
  "variants": [ {"name": string, "hook": string}, {"name": string, "hook": string} ],
  "allocation_strategy": "AB_equal|epsilon_greedy|UCB",
  "exploration_rate": number,
  "allocation": {"variant_1": number, "variant_2": number, "variant_3": number},
  "min_sample": number,
  "stopping_rule": {"impressions": number, "days": number},
  "guardrails": [string]
}

```

### 4.17 Analytics Summary & Recommendations

Goal: Read performance and suggest next actions.

Prompt (System):

```
Analyze the performance data and produce: 3 insights, 3 recommended changes (hooks/angles/CTA), and a go/no-go on scaling the winning variant. Return JSON only.

```

Prompt (User):

```
Performance Data JSON:
{
  "platform": "{platform}",
  "metric": "{metric}",
  "results": [ {"variant": string, "impressions": number, "clicks": number, "ctr": number, "replies": number, "signups": number} ]
}
Constraints: {constraints}

```

Expected JSON:

```
{
  "insights": [string],
  "recommendations": [string],
  "decision": "scale|iterate|pause"
}

```

### 4.18 Knowledge Base Update (Learning Loop)

Goal: Update Voice/Angles/Resources with observed learnings.

Prompt (System):

```
Propose updates to the living knowledge base: refined Voice notes, winning hooks, objection rebuttals, and new resource ideas.
Return JSON only.

```

Prompt (User):

```
Latest Insights JSON:
{analytics_json}
Prior Voice Notes:
{existing_voice_notes}
Angles JSON:
{angles_json}

```

Expected JSON:

```
{
  "voice_updates": [string],
  "winning_hooks": [string],
  "objection_rebuttals": [string],
  "new_resource_ideas": [string]
}

```

---

## 5) Guardrails & QA prompts

### 5.1 Self-critique & Risk Scan

```
System: You are a critical editor. Identify logical gaps, overclaims, and weak transitions. Suggest precise fixes.
User: Draft:
{draft_markdown}
Constraints: {constraints}

Return JSON: { "issues": [string], "fixes": [ {"issue": string, "fix": string} ] }

```

### 5.2 Claims Normalizer

```
System: Normalize risky claims into guarded language (e.g., “can help”, “in many cases”).
User: Text:
{text}
Constraints: {constraints}
Return: Revised text (plain)

```

### 5.3 Voice Delta Checker

```
System: Compare provided text to Voice Profile examples and list 5 concrete adjustments to match diction/cadence.
User: Text:
{text}
Voice Examples:
{voice_examples}
Return JSON: {"adjustments": [string]}

```

---

## 6) Example usage – autonomous run (high-level)

1. Intake → run 4.1 (Canonical Brief)
2. Run 4.2 (Research) with seed competitors/keywords
3. Run 4.3 (Synthesis) → 4.4 (Resources)
4. Run 4.5 (Angles) → 4.6 (Backlog)
5. For each backlog item: 4.7 (Outline) → 4.8 (Draft) → 4.9 (Voice) → 4.10 (Fact-check) → 4.11 (Compliance)
6. Optional 4.12 (SEO) for blog/guide
7. 4.13 (Packaging) → 4.14 (Review) → 4.15 (Scheduling)
8. 4.16 (Experiment)
9. Publish & collect metrics → 4.17 (Analytics) → 4.18 (Knowledge Base)

---

## 7) Notes on platform considerations

- LinkedIn: favor credibility, data points, clear CTA; be mindful of invite/DM policies and avoid automation that violates ToS.
- X: first 2 lines are the hook; threads with strong structure, 1 idea per tweet.
- Email: segment by engagement; ensure DMARC/SPF/DKIM, one-click unsubscribe; keep complaint rate < 0.3%.
- Blog/Guides: show references; avoid thin content; include checklists and next-step CTAs.

---

## 8) Deliverables summary

- Canonical Brief JSON
- Research JSON (market sentiment, pains, JTBDs, objections)
- Opportunity Map JSON
- Resource Strategy JSON
- Angle Matrix JSON
- Backlog JSON
- Outlines JSON per asset
- Drafts (Markdown) per asset
- Fact-check & Compliance JSON
- Platform Variants JSON + Scheduling JSON
- Experiment Plan JSON
- Analytics Summary JSON
- Knowledge Base Update JSON

---

## 9) Operationalization pointers

- Orchestrate stages in a workflow tool (e.g., n8n) with a Postgres/NocoDB backend to store JSON between steps.
- Keep prompts in version control; track output schemas strictly.
- Enforce review gates only at 4.14; the rest runs autonomously from canonical inputs.
- Log references and claims provenance to enable future audits.

---

If you want to learn more about what I can help you with, read the box below 👇

<aside>
▶️

# **Are you a B2B founder who hate marketing?**

Then let’s chat. I don’t dislike marketing.

In fact - I’m borderline obsessed with building high-leverage B2B growth systems, as you’ve probably noticed from my unapologetically detailed writing style. 🥸

I like to think I have a bit of that "productive autism" - the kind that lets me hyper-focus on building genuinely useful stuff.

Anyway, enough about my quirks.

Here’s what matters to you:

If you’re running a B2B business and you're fed up with chasing the latest shiny marketing tactic, then we should probably talk.

Over the past 5 years, I’ve engineered a B2B growth system specifically designed to automate trust-building at scale.

The hidden truth in B2B sales is that a certain level of trust needs to be established before any meaningful deal can close - hence the notoriously lengthy sales cycles.

Yet most founders waste endless hours manually building trust with cold audiences. Bad use of your limited time.

Instead, I install a system that automates initial lead attraction and systematically builds trust, so you spend your time exclusively with warmed-up leads who are ready to close.

You can keep rolling your eyes at marketing - while the system quietly handles it for you.

If that sounds appealing, I recorded a quick walkthrough showing exactly how it works from start to finish.

**Click below to watch it.**

![image.png](attachment:ed146fd6-b9ea-4e96-8762-242a6241ffe6:image.png)

</aside>

Best,

[Harald *(The AI Growth guy for B2B founders)*](https://www.linkedin.com/in/haraldroine/)