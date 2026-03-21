#!/usr/bin/env python3
"""
MiniMax Text-to-Image Generator

Usage:
  python minimax_image.py "your prompt here"
  python minimax_image.py "a sunset" --output sunset.png
  python minimax_image.py "a cat" --aspect_ratio "1:1"
  python minimax_image.py "a dog" --model "image-01" --response_format "base64"

Options:
  --prompt        The text description of the image to generate
  --output        Output filename (default: generated_image.png)
  --aspect_ratio  Image aspect ratio: "16:9", "9:16", "1:1", "4:3", "3:4" (default: 16:9)
  --model         Model to use: "image-01" (default: image-01)
  --response_format Output format: "base64" or "url" (default: base64)
  --api_key       MiniMax API key (or set MINIMAX_API_KEY env)
  --api_host      MiniMax API host (default: https://api.minimax.io)
"""

import argparse
import base64
import os
import json
import sys
import requests

DEFAULT_HOST = "https://api.minimax.io"

def generate_image(
    prompt: str,
    output_path: str = "generated_image.png",
    aspect_ratio: str = "16:9",
    model: str = "image-01",
    response_format: str = "base64",
    api_key: str = None,
    api_host: str = DEFAULT_HOST
) -> str:
    """Generate an image from text using MiniMax API."""
    
    if not api_key:
        api_key = os.environ.get("MINIMAX_API_KEY")
        if not api_key:
            raise ValueError("MINIMAX_API_KEY not set. Pass --api_key or set MINIMAX_API_KEY env")
    
    url = f"{api_host}/v1/image_generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": response_format
    }
    
    print(f"Generating image with prompt: '{prompt[:50]}...'", file=sys.stderr)
    print(f"Aspect ratio: {aspect_ratio}", file=sys.stderr)
    
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    
    result = response.json()
    
    if "base_resp" in result and result["base_resp"].get("status_code") != 0:
        raise Exception(f"API error: {result['base_resp'].get('status_msg')}")
    
    if response_format == "base64":
        images = result.get("data", {}).get("image_base64", [])
        if not images:
            raise Exception("No images in response")
        
        # Decode and save the first image
        image_data = base64.b64decode(images[0])
        with open(output_path, "wb") as f:
            f.write(image_data)
        print(f"Image saved to: {output_path}", file=sys.stderr)
        return output_path
    else:
        # URL format
        urls = result.get("data", {}).get("image_urls", [])
        if not urls:
            raise Exception("No URLs in response")
        url_result = urls[0]
        print(f"Image URL: {url_result}", file=sys.stderr)
        return url_result


def main():
    parser = argparse.ArgumentParser(description="MiniMax Text-to-Image Generator")
    parser.add_argument("prompt", help="The text description of the image to generate")
    parser.add_argument("--output", "-o", default="generated_image.png", help="Output filename")
    parser.add_argument("--aspect_ratio", "-a", default="16:9", 
                        choices=["16:9", "9:16", "1:1", "4:3", "3:4"],
                        help="Image aspect ratio (default: 16:9)")
    parser.add_argument("--model", "-m", default="image-01", help="Model to use (default: image-01)")
    parser.add_argument("--response_format", "-f", default="base64", choices=["base64", "url"],
                        help="Response format (default: base64)")
    parser.add_argument("--api_key", "-k", default=None, help="MiniMax API key")
    parser.add_argument("--api_host", default=DEFAULT_HOST, help="MiniMax API host")
    
    args = parser.parse_args()
    
    # Check for MINIMAX_API_KEY in env if not passed
    if not args.api_key:
        args.api_key = os.environ.get("MINIMAX_API_KEY")
    
    try:
        result = generate_image(
            prompt=args.prompt,
            output_path=args.output,
            aspect_ratio=args.aspect_ratio,
            model=args.model,
            response_format=args.response_format,
            api_key=args.api_key,
            api_host=args.api_host
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
