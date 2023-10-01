# Code I'm heavily trained on

import json
import os
import logging
import toml

json_file_path = "src/gptc/conversations.json"
config_file_path = "src/gptc/config.toml"
output_path = "src/gptc/outputs"

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
            user_config = toml.load(config_file_path)
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
    logging.info("Extracting conversations based on configuration.")
    
    if not isinstance(json_data, list):
        logging.error("JSON data is not a list.")
        return None
    
    logging.info(f"json_data: {json_data}")
    
    extracted_conversations = []
    
    try:
        for conversation in json_data:
            logging.info(f"Processing conversation {conversation}")
            extracted = {}
            
            # Include options for conversation
            if config.get('include_title', False):
                extracted['title'] = conversation.get('title', 'Untitled')

            if config.get('include_create_time', False):
                extracted['create_time'] = conversation.get('create_time', 'Unknown')

            if config.get('include_update_time', False):
                extracted['update_time'] = conversation.get('update_time', 'Unknown')

            # Include options for messages
            message_config = config.get('message', {})
            if message_config.get('include_author_role', False):
                extracted['author_role'] = conversation.get('author', {}).get('role', 'Unknown')

            if message_config.get('include_author_name', False):
                extracted['author_name'] = conversation.get('author', {}).get('name', 'Unknown')

            if message_config.get('include_content_type', False):
                extracted['content_type'] = conversation.get('content', {}).get('type', 'Unknown')

            if message_config.get('include_parts', False):
                extracted['parts'] = conversation.get('content', {}).get('parts', [])

            if message_config.get('include_status', False):
                extracted['status'] = conversation.get('status', 'Unknown')

            if message_config.get('include_end_turn', False):
                extracted['end_turn'] = conversation.get('end_turn', 'Unknown')

            if message_config.get('include_weight', False):
                extracted['weight'] = conversation.get('weight', 'Unknown')

            # Metadata options
            metadata_config = config.get('metadata', {})
            if metadata_config.get('include_is_user_system_message', False):
                extracted['is_user_system_message'] = conversation.get('is_user_system_message', 'Unknown')

            if metadata_config.get('include_user_context_message_data', False):
                extracted['user_context_message_data'] = conversation.get('user_context_message_data', 'Unknown')

            if metadata_config.get('include_finish_details', False):
                extracted['finish_details'] = conversation.get('finish_details', 'Unknown')

            if metadata_config.get('include_timestamp', False):
                extracted['timestamp'] = conversation.get('timestamp', 'Unknown')

            if metadata_config.get('include_message_type', False):
                extracted['message_type'] = conversation.get('message_type', 'Unknown')

            if metadata_config.get('include_model_slug', False):
                extracted['model_slug'] = conversation.get('model_slug', 'Unknown')

            if metadata_config.get('include_parent_id', False):
                extracted['parent_id'] = conversation.get('parent_id', 'Unknown')
            
            extracted_conversations.append(extracted)
    
    except Exception as e:
        logging.error(f"An error occurred while extracting conversations: {e}")
        return None
    logging.info(f"extracted_conversations: {extracted_conversations}")
    return extracted_conversations

def generate_markdown(conversations, config, metadata=None):
    logging.info("Generating Markdown text.")
    
    if not conversations:
        logging.error("No conversations provided.")
        return None
    
    markdown_lines = []
    
    try:
        # This is where the 'conversations' variable is sent to file
        convo_check_dump = (f"Conversations: {type(conversations)} --> {conversations}")
        with open("convo_dump.txt", "a", encoding="utf-8") as dump:
            dump.write(convo_check_dump)
            dump.write("\n")
        for idx, conversation in enumerate(conversations):
            logging.info(f"Processing conversation {type(conversation)} --> {conversation}")
            # If conversation is a string, you might need to convert it to a dictionary
            if idx > 10:
                break
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

def get_json_sample(json_path: str, sample_size: int=10) -> None:
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    for idx, conversation in enumerate(json_data):
        if idx == sample_size:
            break
        with open("json_sample.json", 'w', encoding='utf-8') as f:
            json.dump(conversation, f, indent=4)

def save_to_markdown(markdown_texts, output_path, single_file_output=False):
    """
    Save the generated Markdown text to a .md file or separate .md files based on the configuration.
    """
    logging.info("Saving to Markdown file(s).")
    
    if not markdown_texts:
        logging.error("No Markdown text provided.")
        return
    
    try:
        if single_file_output:
            logging.info("Single file output.")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("\n---\n".join(markdown_texts))
        else:
            logging.info("Multiple file output.")
            os.makedirs(output_path, exist_ok=True)
            for i, markdown_text in enumerate(markdown_texts):
                logging.info(f"Saving: {markdown_text}")
                if i > 10:
                    break
                output_file = os.path.join(output_path, f"conversation_{i+1}.md")
                logging.info(f"Saving to {output_file}.")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_text)
    
    except Exception as e:
        logging.error(f"An error occurred while saving the Markdown files: {e}")

def main(json_file_path, config_file_path=None, output_path="./output"):
    config = configure_conversion(config_file_path)
    json_data = load_json_file(json_file_path)
    conversations = extract_conversations(json_data, config)
    markdown_texts = generate_markdown(conversations, config)
    save_to_markdown(markdown_texts, output_path, config.get("single_file_output"))

if __name__ == "__main__":
    main(json_file_path, config_file_path, output_path)