# Installation & Workspace Fix Guide

## Fresh Install

```bash
# 1. Get app
cd /path/to/frappe-bench
bench get-app media_advertising /path/to/media_advertising

# 2. Install on site
bench --site your-site.localhost install-app media_advertising

# 3. Migrate (this runs patches, syncs workspaces, loads fixtures)
bench --site your-site.localhost migrate

# 4. Build assets
bench build --app media_advertising

# 5. Restart
bench restart
```

After this the **Media Advertising** workspace appears in the left sidebar
and in the workspace list at `/app/workspace`.

---

## If Workspace Still Missing (most common issue)

Run this ONE command — it executes the patch manually:

```bash
bench --site your-site.localhost execute \
  media_advertising.patches.v1_0.create_workspace.execute
```

Then hard-refresh your browser (`Ctrl+Shift+R`).

---

## If App Not Visible on Home Page Left Sidebar

The sidebar shows modules from `config/desktop.py`. If it's missing:

```bash
# Clear cache
bench --site your-site.localhost clear-cache
bench --site your-site.localhost clear-website-cache
bench restart
```

If still missing, go to **Workspace list** (`/app/workspace`), find
**Media Advertising**, open it, and click **Publish** if it shows as unpublished.

---

## Upgrading / Resync Workspace After Code Changes

```bash
bench --site your-site.localhost migrate
bench build --app media_advertising
bench restart
```

The patch `create_workspace` is idempotent — it updates the existing record.

---

## Manual Workspace Import (last resort)

```bash
bench --site your-site.localhost import-doc \
  apps/media_advertising/media_advertising/workspace/media_advertising.json
```

---

## Fixture Reload

```bash
bench --site your-site.localhost import-fixtures --app media_advertising
```
