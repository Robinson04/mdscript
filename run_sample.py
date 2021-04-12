import os


class SampleExecutor:
    def __init__(self, dirpath: str):
        self.expected_record_filepath = os.path.join(dirpath, 'record.json')
        self.expected_code_filepath = os.path.join(dirpath, 'code.py')
        self.expected_output_filepath = os.path.join(dirpath, 'output.txt')

    def get_formatted_markdown(self) -> str:
        return f"""
### Queried record :
```json
{self.get_record()}
```

### Code
```python
{self.get_code()}
```

### Output
```
{self.get_output()}
```
        """

    def get_record(self) -> str:
        with open(self.expected_record_filepath, 'r') as file:
            return file.read()

    def get_code(self) -> str:
        with open(self.expected_code_filepath, 'r') as file:
            return file.read()

    def get_output(self) -> str:
        with open(self.expected_output_filepath, 'r') as file:
            return file.read()

    def run(self):
        import importlib.util
        module_spec = importlib.util.spec_from_file_location("", self.expected_code_filepath)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)


if __name__ == '__main__':
    SampleExecutor(dirpath='./one').run()
