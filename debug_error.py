import traceback
import sys

try:
    print("Importing main module...")
    import main
    print("Main module imported successfully.")
    
    print("\nTrying to run main function...")
    main.main()
    print("Main function executed successfully.")
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
    print("\nDetailed error traceback:")
    traceback.print_exc()

print("\nPress Enter to exit...")
input() 