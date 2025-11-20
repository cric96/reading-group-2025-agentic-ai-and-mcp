import subprocess
import http.server
import socketserver
import os
import argparse

PORT = 8089
NOTEBOOK_FILE = "presentation.ipynb"
HTML_FILE = "presentation"
CSS_FILE = "rise.css"

def convert_notebook_to_slides():
    """Converts the Jupyter notebook to slides using nbconvert."""
    try:
        subprocess.run(
            [
                "jupyter",
                "nbconvert",
                NOTEBOOK_FILE,
                "--to",
                "slides",
                "--output",
                HTML_FILE.replace(".html", ""),
                "--SlidesExporter.reveal_theme=simple",
                "--SlidesExporter.reveal_scroll=True",
                "--SlidesExporter.reveal_transition=slide",
                "--SlidesExporter.reveal_controls=True",
                "--SlidesExporter.reveal_progress=True",
                "--SlidesExporter.reveal_width=1920",
                "--SlidesExporter.reveal_height=1080",
            ],
            check=True,
        )
        print(f"Successfully converted {NOTEBOOK_FILE} to {HTML_FILE}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return False
    except FileNotFoundError:
        print("Error: 'jupyter' command not found. Make sure Jupyter is installed and in your PATH.")
        return False

def link_css_in_html():
    """Links the CSS file in the HTML file."""
    if not os.path.exists(HTML_FILE + ".slides.html"):
        print(f"Error: {HTML_FILE}.slides.html not found.")
        return False

    with open(HTML_FILE + ".slides.html", "r") as f:
        html_content = f.read()

    # Inject CSS link into the <head> section
    link_tag = f'<link rel="stylesheet" href="{CSS_FILE}">'
    if "</head>" in html_content:
        html_content = html_content.replace("</head>", f"{link_tag}</head>")
    else:
        # Fallback if no </head> tag is found
        html_content = f"<html><head>{link_tag}</head><body>{html_content}</body></html>"

    with open(HTML_FILE + ".slides.html", "w") as f:
        f.write(html_content)
    
    print(f"Successfully linked {CSS_FILE} in {HTML_FILE}.slides.html")
    return True

def serve_slides(port=PORT):
    """Serves the generated slides on a local server."""
    if not os.path.exists(HTML_FILE + ".slides.html"):
        print(f"Error: {HTML_FILE}.slides.html not found. Please run the conversion first.")
        return

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving slides at http://localhost:{port}/{HTML_FILE}.slides.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping the server.")
            httpd.shutdown()  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert notebook to slides and optionally serve them.")
    parser.add_argument("--serve", action="store_true", help="Serve the slides locally after conversion.")
    parser.add_argument("--port", type=int, default=PORT, help=f"Port to serve slides on (default: {PORT})")
    args = parser.parse_args()

    if convert_notebook_to_slides():
        if link_css_in_html():
            if args.serve:
                serve_slides(args.port)