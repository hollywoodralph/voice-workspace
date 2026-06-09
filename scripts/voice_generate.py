#!/usr/bin/env python3
"""
Voice synthesis wrapper for OmniVoice Studio.
Call from any project or cron job to generate speech.
"""
import sys, os, argparse, requests, json

OMNIVOICE_URL = os.environ.get("OMNIVOICE_URL", "http://localhost:3900")


def generate(text: str, output_path: str, language: str = "en",
             ref_audio: str = None, ref_text: str = None):
    """Generate speech via OmniVoice API."""
    url = f"{OMNIVOICE_URL}/generate"
    files = {"text": (None, text), "language": (None, language)}
    if ref_audio and os.path.exists(ref_audio):
        files["ref_audio"] = ("voice.wav", open(ref_audio, "rb"), "audio/wav")
    if ref_text:
        files["ref_text"] = (None, ref_text)

    r = requests.post(url, files=files, timeout=300)
    if r.status_code != 200:
        print(f"Error: HTTP {r.status_code} — {r.text}", file=sys.stderr)
        sys.exit(1)
    with open(output_path, "wb") as f:
        f.write(r.content)
    size = os.path.getsize(output_path)
    print(f"Generated: {output_path} ({size} bytes)")


def health():
    r = requests.get(f"{OMNIVOICE_URL}/health", timeout=10)
    print(json.dumps(r.json(), indent=2))


def engines():
    r = requests.get(f"{OMNIVOICE_URL}/engines", timeout=10)
    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Voice synthesis via OmniVoice")
    sub = parser.add_subparsers(dest="cmd")

    gen = sub.add_parser("generate", help="Generate speech")
    gen.add_argument("--text", "-t", required=True)
    gen.add_argument("--output", "-o", required=True)
    gen.add_argument("--lang", "-l", default="en")
    gen.add_argument("--ref-audio", help="Voice clone reference audio")
    gen.add_argument("--ref-text", help="Reference audio transcript")

    sub.add_parser("health", help="Check server health")
    sub.add_parser("engines", help="List engines")

    args = parser.parse_args()
    if args.cmd == "generate":
        generate(args.text, args.output, args.lang, args.ref_audio, args.ref_text)
    elif args.cmd == "health":
        health()
    elif args.cmd == "engines":
        engines()
    else:
        parser.print_help()
