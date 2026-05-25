# Publishing Notes

This directory is the public published location of the `music-shelf` skill inside the `qsunyi/skills` repository.

## Source of development

Day-to-day development happens in a local development source tree maintained by the author. This directory receives publish-ready updates for the `music-shelf` skill.

## Recommended publishing flow

1. Update the local development source.
2. Validate behavior and documentation locally.
3. Sync only the intended public files into `music-shelf/` inside this repository working tree.
4. Review `git status` and `git diff --stat` carefully at the repository root.
5. Commit and push the publish-ready changes from the `qsunyi/skills` repository.

## Repository role

The repository `qsunyi/skills` acts as a multi-skill public distribution repo. The `music-shelf/` directory is the public standalone distribution path for this skill.
