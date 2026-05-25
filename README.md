# skills

A public repository for reusable AI agent skills.

This repository is used to publish standalone skills that are developed locally and then synchronized here for reuse, versioning, and sharing.

## Repository structure

Each top-level directory in this repository represents one skill.

Current published skills:

- [`music-shelf/`](./music-shelf/) — a skill for organizing and maintaining local music libraries, with a focus on archival workflows, normalization, de-duplication, and incremental maintenance.

## Publishing model

Day-to-day development may happen in a separate local development source tree. Publish-ready files are synchronized into this repository and then committed here.

## Notes

- Treat this repository as the public distribution surface.
- Review skill-specific `README.md`, `SKILL.md`, and related references inside each skill directory for details.
