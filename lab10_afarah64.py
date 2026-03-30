from pathlib import Path
import string

class WordAnalyzer:
    """this class is responsible for analyzing the word frequencies in a given text file, while ignoring specified stop words. 
       It processes the file and generates a report of word frequencies.
       
       Attributes:
           __file_path (Path): the path to the file to be analyzed, stored as a private Path object
           __frequencies (dict[str, int]): a dictionary to store the frequency of each word found in the file
           __stop_words (set[str]): a set of words to be ignored in the analysis,
    """
    def __init__(self, file_path: str, stop_words:list [str]):
        """this is the constructor for the WordAnalyzer class

        Args:
            file_path (str): the path to the file to be analyzed
            stop_words (list[str]): a list of words to be ignored in the analysis
        """
        # store the file path as a private Path object
        self.__file_path = Path(file_path)
        # initialize the frequencies dictionary to store word counts
        self.__frequencies: dict[str, int] = {}
        # store the stop words as a set for faster lookup
        self.__stop_words = set(stop_words)


    def process_file(self):
        """this method reads and processes the file, populating the word frequencies while ignoring the stop words.

        Returns:
            bool: True if the file was processed successfully, False otherwise
        """
        self.__frequencies.clear()

        # Check if the file exists before attempting to read it
        if not self.__file_path.exists():
            print(f"File not found: {self.__file_path}")
            return False
        
        # Define a cleaner to remove punctuation and special characters from the text
        cleaner = str.maketrans('', '', string.punctuation + "“”‘’—•†_")
        roman_chars = set("ivxlcdm")
        try:
            with self.__file_path.open('r', encoding='utf-8') as file:
                for raw_line in file:
                    #convert the line to lowercase
                    line = raw_line.lower()
                    #clean the line by removing punctuation and special characters
                    clean_line = line.translate(cleaner)
                    #split the cleaned line into words
                    words = clean_line.split()

                    for word in words:
                        #strip any leading or trailing whitespace from the word
                        word = word.strip()
                        #skip empty words
                        if not word:
                            continue
                        #skip the word if it contains non-alphabetic characters or non-ASCII characters
                        if not word.isalpha() or not word.isascii():
                            continue
                        #
                        if all(char in roman_chars for char in word):
                            continue
                        #skip the word if it is in the stop words set
                        if word in self.__stop_words:
                            continue
                        #update the frequency count for the word in the frequencies dictionary
                        self.__frequencies[word] = self.__frequencies.get(word, 0) + 1

            return True

        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
            return False
                               
    
    def report(self):
        """this method prints the word and their number of frequencies in sorted order
        """
        for word in sorted(self.__frequencies.keys()):
            print(f"{word:<25} :: {self.__frequencies[word]}")

def main():

    """this main class that generates the menu for the user to select a file to analyze, 
       and then processes the selected file and generates a report of word frequencies. 
       or exits the program if the user chooses to do so. 
    """
    # mapping user choices to their paths
    files = {
        "1": Path.cwd() / "monte_cristo.txt",
        "2": Path.cwd() / "princess_mars.txt",
        "3": Path.cwd() / "Tarzan.txt",
        "4": Path.cwd() / "treasure_island.txt"
    }
    # list of stop words to be ignored in the analysis
    stop_words = ["and", "in", "to", "of","on", "above", "that", "the"]
    
    while True:
        print("\n  --- Word Frequency Analyzer ---")
        for key, path in files.items():
            print(f"{key}. {path.stem.replace('_', ' ').title()}")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice in files:
            print(f"Processing file: {files[choice].name}...")
            # create an instance of WordAnalyzer with the selected file and stop words
            analyzer = WordAnalyzer(str(files[choice]), stop_words)
            # process the file and generate the report if processing was successful 
            if analyzer.process_file():
                # print the report of word frequencies. 
                analyzer.report()

                input("\nPress Enter to return to the menu...")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()