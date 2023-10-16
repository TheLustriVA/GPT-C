import os
import json
from pathlib import Path
import re
import html
import icecream as ic 

icecream = ic.IceCreamDebugger()
icecream.disable()

def post_process_md_file(md_filename):
    """post_process the file to remove consecutive empty lines, add 'text' to the start
    code blocks that don't have a language specified, punctuation at the end of 
    headings"""

    # Read in the file
    with open(md_filename, "r") as f:
        md_text = f.read()

    # Remove consecutive empty lines
    md_text = re.sub(r"\n{3,}", "\n\n", md_text)

    # Add 'text' to the start of code blocks that don't have a language specified
    md_text = re.sub(r"```([^`\n]+)\n", r"```text\n", md_text)

    # Add punctuation at the end of headings
    md_text = re.sub(r"#+\s+([^\n]+)(?<![\.\?!:])$", r"# \1.", md_text, flags=re.MULTILINE)

    # Write the processed text back to the file
    with open(md_filename, "w") as f:
        f.write(md_text)

def process_json_file(filename):
    """Read in a JSON file and output individual Markdown files"""

    with open(filename, "r") as f:
        data = json.load(f)

    parent_dir = Path(filename).parent
    subdirectory = Path(filename).stem

    # Loop over items in the root level

    for i, item in enumerate(data):
        title = item["title"]

        # Create a subdirectory from the source file at filename
        try:
            filename = f"{title.lower().replace(' ', '_')}.md"
        except AttributeError as att:
            filename = f"{str(i)}.md"
            print(att)

        # Create the directory for the file if it doesn't exist

        filepath = parent_dir / subdirectory / filename

        os.makedirs(filepath.parent, exist_ok=True)

        # Write the header for the document

        title_newline = "\n\n"

        with open(filepath, "w") as f:
            f.write(f"# {title}{title_newline}")

        # Recursively loop over nested objects and write them out

        process_nested_object("", 1, filepath, item)
        icecream(filepath)
        post_process_md_file(filepath)


def process_nested_object(prefix, depth, filepath, obj):
    """Recursively iterate over nested objects and write them out"""

    for key, value in obj.items():
        if isinstance(value, dict):
            new_prefix = prefix + "-" + key.lower()

            process_nested_object(new_prefix, depth + 1, filepath, value)

        else:
            # Add leading newline for all but top-level headers

            lead_newline = "" if depth == 1 else "\n"

            line = "{}{}: {}\n".format(lead_newline, "-".join([prefix, key]), value)

            newline = "\n"

            # Append the line to the file
            strings_to_check = [
                "message-content-parts:",
                "message-author-role: assistant",
                "message-author-role: user"
                ]

            if any(s in line for s in strings_to_check):
                if isinstance(value, list):
                    for sent_message in value:
                        with open(filepath, "a") as f:
                            f.write(f"{newline}{str(sent_message)}")
                else:
                    with open(filepath, "a") as f:
                        f.write(f"{newline}{newline}{str(value).upper()} >>{newline}")

if __name__ == "__main__":
    filename = "conversations.json"

    process_json_file(filename)
