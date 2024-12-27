def save_results(filename, results):
    """Save scan results to a file."""
    try:
        with open(filename, "w") as file:
            file.write(results)
        print(f"Results saved to {filename}.")
    except Exception as e:
        print(f"Error saving results: {e}")
