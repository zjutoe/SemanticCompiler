# K3-X execution binding acceptance

- Candidate: `d3436f38c053e20d3863dc4d8b56ee1b35c47ccc`
- Parent: `6bac6186d446c5b63ce271350479272caf826f9b`
- Review: independent, strict, read-only, GPT-5.6 Sol high
- Verdict: **ACCEPT**

Accepted byte boundaries:

- execution binding blob: `8289943903b58154e5933c43626e14d646260c16`
- command amendment blob: `aeb2981cbda400cfcba88c33064f2101e2f3d634`
- accepted implementation: `326a57f23ba2934f9cb27d0cd5380643325c1a52`
- implementation acceptance: `dd167e98d70deecb48ca912e678ca22cc7c7e5d5`

The binding requires main to dispatch one exact later execution `HEAD` carrying
these two exact blobs and all six accepted implementation blobs. The complete
operator/launcher/Python environment, runtime hashes, command-once ordering,
success/failure report schemas, dirty-report refusal, sole report path,
exclusions, limited conclusion, and final independent result gate are accepted.

This acceptance does not itself execute either evidence command and grants no
source repair, retry, external access, held-out access, or K4 authority.
