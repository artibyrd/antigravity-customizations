# GLOSSARY.md Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of what the term IS.}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated:** When multiple words compete for the same concept, choose the clearest canonical term and list rejected synonyms under `_Avoid_`.
- **Keep definitions tight:** One or two sentences max. Define what the concept **is**, not how it is implemented.
- **Zero implementation details:** Never include table schemas, HTTP routes, class/function names, library choices, or scratchpad notes.
- **Domain-specific terms only:** Exclude general programming concepts (timeouts, retries, error types, adapters, utilities) even if the codebase uses them everywhere. Before adding a term, ask: *is this unique to this domain context, or a general software term?* Only add the former.
- **Group naturally:** Keep a flat list for cohesive small domains; introduce subheadings only when clear clusters emerge.

## Single-Context vs. Multi-Context Repos

- **Single context (most repos):** One `GLOSSARY.md` at the repository root.
- **Multiple contexts:** A `GLOSSARY-MAP.md` at the repository root pointing to each context's `GLOSSARY.md` and summarizing how contexts interact:

```md
# Glossary Map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): receives and tracks customer orders
- [Billing](./src/billing/GLOSSARY.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/GLOSSARY.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared concepts for `CustomerId` and `Money`
```

### Inference Rules
1. If `GLOSSARY-MAP.md` exists, read it first to locate bounded contexts.
2. If only a root `GLOSSARY.md` exists, treat the repo as single-context.
3. If neither exists, create a root `GLOSSARY.md` lazily when the first domain term is resolved.
4. When multiple contexts exist and the active topic's context is ambiguous, inspect the code first; ask the user only if still unclear.
