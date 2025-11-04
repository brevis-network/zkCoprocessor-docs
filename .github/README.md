# GitHub Actions Sync Workflow

This directory contains the GitHub Actions workflow and scripts for automatically syncing content from the `main` branch to the `deploy` branch with preprocessing.

## Files

### `.github/workflows/sync-deploy.yml`
GitHub Actions workflow that:
- Triggers on pushes to the `main` branch
- Processes markdown files using the Python script
- Syncs the processed files to the `deploy` branch

### `.github/scripts/process_markdown.py`
Python script that processes markdown files by:
1. **Removing YAML frontmatter**: Removes description sections (lines between `---`) from the top of MD files
2. **Converting SUMMARY.md titles**: Changes level 2 titles (`##`) to level 1 titles (`#`) in SUMMARY.md
3. **Removing figure HTML elements**: Removes `<figure>` and `</figure>` tags while preserving the content inside

### `.github/scripts/test_processing.sh`
Local test script to validate the markdown processing functionality.

## How It Works

1. When code is pushed to the `main` branch, the GitHub Action is triggered
2. The workflow checks out the `main` branch and processes all markdown files
3. The processed files are then synced to the `deploy` branch
4. **The changes are reverted on the main branch** to keep original files intact
5. The commit message includes reference to the original main branch commit

This ensures that:
- **Main branch**: Contains original files with YAML frontmatter and figure tags
- **Deploy branch**: Contains processed files ready for deployment

## Testing Locally

You can test the markdown processing locally by running:

```bash
# Test the processing
./.github/scripts/test_processing.sh

# Or run the processing script directly
python .github/scripts/process_markdown.py
```

## Example Transformations

### YAML Frontmatter Removal
**Before:**
```markdown
---
description: Write custom computation circuit for your application.
---

# Application Circuit
```

**After:**
```markdown
# Application Circuit
```

### SUMMARY.md Title Conversion
**Before:**
```markdown
## Developer Guide
## Developer Resources
```

**After:**
```markdown
# Developer Guide
# Developer Resources
```

### Figure Tag Removal
**Before:**
```markdown
<figure><img src="../../.gitbook/assets/img2.png" alt=""><figcaption></figcaption></figure>
```

**After:**
```markdown
<img src="../../.gitbook/assets/img2.png" alt=""><figcaption></figcaption>
```