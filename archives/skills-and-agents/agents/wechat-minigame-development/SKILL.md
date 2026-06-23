---
name: wechat-minigame-development
description: Use when building, porting, or debugging a WeChat Mini Game, especially with PixiJS, Matter.js, or Vite, and the work involves Mini Game runtime incompatibilities such as adapter setup, single-file CJS bundling, touch/input handling, open data context, GLSL/WebGL limits, audio/storage/request APIs, or maintaining AGENTS.md and CLAUDE.md guardrails for AI-driven development.
---

# WeChat Minigame Development

## Overview

Build WeChat Mini Games without accidentally treating them like H5 pages or standard Mini Programs. This skill distills a proven PixiJS 6 + Matter.js + Vite workflow, the platform pitfalls that repeatedly break AI-generated code, and the documentation habits that make AI changes hold up over time.

## Use This Skill When

- The target is a canvas-heavy WeChat Mini Game, not a standard `wxml/wxss` Mini Program page.
- The stack uses PixiJS, Matter.js, Vite/Rollup, or a similar custom canvas runtime.
- The task touches startup, rendering, input, audio, storage, networking, open data context, or build output.
- The project is AI-assisted and needs root instruction files such as `AGENTS.md` or `CLAUDE.md` to capture non-obvious runtime rules.

## Do Not Use This Skill As The Primary Guide When

- The task is a standard WeChat Mini Program UI flow with `wxml`, `wxss`, and page routing rather than a game runtime.
- The project is fully owned by a different engine or build pipeline and you only need engine-specific editor steps.
- The problem is backend-only and does not depend on Mini Game runtime constraints.

## Quick Triage

| If the task is about | Read |
|---|---|
| Picking the stack, configuring Vite/Rollup, or fixing startup crashes | `references/stack-and-build.md` |
| Runtime incompatibilities, rendering/input issues, platform APIs, open data context, or texture timing bugs | `references/platform-pitfalls.md` |
| Making AI changes safer with `AGENTS.md`, `CLAUDE.md`, and constrained prompts | `references/ai-collaboration.md` |

## Core Rules

1. Treat the target as a WeChat Mini Game, not browser code. Assume DOM APIs are unsafe until proven otherwise.
2. Keep stack assumptions explicit. Prefer PixiJS 6, Matter.js, and a single-file CJS Vite build unless the existing project already chose something else.
3. Externalize hidden constraints before feature work. Put them in `AGENTS.md`, `CLAUDE.md`, or the repo's equivalent root instruction file.
4. Make surgical changes. Mini Game infra is fragile; do not refactor base rendering/build code unless the task requires it.
5. Verify in the real Mini Game runtime or WeChat DevTools, not only in a browser.

## Workflow

### 1. Confirm The Runtime Contract

- Verify the project is a WeChat Mini Game, not H5 and not a normal Mini Program page app.
- Identify the engine, build output, adapter layer, and any sandboxed open data context.
- Seed or update `AGENTS.md` with the relevant runtime constraints before asking AI to add features.

### 2. Lock The Build And Startup Invariants

- Import adapter/shim code before touching Pixi, `wx`, or `canvas`.
- Delay actual engine initialization by two animation frames, with a `setTimeout` fallback.
- Output one CJS `game.js` bundle and inline dynamic imports.
- Replace `process.env.NODE_ENV` at build time instead of expecting it at runtime.

### 3. Implement Features In Mini Game Style

- Use `pointerdown`, not `click`.
- Use the global `canvas`, not DOM lookup.
- Use `wx.*` APIs for audio, storage, and network access.
- Cache system info once, export derived layout constants, and avoid hard-coded device heights.
- Treat open data context as a separate sandbox with its own build rules.

### 4. Capture What Broke

- Every new runtime bug should become a short, numbered `AGENTS.md` rule.
- Record the trigger, bad pattern, correct pattern, and how to verify the fix.
- Keep the next AI run from rediscovering the same issue.

### 5. Verify Before Hand-Off

- Startup no longer crashes on `wx`, `canvas`, or shader compilation.
- Input works in Mini Game runtime.
- Audio, storage, and network all use `wx.*` APIs.
- Open data context still builds and runs in its sandbox.
- Texture-dependent sizing waits for texture readiness.

## Example Bootstrap Pattern

```ts
import '@iro/wechat-adapter';
import '@pixi/unsafe-eval';

function initGame() {
  // Create PIXI renderer with the global canvas and continue boot.
}

function deferInit() {
  if (typeof requestAnimationFrame !== 'undefined') {
    requestAnimationFrame(() => requestAnimationFrame(initGame));
    return;
  }

  setTimeout(initGame, 50);
}

setTimeout(deferInit, 0);
```

Use this whenever startup timing differs between the Mini Game runtime and a normal browser.

## Common Mistakes

- Treating the project as browser code and introducing `window`, `document`, `fetch`, `localStorage`, or `new Audio()`.
- Upgrading PixiJS without checking shader/runtime compatibility first.
- Letting the bundler emit ESM or split dynamic chunks.
- Fixing a runtime bug without promoting it into `AGENTS.md`.
- Asking AI for a feature without explicit constraints, then accepting unrelated refactors.

## Resources

- `references/stack-and-build.md`
- `references/platform-pitfalls.md`
- `references/ai-collaboration.md`
