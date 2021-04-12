import os
import re
from pathlib import Path

from run_sample import SampleExecutor

sampler_regex = r'({{sampler::)(.*)(}})'

def run_in_file(source_filepath: str, output_filepath: str):
    with open(source_filepath, 'r') as source_markdown_file:
        source_file_content = source_markdown_file.read()

        rendered_file_content = ""
        remaining_unprocessed_file_content = source_file_content
        for match in re.finditer(pattern=sampler_regex, string=source_file_content):
            match_start = match.start()
            match_end = match.end()

            index_relative_to_remaining_unprocessed = len(source_file_content) - len(remaining_unprocessed_file_content)
            unprocessed_text_pre_match = remaining_unprocessed_file_content[0:match_start - index_relative_to_remaining_unprocessed]
            remaining_unprocessed_file_content = remaining_unprocessed_file_content[match_end - index_relative_to_remaining_unprocessed:]

            template_name = match[2]
            executor = SampleExecutor(dirpath=f'F:/Inoft/StructNoSQL/docs/samples/{template_name}')
            template_code = executor.get_formatted_markdown()

            rendered_file_content += f"{unprocessed_text_pre_match}{template_code}"
        rendered_file_content += remaining_unprocessed_file_content

        with open(output_filepath, 'w+') as output_file:
            output_file.write(rendered_file_content)

def run_with_filepath(source_filepath: str):
    source_filepath_parts = Path(source_filepath).parts
    output_filepath = os.path.join(*source_filepath_parts[0:len(source_filepath_parts)-1], source_filepath_parts[-1][2:])
    run_in_file(source_filepath=source_filepath, output_filepath=output_filepath)

def run_in_folders():
    for root_dirpath, dirs, filenames in os.walk('F:/Inoft/StructNoSQL/docs/docs'):
        for filename in filenames:
            if filename[0:2] == '__':
                source_filepath = os.path.join(root_dirpath, filename)
                output_filename = filename[2:]
                output_filepath = os.path.join(root_dirpath, output_filename)
                run_in_file(source_filepath=source_filepath, output_filepath=output_filepath)

