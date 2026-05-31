# Beauty Content Kit

Beauty Content Kit is a small command-line toolkit for creating short-video topic
angles for beauty creators, especially eyebrow, eye, and lip-blushing studios.

It is designed for creators who need practical, trust-first content prompts
instead of generic marketing copy. The project focuses on:

- short-video hooks
- local-store trust building
- client concern framing
- safe wording for beauty and facial-feature topics
- reusable angle banks for eyebrow, eye, and lip content

## Why this exists

Many beauty creators know their craft, but struggle to turn that expertise into
daily content. This tool helps generate structured topic ideas that can become
Douyin, Xiaohongshu, WeChat Channels, or Instagram Reels scripts.

The wording avoids hard claims such as guaranteed luck, personality verdicts, or
medical-style promises. It keeps the language framed as first impression,
aesthetic judgment, client concerns, and professional consultation.

## Install for local development

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
```

## Usage

Generate five lip-blushing topic ideas:

```bash
beauty-content-kit generate --feature lip --count 5
```

Generate eyebrow ideas in JSON:

```bash
beauty-content-kit generate --feature brow --count 3 --format json
```

Generate ideas for all supported features:

```bash
beauty-content-kit generate --feature all --count 9
```

## Example output

```text
1. 纹唇师说真话：为什么有些嘴唇当场很红，后期却留不住色？
   Angle: client concern
   CTA: 想知道自己适不适合做，先发素颜唇部照片做判断。
```

## Supported features

- `lip`
- `brow`
- `eye`
- `all`

## Development

Run tests:

```bash
python3 -m pytest
```

Run lint-free syntax checks:

```bash
python3 -m compileall src tests
```

## Roadmap

- Add English prompt templates.
- Add script-outline generation.
- Add CSV export for content calendars.
- Add more safe-language filters.
- Add examples for local beauty studios.

## Contributing

Issues and pull requests are welcome. Please keep examples practical, respectful,
and safe for real client communication.

## License

MIT
