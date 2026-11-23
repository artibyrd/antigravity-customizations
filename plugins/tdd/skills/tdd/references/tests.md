# Good and Bad Tests

## Good Tests

**Integration-style at a real seam:** Test through public interfaces, not mocks of internal collaborators.

```typescript
// GOOD: Tests observable behavior through the public seam
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentGateway);
  expect(result.status).toBe("confirmed");
});
```

Characteristics:
- Verifies behavior callers/users actually care about
- Uses the public interface exclusively
- Survives internal refactors unchanged
- Describes **WHAT**, not **HOW**
- Runs hermetically (deterministic clock/RNG, offline, isolated state)
- Asserts one logical outcome per test

---

## Bad Tests

### 1. Implementation-Detail Tests

Coupled to internal wiring; breaks when internals are refactored even though behavior is identical.

```typescript
// BAD: Asserts internal wiring instead of observable outcome
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Red flags:
- Mocking internal classes or collaborators you own
- Testing private helper methods directly
- Asserting call counts or invocation order
- Test name describes *how* the code works instead of *what* it guarantees
- Verifying through a side channel instead of the public interface:

```typescript
// BAD: Bypasses the interface to inspect internal storage
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies round-trip behavior through the public seam
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

### 2. Tautological Tests

The expected value recomputes the implementation's own logic, so the test passes by construction and cannot catch a broken formula.

```typescript
// BAD: Expected value mirrors the implementation
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, worked literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

### 3. Non-Hermetic / Flaky Tests

Tests that depend on live internet calls, wall-clock `Date.now()`, unseeded randomness, or shared mutable directories fail intermittently and poison the TDD loop. Always inject clocks/RNG, isolate temp paths, and run against real in-memory or local seams.
