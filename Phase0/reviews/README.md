# Phase 0 accepted review records

This directory receives real accepted stage review records only. Do not create placeholder or speculative reports.

Each record must use `E<N>_<short-reviewed-sha>_review.md` and include at least:

- exact handoff path and handoff blob SHA;
- exact reviewed commit or commit range;
- intended diff and exact allowed paths;
- verification commands and results;
- paths and checksums for relevant external artifacts;
- reviewer verdict and findings;
- resolution commit for every repaired finding, or an explicit statement that none was required.

The reviewer is independent and read-only. Main owns acceptance, and a record is accepted only for the exact commit/range it names.
