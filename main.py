def main():
    print("Marketplace Intelligence started.")
    while True:
        command = input("> ").strip().lower()
        if command == "quit":
            break
        print(f"Unknown command: {command}")
if __name__ == "__main__":
    main()
