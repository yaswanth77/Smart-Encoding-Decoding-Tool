import argparse
import base64
import urllib.parse
import re
import html

def is_base64(text):
    return re.match(r'^[A-Za-z0-9+/]+={0,2}$', text) is not None

def is_url_encoded(text):
    return '%' in text and re.match(r'^[A-Za-z0-9%_.~-]+$', text) is not None

def is_html_encoded(text):
    return '&' in text and ';' in text and re.search(r'&[#a-zA-Z0-9]+;', text) is not None

def encode_base64(text):
    return base64.b64encode(text.encode()).decode()

def decode_base64(text):
    try:
        return base64.b64decode(text).decode()
    except:
        return None

def encode_url(text):
    return urllib.parse.quote(text)

def decode_url(text):
    try:
        return urllib.parse.unquote(text)
    except:
        return None

def encode_html(text):
    return html.escape(text)

def decode_html(text):
    try:
        return html.unescape(text)
    except:
        return None

def suggest_action(text):
    if is_base64(text):
        return "decode", "base64"
    elif is_url_encoded(text):
        return "decode", "url"
    elif is_html_encoded(text):
        return "decode", "html"
    else:
        return "encode", None

def main():
    parser = argparse.ArgumentParser(description="Smart encode or decode text using various methods.")
    parser.add_argument("text", help="The text to encode or decode")
    parser.add_argument("--method", choices=["base64", "url", "html"], help="The encoding/decoding method to use (optional)")

    args = parser.parse_args()

    suggested_action, suggested_method = suggest_action(args.text)

    if args.method:
        method = args.method
    elif suggested_method:
        method = suggested_method
    else:
        method = input("Choose encoding method (base64/url/html): ").lower()
        while method not in ["base64", "url", "html"]:
            method = input("Invalid choice. Please enter 'base64', 'url', or 'html': ").lower()

    action = input(f"Suggested action: {suggested_action}. Do you want to {suggested_action}? (y/n): ").lower()
    if action != 'y':
        action = "encode" if suggested_action == "decode" else "decode"
    else:
        action = suggested_action

    if method == "base64":
        if action == "encode":
            result = encode_base64(args.text)
            operation = "Base64 Encoding"
        else:
            result = decode_base64(args.text)
            operation = "Base64 Decoding"
    elif method == "url":
        if action == "encode":
            result = encode_url(args.text)
            operation = "URL Encoding"
        else:
            result = decode_url(args.text)
            operation = "URL Decoding"
    elif method == "html":
        if action == "encode":
            result = encode_html(args.text)
            operation = "HTML Encoding"
        else:
            result = decode_html(args.text)
            operation = "HTML Decoding"

    print(f"\nInput: {args.text}")
    print(f"Operation: {operation}")
    print(f"Output: {result}")

    if result is None:
        print("Error: Unable to perform the operation. The input may not be valid for the chosen method and action.")

if __name__ == "__main__":
    main()