from bs4 import BeautifulSoup, Comment, NavigableString
import deepl
import os

# Function to translate text while preserving HTML tags and formatting
def translate_html_element(element, translator, target_lang='PT-BR'):
    if element is None:
        print("The provided element is None.")
        return element

    if not hasattr(element, 'descendants'):
        print("The provided element is not a valid BeautifulSoup object.")
        return element

    # Use a stack to process elements to avoid issues with descendants
    stack = [element]
    while stack:
        current = stack.pop()
        if isinstance(current, Comment):
            continue
        if isinstance(current, NavigableString) and current.strip():
            try:
                # Translate the text while preserving whitespace and formatting
                original_text = current.string
                print(f"Original text: {original_text}")
                translated_text = translator.translate_text(original_text, target_lang=target_lang).text
                print(f"Translated text: {translated_text}")
                current.replace_with(NavigableString(translated_text))
            except Exception as e:
                print(f"Error translating text: {current.string}. Error: {e}")
        elif hasattr(current, 'contents'):
            stack.extend(current.contents)

    return element

# Load the HTML file
file_path = 'D:/Projetos/Empresa sem nome/site/iDocs/translator/Documentation.html'  # Update with the path to your HTML file
if not os.path.isfile(file_path):
    print(f"File not found: {file_path}")
else:
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')  # Try 'html5lib' or 'lxml' if needed

    # Initialize the DeepL translator
    auth_key = "eb5d04cf-8c0c-41cd-ad00-64370c56ad9f:fx"  # Replace with your DeepL API key
    translator = deepl.Translator(auth_key)

    # Translate the textual content within the body tag
    body_content = soup.find('body')
    if body_content:
        translated_body_content = translate_html_element(body_content, translator)

        # Save the translated content back into the HTML structure
        if soup.body:
            soup.body.replace_with(translated_body_content)

            # Write the translated HTML content to a new file
            translated_file_path = 'D:/Projetos/Empresa sem nome/site/iDocs/translator/Translated_Documentation.html'  # Update with the path to save the translated file
            with open(translated_file_path, 'w', encoding='utf-8') as file:
                file.write(soup.prettify(formatter="html"))  # Use prettify with formatter="html" to maintain structure

            print(f"Translated file saved to: {translated_file_path}")
        else:
            print("No <body> tag found in the HTML file.")
    else:
        print("No <body> content found in the HTML file.")
