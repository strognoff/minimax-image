# MiniMax Text-to-Image

Generate images from text prompts using MiniMax's Image-01 model.

## Setup

```bash
# Install dependencies
pip install requests

# Set your API key
export MINIMAX_API_KEY="your-api-key-here"
```

Or pass the API key directly:
```bash
python3 minimax_image.py "your prompt" --api_key "your-key"
```

## Usage

```bash
# Basic usage
python3 minimax_image.py "a beautiful sunset over mountains"

# With output filename
python3 minimax_image.py "a cat" --output cat.png

# Different aspect ratios
python3 minimax_image.py "a logo" --output logo.png --aspect_ratio 1:1
python3 minimax_image.py "a story" --output story.png --aspect_ratio 9:16

# Available aspect ratios: 16:9, 9:16, 1:1, 4:3, 3:4
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--prompt` | Text description of image | (required) |
| `--output` / `-o` | Output filename | `generated_image.png` |
| `--aspect_ratio` / `-a` | Image aspect ratio | `16:9` |
| `--model` / `-m` | Model to use | `image-01` |
| `--response_format` / `-f` | `base64` or `url` | `base64` |
| `--api_key` / `-k` | MiniMax API key | From env `MINIMAX_API_KEY` |

## Example Output

```bash
$ python3 minimax_image.py "a cozy coffee shop, minimal design" --output coffee.png
Generating image with prompt: 'a cozy coffee shop, minimal design'
Aspect ratio: 1:1
Image saved to: coffee.png
```

## Skills Integration

This tool can be used as an OpenClaw skill. See `minimax-image-skill/` directory.

## License

MIT
