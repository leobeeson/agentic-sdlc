# Testing conventions

How this project tests. Every agent that reasons about tests reads this file. The setup phase seeds it from the detected or declared stack; keep it current as conventions settle.

Keep this file under 200 lines.

## Test commands

The exact commands that run the suite (the authoritative copy is `test_gate.commands` in `sdlc.config.yaml`).

## Test naming

The naming convention for tests (for example `test_<behaviour>`).

## Cadence

The development cadence (for example red, green, refactor in vertical slices).

## Mocking policy

Where mocking is allowed (for example only at system boundaries), and the real defaults used in place of mocks.

## Levels

What unit, integration, and end-to-end mean in this project, and when each applies.
