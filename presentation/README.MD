# 🎨 Streamlit Workshop — Presentation

Slide deck for the **Streamlit Workshop**, built with [mkslides](https://github.com/MartenBE/mkslides).

---

## 📁 Structure

- `slides/` — Markdown source files for the presentation
- `slides/images/` — Images used in the slides
- `site/` — Generated output (do not edit manually)

---

## 👀 Viewing the slides

The built slides are in `site/`. Open `site/index.html` in a browser, or use the dev server (see below).

---

## 🛠️ Development

### Prerequisites

Install dependencies via [uv](https://github.com/astral-sh/uv):

```sh
uv sync
```

### Build to `site/`

```sh
uv run mkslides build presentation/slides -d presentation/site
```

### Serve locally (with live reload)

```sh
uv run mkslides serve presentation/slides
```

Opens at `http://localhost:8000` by default.

---

## ✏️ Editing slides

- Edit [`slides/presentation.md`](slides/presentation.md)
- Slides are separated by `---`
- Supports standard Markdown, HTML, and Reveal.js features (themes, fragments, etc.)
