import panflute as pf
# DOESN'T WORK

def read_markdown(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def write_markdown(file_path, doc):
    with open(file_path, 'w') as f:
        f.write(pf.stringify(doc))

def list_headings(doc):
    headings = []
    for elem in doc.walk(pf.Header):
        try:
            headings.append((elem.level, pf.stringify(elem)))
        except:
            # Skip headers that can't be processed
            pass
    return headings

def get_heading_content(doc, target_level, target_text):
    content = []
    capturing = False
    for elem in doc.content:
        if isinstance(elem, pf.Header):
            if elem.level == target_level and pf.stringify(elem) == target_text:
                capturing = True
            elif capturing and elem.level <= target_level:
                break
        elif capturing:
            content.append(elem)
    return pf.Doc(*content)

def set_heading_content(doc, target_level, target_text, new_content):
    new_doc = []
    found = False
    for elem in doc.content:
        if not found:
            new_doc.append(elem)
            if isinstance(elem, pf.Header) and elem.level == target_level and pf.stringify(elem) == target_text:
                found = True
                new_doc.extend(pf.convert_text(new_content))
        elif isinstance(elem, pf.Header) and elem.level <= target_level:
            found = False
            new_doc.append(elem)
    if not found:
        new_doc.append(pf.Header(pf.Str(target_text), level=target_level))
        new_doc.extend(pf.convert_text(new_content))
    return pf.Doc(*new_doc)

def delete_heading(doc, target_level, target_text):
    new_doc = []
    skipping = False
    for elem in doc.content:
        if isinstance(elem, pf.Header):
            if elem.level == target_level and pf.stringify(elem) == target_text:
                skipping = True
            elif skipping and elem.level <= target_level:
                skipping = False
                new_doc.append(elem)
            elif not skipping:
                new_doc.append(elem)
        elif not skipping:
            new_doc.append(elem)
    return pf.Doc(*new_doc)

def main():
    file_path = input("Enter the path to your Markdown file: ")
    
    while True:
        print("\nMarkdown Heading Tester (using Panflute)")
        print("1. List all headings")
        print("2. Get content under a heading")
        print("3. Set/Replace heading content")
        print("4. Delete a heading")
        print("5. View current file content")
        print("6. Quit")
        
        choice = input("Enter your choice (1-6): ")
        
        try:
            doc = pf.convert_text(read_markdown(file_path), standalone=True)
        except Exception as e:
            print(f"Error reading or parsing the file: {e}")
            continue
        
        if choice == '1':
            headings = list_headings(doc)
            print("\nHeadings in the file:")
            for level, text in headings:
                print(f"{'#' * level} {text}")
        
        elif choice == '2':
            headings = list_headings(doc)
            print("\nAvailable headings:")
            for i, (level, text) in enumerate(headings, 1):
                print(f"{i}. {'#' * level} {text}")
            index = int(input("Enter the number of the heading to get content from: ")) - 1
            if 0 <= index < len(headings):
                level, text = headings[index]
                content = get_heading_content(doc, level, text)
                print(f"\nContent under '{text}':\n{pf.stringify(content)}")
            else:
                print("Invalid heading number.")
        
        elif choice == '3':
            headings = list_headings(doc)
            print("\nAvailable headings:")
            for i, (level, text) in enumerate(headings, 1):
                print(f"{i}. {'#' * level} {text}")
            print(f"{len(headings) + 1}. Add a new heading")
            index = int(input("Enter the number of the heading to set/replace (or add new): ")) - 1
            if 0 <= index <= len(headings):
                if index == len(headings):
                    new_heading = input("Enter the new heading (including '#' symbols): ")
                    level = new_heading.count('#')
                    text = new_heading.lstrip('#').strip()
                else:
                    level, text = headings[index]
                new_content = input("Enter the new content for this heading: ")
                doc = set_heading_content(doc, level, text, new_content)
                write_markdown(file_path, doc)
                print(f"Heading '{text}' has been set/replaced with new content.")
            else:
                print("Invalid heading number.")
        
        elif choice == '4':
            headings = list_headings(doc)
            print("\nAvailable headings:")
            for i, (level, text) in enumerate(headings, 1):
                print(f"{i}. {'#' * level} {text}")
            index = int(input("Enter the number of the heading to delete: ")) - 1
            if 0 <= index < len(headings):
                level, text = headings[index]
                doc = delete_heading(doc, level, text)
                write_markdown(file_path, doc)
                print(f"Heading '{text}' and its content have been deleted.")
            else:
                print("Invalid heading number.")
        
        elif choice == '5':
            print("\nCurrent file content:")
            print(read_markdown(file_path))
        
        elif choice == '6':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()