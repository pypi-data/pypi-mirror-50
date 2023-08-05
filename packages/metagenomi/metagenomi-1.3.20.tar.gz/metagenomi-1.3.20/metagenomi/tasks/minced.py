import os

from metagenomi.tasks.taskbase import MgTask
from metagenomi.helpers import to_int
from metagenomi.helpers import download_file


class Minced(MgTask):
    def __init__(self, mgid, **data):
        MgTask.__init__(self, mgid,  **data)

        self.crispr_arrays = to_int(self.d.get('crispr_arrays', 'None'))
        self.unique_repeats = to_int(self.d.get('unique_repeats', 'None'))
        self.unique_spacers = to_int(self.d.get('unique_spacers', 'None'))
        self.contigs_w_crisprs = to_int(self.d.get(
                                        'contigs_w_crisprs', 'None'))

        self.repeats = self.d.get('repeats', 'None')
        self.spacers = self.d.get('spacers', 'None')
        self.minced_summary = self.d.get('minced_summary', 'None')
        self.minced_gff = self.d.get('minced_gff', 'None')
        # self.unique_id = self.d.get('unique_id')
        self.output = self.d.get('output')

        self.schema = {**self.schema, **{
            'crispr_arrays': {'required': True, 'type': 'integer'},
            'unique_spacers': {'required': True, 'type': 'integer'},
            'unique_repeats': {'required': True, 'type': 'integer'},
            'contigs_w_crisprs': {'required': True, 'type': 'integer'},
            'repeats': {'required': True, 'type': 's3file'},
            'spacers': {'required': True, 'type': 's3file'},
            'minced_summary': {'required': True, 'type': 's3file'},
            'minced_gff': {'required': True, 'type': 's3file'},
            'output': {'required': True, 'type': 's3file'}
        }}

        if self.check:
            self.validate()

    def download_summary(self, dir_to_dl=os.getcwd()):
        return download_file(self.minced_summary, dir_to_dl)

    def download_spacers(self, dir_to_dl=os.getcwd()):
        return download_file(self.spacers, dir_to_dl)

    def download_repeats(self, dir_to_dl=os.getcwd()):
        return download_file(self.repeats, dir_to_dl)

    def download_gff(self, dir_to_dl=os.getcwd()):
        return download_file(self.minced_gff, dir_to_dl)
