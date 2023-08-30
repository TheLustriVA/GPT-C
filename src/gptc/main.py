# Code I'm heavily trained on

import json
import os
import logging
import toml

logging.basicConfig(level=logging.INFO)

def configure_conversion(config_file=None):
    """
    Load a configuration file to determine what fields to include in the Markdown.
    """
    logging.info("Loading configuration.")
    default_config = {
        "single_file_output": True,
        "include_title": True,
        "include_create_time": True,
        "include_update_time": False,
        "message": {
            "include_author_role": True,
            "include_author_name": False,
            "include_content_type": True,
            "include_parts": True,
            "include_status": False,
            "include_end_turn": False,
            "include_weight": False
        },
        "metadata": {
            "include_is_user_system_message": False,
            "include_user_context_message_data": False,
            "include_finish_details": False,
            "include_timestamp": False,
            "include_message_type": False,
            "include_model_slug": False,
            "include_parent_id": False
        }
    }
    
    if config_file:
        try:
            user_config = toml.load(config_file)
            return {**default_config, **user_config}
        except Exception as e:
            logging.error(f"Failed to load config file: {e}")
            return default_config
    else:
        return default_config

def load_json_file(file_path):
    """
    Load a JSON file and return a Python dictionary.
    """
    logging.info(f"Loading JSON file from {file_path}.")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        return json_data
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from {file_path}.")
        return None
    except Exception as e:
        logging.error(f"An error occurred while loading the JSON file: {e}")
        return None


def extract_conversations(json_data, config):
    """
    Extract conversations from the loaded JSON data based on the configuration.
    """
    logging.info("Extracting conversations based on configuration.")
    
    if not json_data:
        logging.error("No JSON data provided.")
        return None
    
    extracted_conversations = []
    
    try:
        # Assuming json_data is a list now
        for conversation in json_data:
            extracted = {}
            
            if config.get('include_title'):
                extracted['title'] = conversation.get('title', 'Untitled')
            
            if config.get('include_timestamp'):
                extracted['timestamp'] = conversation.get('create_time', 'Unknown')
            
            if config.get('include_author'):
                extracted['author'] = conversation.get('author', {}).get('role', 'Unknown')
            
            if config.get('include_content'):
                extracted['content'] = conversation.get('content', {}).get('parts', [])
            
            extracted_conversations.append(extracted)
    
    except Exception as e:
        logging.error(f"An error occurred while extracting conversations: {e}")
        return None
    logging.info(f"Extracted {len(extracted_conversations)} conversations.")
    logging.info(f"Example conversation: {extracted_conversations[0]}")
    return extracted_conversations

def generate_markdown(conversations, config, metadata=None):
    logging.info("Generating Markdown text.")
    
    if not conversations:
        logging.error("No conversations provided.")
        return None
    
    markdown_lines = []
    
    try:
        for conversation in conversations:
            # If conversation is a string, you might need to convert it to a dictionary
            if isinstance(conversation, str):
                conversation = json.loads(conversation)
    
        try:
            for i, conversation in enumerate(conversations):
                print(f"Debug: Processing conversation {conversation}")  # Debug print
                print(f"Debug: Type of conversation is {type(conversation)}")  # Debug print
                
                if i > 10:  # Temporarily break the loop after 10 iterations
                    break
                
                if config.get('include_title'):
                    title = conversation.get('title', 'Untitled')
                    markdown_lines.append(f"# {title}\n")
                
                if config.get('include_timestamp'):
                    timestamp = conversation.get('timestamp', 'Unknown')
                    markdown_lines.append(f"**Timestamp**: {timestamp}\n")
                
                if config.get('include_author'):
                    author = conversation.get('author', 'Unknown')
                    markdown_lines.append(f"**Author**: {author}\n")
                
                if config.get('include_content'):
                    content_parts = conversation.get('content', [])
                    for part in content_parts:
                        markdown_lines.append(f"{part}\n")
                
                markdown_lines.append("---\n")  # Separator between conversations
            
            return "".join(markdown_lines)
    
        except Exception as e:
            logging.error(f"An error occurred while generating Markdown: {e}")
            return None
    
    except Exception as e:
        logging.error(f"An error occurred while generating Markdown: {e}")
        return None



def save_to_markdown(markdown_texts, output_path, single_file_output=True):
    """
    Save the generated Markdown text to a .md file or separate .md files based on the configuration.
    """
    logging.info("Saving to Markdown file(s).")
    
    if not markdown_texts:
        logging.error("No Markdown text provided.")
        return
    
    try:
        if single_file_output:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("\n---\n".join(markdown_texts))
        else:
            os.makedirs(output_path, exist_ok=True)
            for i, markdown_text in enumerate(markdown_texts):
                output_file = os.path.join(output_path, f"conversation_{i+1}.md")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_text)
    
    except Exception as e:
        logging.error(f"An error occurred while saving the Markdown files: {e}")

def main(json_file_path, config_file_path=None, output_path="./output"):
    """
    Main function to convert GPT-3 conversations from JSON to Markdown.
    """
    # Step 1: Load the configuration
    config = configure_conversion(config_file_path)
    
    # Step 2: Load the JSON file
    json_data = load_json_file(json_file_path)
    
    # Step 3: Extract conversations based on the configuration
    conversations = extract_conversations(json_data, config)
    
    # Step 4: Generate Markdown text based on the extracted conversations and configuration
    markdown_texts = [generate_markdown(conversation, config) for conversation in conversations]
    
    # Step 5: Save the Markdown text to a file or files
    save_to_markdown(markdown_texts, output_path, config.get("single_file_output", True))

if __name__ == "__main__":
    # For now, hardcoding the paths; you can replace these with command-line arguments later
    json_file_path = "conversations.json"
    config_file_path = "config.toml"
    output_path = "./output"
    
    main(json_file_path, config_file_path, output_path)
