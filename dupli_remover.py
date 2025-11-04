def remove_duplicates_in_files(tokaid_path, toka_path):
    # Read both files and store lines
    with open(tokaid_path, 'r') as tokaid_file:
        tokaid_lines = tokaid_file.readlines()
    
    with open(toka_path, 'r') as toka_file:
        toka_lines = toka_file.readlines()

    # Dictionary to track the latest occurrence of each UID
    latest_uid_index = {}

    # Identify latest occurrences of each UID
    for i, line in enumerate(tokaid_lines):
        uid = line.split()[0]  # Assuming UID is the first item on each line
        latest_uid_index[uid] = i  # Always store the latest occurrence

    # Print and remove duplicates, keeping only the latest entries
    print("Removing the following duplicates:")
    new_tokaid_lines = []
    new_toka_lines = []
    for i, line in enumerate(tokaid_lines):
        uid = line.split()[0]
        if latest_uid_index[uid] == i:
            new_tokaid_lines.append(tokaid_lines[i])
            new_toka_lines.append(toka_lines[i])
        else:
            print(f"Line {i + 1}: '{line.strip()}' (duplicate removed)")

    # Write the modified content back to each file
    with open(tokaid_path, 'w') as tokaid_file:
        tokaid_file.writelines(new_tokaid_lines)
    
    with open(toka_path, 'w') as toka_file:
        toka_file.writelines(new_toka_lines)

    print("Duplicate removal complete.")

def main_menu():
    print("Duplicate Removal Tool")
    print("======================")
    print("1. Remove duplicates from tokaid.txt and toka.txt")
    print("2. Exit")

    choice = input("Enter your choice: ")
    if choice == "1":
        tokaid_path = '/sdcard/Test/tokaid.txt'
        toka_path = '/sdcard/Test/toka.txt'
        remove_duplicates_in_files(tokaid_path, toka_path)
    elif choice == "2":
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")
        main_menu()

# Run the main menu
main_menu()
