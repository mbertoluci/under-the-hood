# Episode 02 — Watch V8 give up on your code

> V8's optimizing compiler doesn't compile generic code. It compiles a specialized
> version based on what it has observed, and throws it away the moment you break
> its assumptions. That's deoptimization, and you can watch it happen.

## Run it

```bash
node --trace-opt --trace-deopt episodes/02-jit-pipeline/deopt-live.js 2>&1 | grep -E "PHASE|add"
```

## What you should see

Output varies by Node version. On Node 22, the relevant lines look like this:

```
PHASE 1: feeding add() with numbers only...
[marking <JSFunction add> for optimization to TURBOFAN, reason: hot and stable]
[completed optimizing <JSFunction add> (target TURBOFAN)]

PHASE 2: the betrayal. Passing strings now...
[bailout (kind: deopt-eager, reason: not a Smi): deoptimizing <JSFunction add>, <Code TURBOFAN>]

PHASE 3: back to numbers...
[marking <JSFunction add> for optimization to TURBOFAN, reason: hot and stable]
[completed optimizing <JSFunction add> (target TURBOFAN)]
```

## Reading the output

- **"hot and stable"**: the function ran a lot (hot), always with the same types (stable). TurboFan compiles a specialized, number-only version.
- **"bailout ... reason: not a Smi"**: a Smi (Small integer) is V8's fast internal format for whole numbers. The optimized code expected one, received a string, and bailed out. The function goes back to the interpreter.
- **Phase 3**: V8 re-optimizes once the types stabilize again. Every cycle costs: discard code, recompile, run slower in between.

## Takeaways

1. In hot code, feed each function one consistent set of types.
2. TypeScript discipline helps here: typed code tends to stay monomorphic, which is exactly what the engine optimizes best.

📎 LinkedIn post: _coming soon_
