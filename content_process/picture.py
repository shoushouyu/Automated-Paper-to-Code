import os 
import re

from volcenginesdkarkruntime import Ark

def describe_images_in_markdown(
    input_md_path: str,
    output_md_path: str,
    model: str = "doubao-1.5-vision-pro-32k-250115" #or other gpt models,such as gpt-4o
):
    """
    Retrieve all image URLs from the specified Markdown file,
    call a large model to obtain image descriptions (also sending the entire paper content).
    If the model returns "no", indicating that the image cannot be described,
    then do not insert any description.
    Finally, write the modified content to a new file.
    """
    
    
    client = Ark(api_key=os.getenv("ARK_API_KEY"))
    
    
    with open(input_md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    
    pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')

    # Cache image descriptions that have already been requested to avoid repeated calls
    url_to_description = {}

    
    def replace_func(match: re.Match) -> str:
        alt_text = match.group(1)  # Original alt text
        img_url  = match.group(2)  # Image URL

        # If a description for this URL has not been obtained, call the model
        if img_url not in url_to_description:
            # Construct the message to be sent to the model.
            # Send the entire paper content along with the image URL.
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Based on the paper content and your visual understanding of the image, please provide a complete description of the image, with an emphasis on numerical details. "
                                "Note that your response should contain a comprehensive description of the image's information without any omissions (especially all details related to the model architecture), and it should not include any analysis of colors.\n"
                                "Below is the full paper content:\n\n"
                                f"{md_content}\n\n"
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": img_url}
                        }
                    ]
                }
            ]

            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            description = response.choices[0].message.content.strip()
            url_to_description[img_url] = description


        description = url_to_description[img_url]
        
        
        if description.lower() == "no":
            return f'![{alt_text}]({img_url})'
        else:
            
            new_markdown = f'![{alt_text}]({img_url})\n\n> **Picture description**: {description}\n'
            return new_markdown

    
    new_md_content = pattern.sub(replace_func, md_content)

    
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(new_md_content)


if __name__ == "__main__":
    # Path to your paper's Markdown file
    input_path = "paper_markdown/paper.md"
    # Path to write the results (can be a new file or overwrite the existing one)
    output_path = "paper_markdown/paper.md"
    
    describe_images_in_markdown(input_path, output_path)
    print(f"Generation completed, the processed content has been written to {output_path}")
