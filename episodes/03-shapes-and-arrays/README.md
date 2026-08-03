# Episode 03 — Your arrays have shapes too

> V8 tags every array with an internal label (its "elements kind") describing
> what's inside: PACKED_SMI (whole numbers, fastest), PACKED_DOUBLE (decimals),
> PACKED (anything), each with a HOLEY twin for arrays with gaps. The label only
> moves toward slower kinds, never back. `new Array(n)` is born HOLEY.

## Run it

```bash
# Main benchmark: packed vs born-holey (filled) vs real holes
node episodes/03-shapes-and-arrays/benchmark-holey.js

# The plain variant: same comparison, simpler loop
node episodes/03-shapes-and-arrays/benchmark-holey-plain.js

# Bonus: object shapes, monomorphic vs megamorphic access
node episodes/03-shapes-and-arrays/benchmark-monomorphic.js
```

## Results on my machine (Node 22, Apple Silicon)

`benchmark-holey.js` (loop guards each read with `|| 0`):

```
1. packed  ([] + push)     104 ms
2. holey, fully filled     201 ms   (1.93x)
3. holey, real holes       210 ms   (2.01x)
```

`benchmark-holey-plain.js` (plain `total += arr[i]`, holey fully filled):

```
packed  ([] + push)        104 ms
holey, fully filled        103 ms   (1.00x)
```

## The honest takeaway

The two variants disagree on purpose. In the plain loop, modern V8 optimizes the
cost of a fully-filled HOLEY array away completely. Add a small guard around the
read and the same label costs ~2x. Real holes cost ~2x in both worlds.

So the HOLEY label is not a fixed price. It's a **risk** whose cost depends on
the code around it. In hot paths, don't gamble:

1. Build arrays with `[] + push` or `Array.from`, skip `new Array(n)`.
2. Never `delete` from an array, never skip indexes.
3. Keep contents homogeneous.
4. Distrust performance advice that ships without a benchmark. Including this
   one: run the scripts on your machine and your Node version.

📎 LinkedIn post: _coming soon_
