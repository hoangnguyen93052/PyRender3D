import os
import random
import string
import subprocess
import tempfile
from typing import List, Dict, Any, Tuple

class Fuzzer:
    def __init__(self, target_program: str, input_generator: 'InputGenerator'):
        self.target_program = target_program
        self.input_generator = input_generator

    def run(self, iterations: int):
        for _ in range(iterations):
            test_input = self.input_generator.generate()
            self.execute_target(test_input)

    def execute_target(self, test_input: str):
        with tempfile.NamedTemporaryFile(suffix=".input", delete=False) as input_file:
            input_file.write(test_input.encode())
            input_file.close()
            try:
                result = subprocess.run([self.target_program], input=test_input, text=True, capture_output=True)
                print(f"Output: {result.stdout}")
                print(f"Error: {result.stderr}")
                return result.returncode
            finally:
                os.remove(input_file.name)

class InputGenerator:
    def __init__(self, length_range: Tuple[int, int]):
        self.length_range = length_range

    def generate(self) -> str:
        length = random.randint(*self.length_range)
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class FileInputGenerator(InputGenerator):
    def __init__(self, file_path: str):
        super().__init__((1, 1024))  # Default range
        self.file_path = file_path

    def generate(self) -> str:
        with open(self.file_path, 'r') as f:
            return random.choice(f.readlines())

def main():
    target = "path_to_your_target_program"
    iterations = 1000
    fuzzing_input_generator = InputGenerator((1, 128))
    fuzzer = Fuzzer(target, fuzzing_input_generator)

    print("Starting fuzz testing...")
    fuzzer.run(iterations)
    print("Fuzz testing completed.")

if __name__ == "__main__":
    main()
```

```python
file_name: advanced_fuzz_testing.py
commit: Added advanced input generation and mutation techniques
code:
import os
import random
import string
import subprocess
import tempfile
import json
from typing import List, Dict, Any, Tuple

class Fuzzer:
    def __init__(self, target_program: str, input_generator: 'InputGenerator'):
        self.target_program = target_program
        self.input_generator = input_generator

    def run(self, iterations: int):
        for _ in range(iterations):
            test_input = self.input_generator.generate()
            self.execute_target(test_input)

    def execute_target(self, test_input: str):
        with tempfile.NamedTemporaryFile(suffix=".input", delete=False) as input_file:
            input_file.write(test_input.encode())
            input_file.close()
            try:
                result = subprocess.run([self.target_program], input=test_input, text=True, capture_output=True)
                print(f"Output: {result.stdout}")
                print(f"Error: {result.stderr}")
                return result.returncode
            except Exception as e:
                print(f"Exception occurred: {e}")
            finally:
                os.remove(input_file.name)

class InputGenerator:
    def __init__(self, length_range: Tuple[int, int]):
        self.length_range = length_range

    def generate(self) -> str:
        length = random.randint(*self.length_range)
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class MutatedInputGenerator(InputGenerator):
    def __init__(self, original_input: str):
        super().__init__((1, len(original_input)))
        self.original_input = original_input

    def generate(self) -> str:
        mutation_index = random.randint(0, len(self.original_input) - 1)
        mutation_char = random.choice(string.ascii_letters + string.digits)
        mutated_input = self.original_input[:mutation_index] + mutation_char + self.original_input[mutation_index + 1:]
        return mutated_input

class FileInputGenerator(InputGenerator):
    def __init__(self, file_path: str):
        super().__init__((1, 1024))  # Default range
        self.file_path = file_path

    def generate(self) -> str:
        with open(self.file_path, 'r') as f:
            return random.choice(f.readlines()).strip()

def main():
    target = "path_to_your_target_program"
    iterations = 1000
    original_input = "sample input for fuzzing"
    file_input_gen = FileInputGenerator("input_samples.txt")
    mutated_input_gen = MutatedInputGenerator(original_input)
    
    fuzzer = Fuzzer(target, file_input_gen)

    print("Starting fuzz testing with file input...")
    fuzzer.run(iterations)

    print("Starting fuzz testing with mutated input...")
    for _ in range(iterations):
        test_input = mutated_input_gen.generate()
        fuzzer.execute_target(test_input)

    print("Fuzz testing completed.")

if __name__ == "__main__":
    main()
```

```python
file_name: fuzzer_report_generator.py
commit: Implemented report generation for fuzzing results
code:
import os
import json
from datetime import datetime
from typing import List, Dict

class FuzzingReport:
    def __init__(self, results: List[Dict[str, Any]]):
        self.results = results
        self.timestamp = datetime.now().isoformat()

    def generate_summary(self) -> dict:
        summary = {
            'total_tests': len(self.results),
            'total_crashes': sum(1 for result in self.results if result['crash']),
            'total_time': sum(result['duration'] for result in self.results),
            'timestamp': self.timestamp,
        }
        return summary

    def save_report(self, filename: str):
        summary = self.generate_summary()
        with open(filename, 'w') as report_file:
            json.dump({
                'summary': summary,
                'detailed_results': self.results
            }, report_file, indent=4)
        print(f"Report saved as {filename}")

def main():
    results = [
        {'test_input': 'input1', 'crash': True, 'duration': 0.5},
        {'test_input': 'input2', 'crash': False, 'duration': 0.2},
        {'test_input': 'input3', 'crash': True, 'duration': 0.4},
        # Add more results here
    ]
    
    report = FuzzingReport(results)
    report_filename = 'fuzzing_report.json'
    report.save_report(report_filename)

if __name__ == "__main__":
    main()