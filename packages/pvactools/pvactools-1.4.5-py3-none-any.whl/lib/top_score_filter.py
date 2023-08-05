import csv
import argparse
import lib.sort

class TopScoreFilter:
    def __init__(self, input_file, output_file, top_score_metric):
        self.input_file = input_file
        self.output_file = output_file
        self.top_score_metric = top_score_metric

    def execute(self):
        rows = []
        with open(self.input_file) as input_fh:
            reader = csv.DictReader(input_fh, delimiter = "\t")
            fieldnames = reader.fieldnames
            for line in reader:
                rows.append(line)


        sorted_rows = lib.sort.default_sort(rows, self.top_score_metric)
        with open(self.output_file, 'w') as output_fh:
            writer = csv.DictWriter(output_fh, delimiter = "\t", fieldnames = fieldnames)
            writer.writeheader()
            filtered_results = {}
            for line in sorted_rows:
                chromosome = line['Chromosome']
                start = line['Start']
                stop = line['Stop']
                ref = line['Reference']
                var = line['Variant']
                index = '%s.%s.%s.%s.%s' % (chromosome, start, stop, ref, var)
                if index not in filtered_results:
                    filtered_results[index] = line
                else:
                    if ((self.top_score_metric == 'median' and float(line['Median MT Score']) < float(filtered_results[index]['Median MT Score'])) or
                        (self.top_score_metric == 'lowest' and float(line['Best MT Score']) < float(filtered_results[index]['Best MT Score']))):
                        filtered_results[index] = line

            writer.writerows(filtered_results.values())

    @classmethod
    def parser(cls, tool):
        parser = argparse.ArgumentParser('%s top_score_filter' % tool, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument(
            'input_file',
            help="The final report .tsv file to filter."
        )
        parser.add_argument(
            'output_file',
            help="Output .tsv file containing only the list of the top "
                 + "epitope per variant."
        )
        parser.add_argument(
            '-m', '--top-score-metric',
            choices=['lowest', 'median'],
            default='median',
            help="The ic50 scoring metric to use for filtering. "
                 + "lowest: Use the best MT Score (i.e. the lowest MT ic50 binding score of all chosen prediction methods). "
                 + "median: Use the median MT Score (i.e. the median MT ic50 binding score of all chosen prediction methods)."
        )
        return parser
