# When to Mock (and Hermetic Boundaries)

Mock at **external system boundaries** only:
- Third-party HTTP APIs (payments, email, webhooks, LLM endpoints)
- Non-deterministic inputs (wall-clock time, UUID/RNG generation)
- External databases or remote queues (prefer an in-memory fake or ephemeral local test DB whenever practical)
- Filesystem only when an isolated temporary directory is impractical

Do **not** mock:
- Your own classes, modules, or domain services
- Internal collaborators inside the same boundary
- Anything you control that can execute fast, offline, and deterministically

---

## Designing Clean Boundary Seams

### 1. Inject External Dependencies

Pass external clients in at the seam instead of instantiating them inside domain logic:

```typescript
// GOOD: External client injected at the seam
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// BAD: Hard-wired external SDK forces monkey-patching or live calls
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

### 2. Prefer Narrow SDK-Style Adapters Over Generic Fetchers

Expose one focused operation per external capability instead of a generic transport function requiring conditional routing inside mocks:

```typescript
// GOOD: Each operation is narrow, typed, and independently fakeable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch("/orders", { method: "POST", body: data }),
};

// BAD: Generic fetcher forces fragile URL-matching logic inside test mocks
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

Why narrow SDK adapters win:
- Each fake returns one explicit shape with zero conditional branching
- Tests state clearly which external operation they exercise
- Static types validate every fake against the real seam

### 3. Prefer In-Memory Fakes Over Heavy Mock Frameworks

When a real local boundary exists (e.g., SQLite in-memory, temporary directory, in-memory repository implementing the same interface), use it instead of assertion-heavy mock spies. In-memory fakes preserve hermetic offline speed while catching real contract bugs that brittle mocks miss.
