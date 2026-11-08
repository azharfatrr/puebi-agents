# PUEBI

**English** | [<kbd>Bahasa Indonesia</kbd>](README.id.md)

An agent skill for checking Indonesian spelling against **EYD V**, the standard that replaced PUEBI. It can proofread existing text or guide new writing. When drafting, it prefers familiar loanwords over rare native coinages.

In review and fix modes, it corrects spelling without changing what the text says. In rewrite mode, it may also reorganize sentences for clarity.

> [!WARNING]
> **Disclaimer:** This project is maintained by a developer, not a linguist or language professional. The rules and examples were transcribed from the official EYD V website, and mistakes may remain. Verify important corrections against the official EYD V site or KBBI. Contributions from language professionals are welcome.

## What it does

The skill corrects spelling without changing what the text says in review and fix modes. It covers letters, capitalization, italics, bold, word formation, affixes, reduplication, compounds, prepositions, particles, abbreviations, acronyms, numbers, pronouns, articles, punctuation, and loanword absorption.

It follows **EYD V** (Ejaan Bahasa Indonesia yang Disempurnakan, fifth edition), set out in Keputusan Kepala Badan Pengembangan dan Pembinaan Bahasa Nomor 0424/I/BS.00.01/2022 on 16 August 2022. PUEBI remains the familiar name, so it stays in the project title.

## Before and after

**Before:**

> ## 5 Tips Menulis Yang Baik.
>
> Menulis adalah keterampilan yang penting , baik untuk pekerjaan maupun kehidupan sehari hari. Banyak orang menganggap bahwa menulis hanya untuk penulis professional, padahal setiap orang bisa menulis.
>
> Apapun profesi anda, luangkan waktu 15 menit setiap hari untuk menulis.

**After:**

> ## 5 Tips Menulis yang Baik
>
> Menulis adalah keterampilan yang penting, baik untuk pekerjaan maupun kehidupan sehari-hari. Banyak orang menganggap bahwa menulis hanya untuk penulis profesional, padahal setiap orang bisa menulis.
>
> Apa pun profesi Anda, luangkan waktu 15 menit setiap hari untuk menulis.

During pure proofreading, the skill keeps the writer's words. The loanword preference applies when writing, rewriting, or choosing terms. For example, `prototipe` may be easier to recognize than `purwarupa`, but terminology required by the user or a document comes first. See [`references/09-pilihan-kata.md`](references/09-pilihan-kata.md).

## Install

Requires Node.js 22.20 or newer for `npx skills` and Python 3.9 or newer for the scripts.

From this repository:

```bash
npx skills add . --global --agent '*'
```

After publication, replace `.` with the repository name:

```bash
npx skills add <owner>/<repo> --global --agent '*'
```

To install only for one agent, replace `'*'` with a name such as `claude-code` or `codex`. You can also copy this directory into an agent skill directory, such as `~/.config/opencode/skills/puebi` or `~/.claude/skills/puebi`.

Then install the slash command:

```bash
python scripts/install_commands.py --global --agent both
```

Use `--agent opencode` or `--agent claude` for one agent. To install into a specific project, add `--scope project --project-dir <path>`. The installer does not overwrite existing commands unless you pass `--force`.

The Claude Code plugin adds the command `/puebi:puebi`. Use the global `/puebi` command for the short name.

## Command

There is one command: `/puebi`.

| Argument | Behavior |
|---|---|
| no mode | Check spelling without editing files. |
| `review` | Same as no mode. |
| `fix` | Fix spelling with minimal changes. |
| `rewrite` | Rewrite for clarity while fixing spelling. |

Examples:

```text
/puebi docs/guide.md
/puebi review docs/guide.md
/puebi fix "Kami akan meeting besok."
/puebi rewrite report.md
```

You can also ask in plain language:

```text
Fix the spelling in docs/guide.md according to EYD V.
```

## Automated checker

The script finds spelling errors that can be decided without reading the whole sentence:

```bash
python scripts/audit.py text.md
python scripts/audit.py text.md --json
python scripts/audit.py text.md --fix
```

`--fix` applies mechanical fixes. Review the result, especially when a word or number has more than one interpretation. The script skips code blocks, inline code, frontmatter, URLs, email addresses, and link targets. Names, punctuation context, italics, and standard word forms still need human review and KBBI.

Exit code `0` means no findings, `1` means findings remain, and `2` means a file could not be read.

## Tests

```bash
python -m unittest scripts/test_audit.py scripts/test_commands.py -v
python scripts/run_evals.py
python scripts/validate-package.py
```

The cases in `evals/` pair text that needs correction with the expected result. `run_evals.py` checks that the input produces findings and the expected file passes the checker. Agent behavior still needs a manual comparison with the expected files.

## Scope and limits

EYD regulates spelling, not the quality of an entire piece of writing. KBBI determines whether a word form is standard. Grammar, word choice, translation, and fact-checking are separate jobs. If you need the older PUEBI edition, say which edition applies.

## Disclaimer

This project is maintained by a developer, not a linguist or language professional. The rules and examples were transcribed from the official EYD V website, and mistakes may remain. When a correction matters, verify it against the [official EYD V site](https://ejaan.kemendikdasmen.go.id/) or [KBBI](https://kbbi.kemdikbud.go.id/). Corrections from language teachers, editors, translators, and other readers are welcome.

## Contributing

Contributions are welcome, especially from people with a background in Indonesian language, linguistics, editing, or teaching.

- Report a wrong rule, example, or explanation with the rule number and a source link.
- Send a pull request for spelling, wording, or formatting fixes.
- Keep quoted EYD V rules faithful. Explain any change to a rule or example.
- Run the tests before opening a pull request.
- For large changes, open an issue first so the direction can be discussed.

You do not need to be a linguist to contribute. Clear examples and careful proofreading help just as much.

## Sources and license

- [EYD V](https://ejaan.kemendikdasmen.go.id/)
- [Decree](https://ejaan.kemendikdasmen.go.id/eyd/surat-keputusan/)
- [KBBI Daring](https://kbbi.kemdikbud.go.id/)

MIT covers the original code and prose. Copied EYD V material and the CC BY-ND excerpt are excluded; see [NOTICE.md](NOTICE.md).
