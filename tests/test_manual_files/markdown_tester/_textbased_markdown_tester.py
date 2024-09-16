import os
# THIS WORKS - but might be the same as the existing, doesn't use any python parser or package

def read_complete_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_complete_text(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def get_heading_level(heading):
    return len(heading.split()[0])  # Count '#' symbols in the first word

def find_heading_text(full_text, heading):
    lines = full_text.split('\n')
    start_index = -1
    end_index = -1
    
    for i, line in enumerate(lines):
        if line.strip() == heading.strip():
            start_index = i
            break
    
    if start_index != -1:
        for i in range(start_index + 1, len(lines)):
            if lines[i].strip().startswith('#'):
                end_index = i
                break
        if end_index == -1:
            end_index = len(lines)
        return '\n'.join(lines[start_index+1:end_index]).strip()
    return None

def get_heading(file_path, heading):
    complete_text = read_complete_text(file_path)
    return find_heading_text(complete_text, heading)

def set_heading(file_path, new_text, heading):
    complete_text = read_complete_text(file_path)
    lines = complete_text.split('\n')
    start_index = -1
    end_index = -1
    
    for i, line in enumerate(lines):
        if line.strip() == heading.strip():
            start_index = i
            break
    
    if start_index != -1:
        for i in range(start_index + 1, len(lines)):
            if lines[i].strip().startswith('#'):
                end_index = i
                break
        if end_index == -1:
            end_index = len(lines)
        lines[start_index+1:end_index] = new_text.split('\n')
    else:
        lines.append(heading)
        lines.extend(new_text.split('\n'))
    
    write_complete_text(file_path, '\n'.join(lines))

def delete_heading(file_path, heading):
    complete_text = read_complete_text(file_path)
    lines = complete_text.split('\n')
    start_index = -1
    end_index = -1
    
    for i, line in enumerate(lines):
        if line.strip() == heading.strip():
            start_index = i
            break
    
    if start_index != -1:
        for i in range(start_index + 1, len(lines)):
            if lines[i].strip().startswith('#'):
                end_index = i
                break
        if end_index == -1:
            end_index = len(lines)
        del lines[start_index:end_index]
        write_complete_text(file_path, '\n'.join(lines))
        return True
    return False

def list_headings(file_path):
    complete_text = read_complete_text(file_path)
    headings = []
    for line in complete_text.split('\n'):
        if line.strip().startswith('#'):
            headings.append(line.strip())
    return headings

def main():
    file_path = input("Enter the path to your Markdown file: ")
    
    while True:
        print("\nMarkdown Heading Tester")
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
                result = get_heading(file_path, headings[index])
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
                else:
                    new_heading = headings[index]
                new_content = input("Enter the new content for this heading: ")
                set_heading(file_path, new_content, new_heading)
                print(f"Heading '{new_heading}' has been set/replaced with new content.")
            else:
                print("Invalid heading number.")
        
        elif choice == '4':
            headings = list_headings(file_path)
            print("\nAvailable headings:")
            for i, heading in enumerate(headings, 1):
                print(f"{i}. {heading}")
            index = int(input("Enter the number of the heading to delete: ")) - 1
            if 0 <= index < len(headings):
                if delete_heading(file_path, headings[index]):
                    print(f"Heading '{headings[index]}' and its content have been deleted.")
                else:
                    print(f"Failed to delete heading '{headings[index]}'.")
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