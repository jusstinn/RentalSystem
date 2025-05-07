try:
    import main
    print("Successfully imported main module")
    print("Trying to run main function...")
    main.main()
    print("Main function executed successfully")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc() 