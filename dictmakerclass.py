
"""
Make An Excel File with this one weird trick
"""
import csv


class LQLtoCSV:
    """
    Class for Conversion
    """

    def __init__(self, file):
        self.file = file
        self.schema = ["Value/Data", "Lytics Slug", "Condition",
                       "Short Description", "Long Description",
                       "Data Type", "Custom Storage Rule"]
        self.csv_file = file[:-4] + ".csv"
        self.lql_data = []
        self.input = "input/"
        self.output = "output/"

    def get_lql_data(self):
        """
        Read LQL file, extract query lines
        """

        with open(self.input + self.file, 'r') as lql_file:

            lines = lql_file.read().split('\n')
            for line in lines:
                if " AS " in line:
                    self.lql_data.append(line)



    def extract_and_write(self):
        """Iterate through lines, convert, write"""

        with open(self.output + self.csv_file, 'w') as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(self.schema)

            for line in self.lql_data:
                attributes = self.line_parser(line)

                writer.writerow([attributes['value'],
                                 attributes['as'],
                                 attributes['if'],
                                 attributes['shortdesc'],
                                 attributes['longdesc'],
                                 attributes['kind'],
                                 attributes['mergeop']])

            csv_file.close()


    def line_parser(self, line):
        """Return line formatted for CSV"""

        def get_substring_by_space(line, keyword):

            if keyword in line:

                # Look for keyword, omitting from beginning of substr
                start = line.find(keyword) + len(keyword)

                # Look for end of substr, inidcated by character
                end = line[start:].find(" ")

                # in case end EOL
                if end == -1:
                    return line[start:]

                return line[start:start + end]

            return ""


        def get_substring_by_quote(line, keyword):

            if keyword in line:

                # Look for keyword, omitting from beginning of substr
                start = line.find(keyword) + len(keyword)

                # Find first quote
                open_quote = line[start:].find("\"") + len("\"") + start

                # Look for end of substr, inidcated by quote
                close_quote = line[open_quote:].find("\"")

                return line[open_quote:open_quote + close_quote]

            return ""


        def value(line):
            """value gets its own function, it is not ident by keyword"""

            parsed = line.split(" AS ")[0].strip()

            # If present remove leading comma
            if parsed[0] == ",":
                return parsed[1:].strip()

            return parsed


        def if_field(line):
            """if gets its own function, ending not ident by specific keyword"""

            stopwords = ["SHORTDESC", "LONGDESC", "KIND", "MERGEOP"]

            if " IF " in line:
                if_index = line.find(" IF ") + len(" IF ")

                for stopword in stopwords:
                    if stopword in line:
                        end_if = line[if_index:].find(stopword)
                        break
                    else:
                        end_if = 0

                try:
                    return line[if_index:if_index + end_if].strip()

                # Catches if nothing after IF condition in line
                except IndexError:
                    return line[if_index:].strip()

            return ""

        return {
            "value": value(line),
            "as": get_substring_by_space(line, " AS "),
            "if": if_field(line),
            "shortdesc": get_substring_by_quote(line, " SHORTDESC "),
            "longdesc":  get_substring_by_quote(line, " LONGDESC "),
            "kind": get_substring_by_space(line, " KIND "),
            "mergeop": get_substring_by_space(line, " MERGEOP ")
        }
