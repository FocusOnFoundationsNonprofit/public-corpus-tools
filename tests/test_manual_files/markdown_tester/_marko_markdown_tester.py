import marko
import os
#DOESN'T WORK

def read_complete_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_complete_text(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def get_heading_level(element):
    return element.level if isinstance(element, marko.block.Heading) else None

def find_heading_content(doc, heading_text):
    content = []
    found_heading = False
    target_level = None

    for element in doc.children:
        if isinstance(element, marko.block.Heading) and element.children[0].children == heading_text:
            found_heading = True
            target_level = element.level
            continue
        if found_heading:
            if isinstance(element, marko.block.Heading) and element.level <= target_level:
                break
            content.append(element)

    return content

def get_heading(file_path, heading_text):
    complete_text = read_complete_text(file_path)
    doc = marko.parse(complete_text)
    content = find_heading_content(doc, heading_text)
    if content:
        temp_doc = marko.block.Document()
        temp_doc.children = content
        return marko.render(temp_doc)
    return "No content found under this heading."

def set_heading(file_path, new_text, heading_text):
    complete_text = read_complete_text(file_path)
    doc = marko.parse(complete_text)
    new_content = []
    found_heading = False
    for element in doc.children:
        if isinstance(element, marko.block.Heading) and element.children[0].children == heading_text:
            new_content.append(element)
            new_content.extend(marko.parse(new_text).children)
            found_heading = True
        elif found_heading and isinstance(element, marko.block.Heading) and element.level <= get_heading_level(new_content[0]):
            found_heading = False
            new_content.append(element)
        elif not found_heading:
            new_content.append(element)
    
    if not found_heading:
        new_heading = marko.block.Heading()
        new_heading.level = 1
        new_heading.children = [marko.inline.RawText(heading_text)]
        new_content.append(new_heading)
        new_content.extend(marko.parse(new_text).children)
    
    temp_doc = marko.block.Document()
    temp_doc.children = new_content
    write_complete_text(file_path, marko.render(temp_doc))

def delete_heading(file_path, heading_text):
    complete_text = read_complete_text(file_path)
    doc = marko.parse(complete_text)
    new_content = []
    skip = False
    for element in doc.children:
        if isinstance(element, marko.block.Heading) and element.children[0].children == heading_text:
            skip = True
        elif skip and isinstance(element, marko.block.Heading) and element.level <= get_heading_level(element):
            skip = False
            new_content.append(element)
        elif not skip:
            new_content.append(element)
    
    temp_doc = marko.block.Document()
    temp_doc.children = new_content
    write_complete_text(file_path, marko.render(temp_doc))

def list_headings(file_path):
    complete_text = read_complete_text(file_path)
    doc = marko.parse(complete_text)
    headings = []
    for element in doc.children:
        if isinstance(element, marko.block.Heading):
            headings.append(f"{'#' * element.level} {element.children[0].children}")
    return headings

def main():
    file_path = input("Enter the path to your Markdown file: ")
    
    while True:
        print("\nMarkdown Heading Tester (using Marko)")
        print("1. List all headings")
        print("2. Get content under a heading")
        print("3. Set/Replace heading content")
        print("4. Delete a heading")
        print("5. View current file content")
        print("6. Quit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            headings = list_headings(file_path)
            print("\nHeadings in the file:")
            for heading in headings:
                print(f"- {heading}")
        
        elif choice == '2':
            headings = list_headings(file_path)
            print("\nAvailable headings:")
            for i, heading in enumerate(headings, 1):
                print(f"{i}. {heading}")
            index = int(input("Enter the number of the heading to get content from: ")) - 1
            if 0 <= index < len(headings):
                heading_text = headings[index].split(' ', 1)[1]
                result = get_heading(file_path, heading_text)
                print(f"\nContent under '{headings[index]}':\n{result}")
            else:
                print("Invalid heading number.")
        
        elif choice == '3':
            headings = list_headings(file_path)
            print("\nAvailable headings:")
            for i, heading in enumerate(headings, 1):
                print(f"{i}. {heading}")
            print(f"{len(headings) + 1}. Add a new heading")
            index = int(input("Enter the number of the heading to set/replace (or add new): ")) - 1
            if 0 <= index <= len(headings):
                if index == len(headings):
                    new_heading = input("Enter the new heading (including '#' symbols): ")
                    heading_text = new_heading.split(' ', 1)[1]
                else:
                    heading_text = headings[index].split(' ', 1)[1]
                new_content = input("Enter the new content for this heading: ")
                set_heading(file_path, new_content, heading_text)
                print(f"Heading '{heading_text}' has been set/replaced with new content.")
            else:
                print("Invalid heading number.")
        
        elif choice == '4':
            headings = list_headings(file_path)
            print("\nAvailable headings:")
            for i, heading in enumerate(headings, 1):
                print(f"{i}. {heading}")
            index = int(input("Enter the number of the heading to delete: ")) - 1
            if 0 <= index < len(headings):
                heading_text = headings[index].split(' ', 1)[1]
                delete_heading(file_path, heading_text)
                print(f"Heading '{headings[index]}' and its content have been deleted.")
            else:
                print("Invalid heading number.")
        
        elif choice == '5':
            content = read_complete_text(file_path)
            print("\nCurrent file content:")
            print(content)
        
        elif choice == '6':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()