import os

from metagenomi.models.modelbase import MgModel

from metagenomi.tasks.assemblystats import AssemblyStats
from metagenomi.tasks.prodigal import Prodigal
from metagenomi.tasks.mapping import Mapping
from metagenomi.tasks.minced import Minced
from metagenomi.tasks.kaiju import KaijuProteins, KaijuContigs
from metagenomi.tasks.crisprconnection import CrisprConnection
from metagenomi.tasks.r16s import R16S
# from metagenomi.tasks.hmm import HmmSearch
from metagenomi.tasks.jgimetadata import JgiMetadata
# from metagenomi.tasks.hmm import HmmSearch
from metagenomi.helpers import download_file

# from metagenomi.logger import logger


class Assembly(MgModel):
    # Possible tasks:
    # Mapping, Megahit, TODO:Prodigal
    def __init__(self, mgid, **data):
        self.mgtype = 'assembly'
        MgModel.__init__(self, mgid, **data)

        self.s3path = self.d.get('s3path')

        if 'mgtype' in self.d:
            self.mgtype = self.d['mgtype']

        self.mappings = None
        if 'Mappings' in self.d:
            self.mappings = []
            for m in self.d['Mappings']:
                self.mappings.append(Mapping(self.mgid, db=self.db, check=self.check, **m))

        self.assembly_stats = None
        if 'AssemblyStats' in self.d:
            self.assembly_stats = AssemblyStats(self.mgid,
                                                db=self.db, check=self.check, **self.d['AssemblyStats'])

        self.prodigal = None
        if 'Prodigal' in self.d:
            self.prodigal = Prodigal(self.mgid, db=self.db, check=self.check, **self.d['Prodigal'])

        self.jgi_metadata = None
        if 'JgiMetadata' in self.d:
            self.jgi_metadata = JgiMetadata(self.mgid, db=self.db, check=self.check,  **self.d['JgiMetadata'])

        self.minced = None
        if 'Minced' in self.d:
            self.minced = Minced(self.mgid, db=self.db, check=self.check, **self.d['Minced'])

        self.crispr_connections = None
        if 'CrisprConnections' in self.d:
            self.crispr_connections = []
            for m in self.d['CrisprConnections']:
                self.crispr_connections.append(CrisprConnection(self.mgid, db=self.db, check=self.check, **m))

        self.r16s = None
        if 'R16S' in self.d:
            self.r16s = R16S(self.mgid, db=self.db, check=self.check, **self.d['R16S'])

        self.kaiju_proteins = None
        if 'KaijuProteins' in self.d:
            self.kaiju_proteins = KaijuProteins(self.mgid, db=self.db, check=self.check, **self.d['KaijuProteins'])

        self.kaiju_contigs = None
        if 'KaijuContigs' in self.d:
            self.kaiju_contigs = KaijuContigs(self.mgid, db=self.db, check=self.check, **self.d['KaijuContigs'])

        # No MgTasks are required. TODO: Except perhaps mapping?
        self.schema = {**self.schema, **{
            'Prodigal': {'type': 'dict'},
            'AssemblyStats': {'type': 'dict'},
            'Mappings': {'type': 'list'},
            'JgiMetadata': {'type': 'dict'},
            'Minced': {'type': 'dict'},
            'R16S': {'type': 'dict'},
            'CrisprConnections': {'type': 'list'},
            'mgtype': {'type': 'string',
                       'allowed': ['assembly'],
                       'required': True}
            },
            's3path': {'type': 's3file', 'required': True},
            'associated': {'type': 'dict',
                           'required': True,
                           'schema': {'sequencing': {
                                'type': 'list',
                                'schema': {'type': ['mgid',
                                                    'nonestring']},
                                'required': True
                                },
                            }
                        }
            }

        if self.check:
            self.validate()

    def set_s3path(self, newpath, write=True):
        self.s3path = newpath
        if write:
            if self.validate():
                self.update('s3path', newpath)

    def link_sequencing(self, seq_mgid, xlink=True, write=True):
        '''
        xlink = whether or not you want to also link the corresponding sequencing
        to this assembly. If this were always True, would result in infinite
        loop
        TODO: Allow this to take either an mgid or an object
        '''
        from metagenomi.models.sequencing import Sequencing
        if xlink:
            linked_sequencing = Sequencing(seq_mgid, db=self.db, load=True)
            linked_sequencing.link_assembly(self.mgid, xlink=False)

        if 'sequencing' in self.associated:
            if self.associated['sequencing'] == ['None']:
                self.associated['sequencing'] = [seq_mgid]
            else:
                if seq_mgid not in self.associated['sequencing']:
                    self.associated['sequencing'] = self.associated['sequencing'] + [seq_mgid]
        else:
            self.associated['sequencing'] = [seq_mgid]

        if write:
            self.update('associated', self.associated)

    def get_filtered_contigs(self, raise_error=False):
        '''
        DEPRECATED
        '''
        if self.prodigal:
            ctgs = self.prodigal.pullseq_contigs
            return ctgs
        else:
            if raise_error:
                e = f'No filtered contigs, prodigal has not been run'
                raise ValueError(e)
            else:
                return None

    def get_contigs(self, filtered=True, raise_error=False):
        if filtered:
            if self.prodigal:
                ctgs = self.prodigal.pullseq_contigs
                return ctgs
            else:
                if raise_error:
                    e = f'No filtered contigs, prodigal has not been run'
                    raise ValueError(e)
                else:
                    return None
        else:
            return self.s3path

    def download_contigs(self, dir_to_dl=os.getcwd(), filtered=True, overwrite=True, dry_run=False):
        if filtered:
            if self.prodigal:
                ctgs = self.prodigal.pullseq_contigs
                return ctgs
            else:
                if raise_error:
                    e = f'No filtered contigs, prodigal has not been run'
                    raise ValueError(e)
                else:
                    return None
        else:
            ctgs = self.s3path

        return download_file(ctgs, dir_to_dl, dry_run=dry_run, overwrite=overwrite)

    def download_faa(self, dir_to_dl=os.getcwd(), overwrite=True, dry_run=False, raise_error=True):
        '''
        DEPRECATED
        '''
        if self.prodigal:
            faa = self.prodigal.protein_file
        else:
            if raise_error:
                e = f'No filtered contigs, prodigal has not been run'
                raise ValueError(e)
            else:
                return None

        return download_file(faa, dir_to_dl, dry_run=dry_run, overwrite=overwrite)

    def download_proteins(self, dir_to_dl=os.getcwd(), overwrite=True, dry_run=False, raise_error=True):
        if self.prodigal:
            faa = self.prodigal.protein_file
        else:
            if raise_error:
                e = f'No filtered contigs, prodigal has not been run'
                raise ValueError(e)
            else:
                return None

        return download_file(faa, dir_to_dl, dry_run=dry_run, overwrite=overwrite)

    def get_associated_sequencings(self):
        if 'sequencing' in self.associated:
            return self.associated['sequencing']
        else:
            return []

    def get_prodigal_cmd(self, cutoff=1000):
        cmd = f'python submit_prodigal_job.py --mgid {self.mgid}'

        return(cmd)

    def get_minced_cmd(self, filtered_ctgs=True, overrides=None):
        '''
        '''

        if self.prodigal:
            cmd = f'python submit_minced.py --mgid {self.mgid} --gff'
            return(cmd)
        else:
            e = f'No filtered contigs, prodigal has not been run'
            raise ValueError(e)

    def get_reassembly_cmd(self, out, jobdef=None):
        cmd = f'python submit_megahit_job.py --mgid {self.mgid} --out {out}'
        if jobdef:
            cmd += f' --job-def {jobdef}'
        return cmd
