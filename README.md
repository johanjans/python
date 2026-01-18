# Scientific Programming

A computer supported approach to engineering mathematics.

## Project Architecture

This project uses a **shared infrastructure model** where common theme files, Lua filters, and build tools are centralized in the [quarto-shared](https://github.com/cenmir/quarto-shared) repository. This allows multiple Quarto book projects (python, mechanics, fem, etc.) to share the same styling and build system.

```
~/
├── quarto-shared/      # REQUIRED - Shared infrastructure (separate git repo)
│   ├── theme/          # SCSS stylesheets (dark.scss, light.scss, custom.scss)
│   ├── filters/        # Lua filters (hint.lua, color-emphasis.lua, lastModified.lua)
│   ├── includes/       # Footer, citation style
│   └── quarto_shared/  # Python package for build, sync & post-processing
│
├── python/             # This project
├── mechanics/          # Applied Mechanics book
└── fem/                # Future projects...
```

### How It Works

**Static files** (SCSS, Lua, HTML) are synced/copied from quarto-shared to each project.

**Python logic** (build, sync, post-processing) runs directly from `~/quarto-shared` - never copied.
This means updates to the build system apply to all projects automatically.

---

## For New Authors

### Prerequisites

1. **Python 3.10+** with pip
2. **Quarto CLI** - [Install Quarto](https://quarto.org/docs/get-started/)
3. **Git** configured with SSH key access

### Initial Setup

#### 1. Clone quarto-shared (required for all projects)

```bash
cd ~
git clone https://github.com/cenmir/quarto-shared.git quarto-shared
```

This repository contains all shared theme files and the build system. **Every author needs this.**

#### 2. Clone this project

```bash
cd ~
git clone <python-repo-url> python
```

#### 3. Set up Python environment

```bash
cd ~/python
python3 -m venv .venv
source .venv/bin/activate
pip install pyyaml beautifulsoup4 lxml
```

#### 4. Verify quarto-shared integration

```bash
./publish.py --version
```

Should show: `publish 2.0.0 (quarto_shared 1.1.0)`

#### 5. Sync theme files from quarto-shared

```bash
./publish.py --sync
```

This copies the latest theme files from `~/quarto-shared` into this project.

#### 6. Preview locally

```bash
quarto preview
```

The site will be available at http://localhost:4200

### Writing Content

- **Quarto documents**: Create `.qmd` files for text-heavy content
- **Jupyter notebooks**: Create `.ipynb` files for interactive code examples
- Add new files to `_quarto.yml` under the appropriate chapter/part

### Building and Publishing

```bash
./publish.py              # Build changed files and deploy
./publish.py --full       # Force full rebuild
./publish.py --dry-run    # Preview what would be built
./publish.py --no-deploy  # Build locally without deploying
./publish.py --git        # Build, deploy, and push to git
```

**Automatic sync check**: Before each build, the script checks if theme files differ from `quarto-shared` and prompts you to sync:

```
3 file(s) differ from quarto-shared:

  ~ dark.scss (modified)
  ~ custom.scss (modified)

Sync theme files from quarto-shared? [y/N]
```

---

## Starting a New Book Project (e.g., FEM)

### Option 1: Using init-book (Recommended)

The easiest way to create a new book project:

```bash
# 1. Ensure quarto-shared is cloned
cd ~
git clone https://github.com/cenmir/quarto-shared.git quarto-shared  # if not already done

# 2. Initialize the new project
python -m quarto_shared.init_book ~/fem \
    --title "Finite Element Methods" \
    --port 4202 \
    --deploy-path "/var/www/fem/"

# 3. Start working
cd ~/fem
quarto preview
```

The `init-book` command creates:
- `_quarto.yml` configured for the shared theme
- `publish.py` build script (edit `DEPLOY_DIR` and `SSH_KEY` as needed)
- `index.qmd` starter page
- All theme files synced from quarto-shared
- Git repository initialized with initial commit

**init-book options:**
- `--title, -t`: Book title (default: "My Quarto Book")
- `--port, -p`: Preview server port (default: 4200)
- `--deploy-path, -d`: Server deployment path (default: /var/www/mybook/)
- `--no-git`: Skip git initialization

### Option 2: Manual Setup

If you prefer to set up manually:

1. Create project directory: `mkdir ~/fem && cd ~/fem`

2. Create `_quarto.yml`:

```yaml
project:
  type: book
  output-dir: _book
  preview:
    port: 4201

book:
  title: "Finite Element Methods"
  author:
    - name: "Your Name"
      email: "your.email@example.com"
  page-navigation: true
  sidebar:
    search: true
    collapse-level: 1
  chapters:
    - index.qmd

# These files come from quarto-shared via ./publish.py --sync
filters:
  - lastModified.lua

format:
  html:
    theme:
      dark: [darkly, dark.scss, custom.scss]
      light: [flatly, light.scss, custom.scss]
    filters:
      - hint.lua
      - color-emphasis.lua
    toc: true
    code-fold: true
    html-math-method:
      method: mathjax
      url: https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js
    header-includes: |
      <link href='https://fonts.googleapis.com/css?family=Vollkorn' rel='stylesheet'>
      <link rel="stylesheet" type="text/css" href="https://cdn.rawgit.com/dreampulse/computer-modern-web-font/master/fonts.css">
    include-after-body:
      - footer.html
    number-sections: true
    number-depth: 1

crossref:
  eq-prefix: ""
```

3. Copy `publish.py` from an existing project and update `DEPLOY_DIR`

4. Run `./publish.py --sync` to copy theme files

5. Create `index.qmd` and initialize git

---

## Working with quarto-shared

### Updating the shared theme

When you want to change styles that apply to ALL projects:

1. Edit files in `~/quarto-shared/theme/`, `~/quarto-shared/filters/`, etc.
2. Commit and push:
   ```bash
   cd ~/quarto-shared
   git add -A
   git commit -m "Update dark theme colors"
   git push
   ```
3. In each project, the next `./publish.py` run will detect changes and prompt to sync

### Multi-user workflow

1. **User A** updates `quarto-shared` and pushes
2. **User B** pulls the latest:
   ```bash
   cd ~/quarto-shared
   git pull
   ```
3. **User B** runs `./publish.py` in their project - sync prompt appears automatically

### Files managed by quarto-shared

| Source | Destination | Purpose |
|--------|-------------|---------|
| `quarto-shared/theme/dark.scss` | `project/dark.scss` | Dark mode styling |
| `quarto-shared/theme/light.scss` | `project/light.scss` | Light mode styling |
| `quarto-shared/theme/custom.scss` | `project/custom.scss` | Custom components |
| `quarto-shared/filters/hint.lua` | `project/hint.lua` | Hint box filter |
| `quarto-shared/filters/color-emphasis.lua` | `project/color-emphasis.lua` | Color spans |
| `quarto-shared/filters/lastModified.lua` | `project/lastModified.lua` | Last modified date |
| `quarto-shared/includes/footer.html` | `project/footer.html` | Page footer |
| `quarto-shared/includes/elsevier-vancouver.csl` | `project/elsevier-vancouver.csl` | Citation style |

---

## Custom Styling (from quarto-shared)

### Hint Boxes (blurred until hover)
```markdown
::: {.hintbox}
Hidden hint content revealed on hover.
:::
```

### Note Boxes
```markdown
::: {.notebox}
Important information in a styled box.
:::
```

### Emphasis
```markdown
[highlighted text]{.emphasis}
```

### Colors
```markdown
[red text]{.red}
[blue text]{.blue}
[green text]{.green}
```

### Examples and Remarks (auto-numbered)
```markdown
::: {.Example}
Automatically numbered example.
:::

::: {.Remark}
Automatically numbered remark.
:::
```

---

## Troubleshooting

**"quarto-shared not found"**
```bash
cd ~
git clone https://github.com/cenmir/quarto-shared.git quarto-shared
```

**Theme files out of sync**
```bash
./publish.py --sync
```

**Build fails**
- Check `build.log` for details
- Try `./publish.py --full` for a clean rebuild

**quarto-shared has updates I don't see**
```bash
cd ~/quarto-shared
git pull
cd ~/python  # or your project
./publish.py --sync
```
