# Episode 01 — Meet V8

> Your JavaScript doesn't run itself.

**The story:** in 2008, JavaScript was too slow for the apps Google wanted to build (Gmail, Maps). So Google hired Lars Bak — a virtual machine legend — who assembled a small team in Aarhus, Denmark, and built a new engine from scratch. When Chrome launched with V8, JavaScript got ~10x faster overnight.

One year later, Ryan Dahl took the open-source V8 and built **Node.js** on top of it. No V8 → no Node → no modern JS ecosystem.

## Key ideas

1. **V8 compiles your JS to machine code** — it's not "just interpreted" anymore.
2. **Type erasure lives upstream:** TypeScript never reaches V8 — only the compiled JS does.
3. **The engine bets on your consistency** (hidden classes) — episode 03 goes deep on this.

## Who maintains it

Google (Chromium project). 100% open source: https://v8.dev

Runs inside: Chrome, Edge, Node.js, Deno, Electron, Cloudflare Workers.

📎 LinkedIn post: _coming soon_
