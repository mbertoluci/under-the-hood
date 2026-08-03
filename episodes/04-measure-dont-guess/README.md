# Episode 04 — Stop guessing, start measuring

> A fake API worker with three suspects: validate, transform, serialize.
> One of them is slow. Don't guess. Node ships with a sampling profiler:
> about 1,000 times per second it checks which function is running and
> keeps a tally. The function with the most ticks is your bottleneck.

## Run it

```bash
node --prof episodes/04-measure-dont-guess/profile-me.js
node --prof-process isolate-*.log > profile.txt
```

Open `profile.txt` and read the `[JavaScript]` section. Delete the
`isolate-*.log` file when you're done.

## What I got (Node 22, Apple Silicon)

```
[JavaScript]:
  ticks  total  name
    43   10.2%  Builtin: KeyedStoreIC_Megamorphic
    37    8.8%  JS: *deepClone  profile-me.js:44
    17    4.0%  Builtin: KeyedLoadIC_Megamorphic
```

The verdict: `deepClone`, a hand-rolled recursive clone running on every
request. The two "Megamorphic" builtins around it are collateral damage
(episode 03 explains what megamorphic means). `validate` and `transform`
don't even show up.

## The fix, and the proof

`transform` already returns fresh objects, so the clone was pure waste.
Removing that one line:

```
before:  0.456s
after:   0.304s   (33% faster, same output)
```

## The workflow that matters more than the tools

1. A real metric says "this is slow" (latency, throughput, cost).
2. Profile under realistic conditions.
3. Fix the top hotspot. Only that one.
4. Measure again.
5. Stop. Readability wins everywhere else.

Other tools for the same job: Chrome DevTools profiler (`node --inspect`),
`node --cpu-prof` (open the file in DevTools), 0x and clinic.js for
flamegraphs.

📎 LinkedIn post: _coming soon_
