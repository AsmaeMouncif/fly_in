def parse_file(self):
    try:
        with open(self.file_path, "r") as file:
            lines = []
            for line_number, raw_line in enumerate(file, start=1):
                content = self.strip_comment(raw_line)
                if not content:
                    continue
                lines.append((line_number, content))
    except FileNotFoundError:
        raise ParserError(f"File not found: {self.file_path}")
    except PermissionError:
        raise ParserError(f"Permission denied: {self.file_path}")
    except IsADirectoryError:
        raise ParserError(f"Expected a file, got a directory: {self.file_path}")
    except OSError as e:
        raise ParserError(f"Cannot read file {self.file_path}: {e}")
    if not lines:
        raise ParserError(f"Empty file: {self.file_path}")
    first_line_number, first_content = lines[0]
    if not first_content.startswith("nb_drones:"):
        raise ParserError(
            f"Line {first_line_number}: nb_drones must be the first line of the file"
        )
    contents_only = []
    for line_number, content in lines:
        contents_only.append(content)
    self.check_required_fields_present(contents_only)
    for line_number, content in lines:
        try:
            self.parse_line(content)
        except ParserError as e:
            raise ParserError(f"Line {line_number}: {e}") from e