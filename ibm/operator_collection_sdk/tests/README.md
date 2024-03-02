### Running Tests Locally
---

Test scripts can be run from anywhere within the repository collection, given current working directory is `~/.../ibm/operator_collection_sdk/.../`.

Make sure to supply the `-i` or `--install-collection` flag to install the collection locally before testing.

**Quick Start:**
1. Navigate to `~/.../ibm/operator_collection_sdk/`
2. Deactivate virtual environment if it is active
3. Run a command *with* the `-i` / `--install-collection` flag
---

#### Unit Tests
Install collection and run all unit tests:
```bash
sh ./tests/unit/unit.sh -i
```
---

#### Sanity Tests
Install collection and run sanity tests:
```bash
sh ./tests/unit/unit.sh -i
```
---

#### Integration Tests
Install collection and run all Integration tests:
```bash
sh ./tests/integration/integration.sh -i
```