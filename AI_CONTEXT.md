# Vnstock AI Context

This project is a local fork/vendor copy of upstream `vnstock` used by the
equity workspace as a Python data dependency.

## Agent Guide

Use `docs/agent-guide/vnstock/` as the local reference copy of the free-tier
`vnstock` guide from <https://github.com/vnstock-hq/vnstock-agent-guide>.

Consult it when writing examples, checking public API usage, or explaining
free `vnstock` behavior. Do not recommend or assume access to paid-tier
libraries such as `vnstock_data`, `vnstock_ta`, `vnstock_news`, or
`vnstock_pipeline` unless the user explicitly changes their access level.

Do not treat the guide as source-code architecture for this fork unless the
local implementation confirms the same behavior.

## Local Policy

Keep `AGENTS.md` focused on contribution behavior. Do not overwrite this
project's root `AGENTS.md` with the external guide's `AGENTS.md`.
