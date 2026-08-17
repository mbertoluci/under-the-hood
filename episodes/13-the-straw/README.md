# Episode 13 — Serving 2 GB with ~50 MB of RAM

> To drink a pool you don't need a pool-sized stomach. You need a
> straw. Streams move a file from disk to socket in ~64 KB sips, so
> only the sip ever lives in RAM — no matter how big the pool is.
> The whole trick is one line: `fs.createReadStream(file).pipe(res)`.

## Run it

```bash
node episodes/13-the-straw/big-file-server.js
```

Creates a temporary 2 GiB file (deleted at the end), serves it two
ways, and reports the server's own peak RSS. Three processes keep the
measurement honest: a child creates the file, the server samples its
peak memory, a forked client streams the download and discards it.

## What I got (Node 22, Apple Silicon)

```
file size: 2048 MB
baseline RSS:                 46 MB
/straw (createReadStream):    peak 123 MB
/gulp  (whole file in RAM):   peak 2167 MB
```

Full honesty: the title says ~50 MB and the straw peaked at 123 MB —
the 64 KB sips churn the garbage collector a bit. Still 17x less than
the gulp, and the important property: the straw's cost does NOT grow
with the file. The gulp's does, per request.

## Three walls Node put in my way (all deliberate)

Building the gulp took effort, because Node really doesn't want you to
do it:

1. **`fs.readFile` refuses files of 2 GiB or more**
   (`ERR_FS_FILE_TOO_LARGE`). I had to gulp by hand with a Buffer and
   a read loop.
2. **A single 2 GiB socket write overflows an int32** and kills the
   connection.
3. **Queueing 2 GiB of writes at once also kills the socket** — I had
   to add `drain` handling (backpressure!) to make the WRONG solution
   work at all. That is next episode's topic, arriving early.

When the platform fights you this hard, it's telling you something.

## The one-liner

**The pool is huge. The sip is tiny. Only the sip needs to fit in RAM.**
