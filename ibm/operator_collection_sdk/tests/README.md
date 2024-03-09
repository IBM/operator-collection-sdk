### Running Tests Locally
---

> This document does not cover molecule testing.

Test scripts can be run from anywhere within the collection, given the current working directory is `~/**/ibm/operator_collection_sdk/*`.

By default, the tests will install the codebase/collection locally. This functionality can be configured with the following flags:`-i` / `--install-collection` 
which can be set either `true` or `false`, i.e. `--install-collection=false`.

Usage: 
- `--install-collection=<true|false>`, default: `true`
- Alias: `-i=<true|false>`

**Quick Start:**
1. Navigate to `~/**/ibm/operator_collection_sdk/*`.
2. Deactivate your virtual environment (if it is active).
3. Run a test script.
---

#### Unit Tests
To install the collection and run all unit tests:
```bash
sh ./tests/unit/unit.sh
```
---

#### Sanity Tests
To install the collection and run sanity tests:
```bash
sh ./tests/unit/unit.sh
```
---

#### Integration Tests
To install the collection and run all Integration tests:
```bash
sh ./tests/integration/integration.sh
```
Note: This test will set up and teardown a cluster environment too.