import io
import json
import pysam
from .feature import Feature

class VariantTable:

    # Always remember the *self* argument
    def __init__(self, vcfFile, species, info_columns = None, sample_columns = None):

        vcf = pysam.VariantFile(vcfFile)

        self.info_fields =  info_columns or []
        self.sample_fields = sample_columns or []
        self.variants = []
        self.features = []   #Bed-like features
        self.species = species

        for unique_id, var in enumerate(vcf.fetch()):
            self.variants.append((var, unique_id))
            chr = var.chrom
            start = var.pos - 1
            end = start + 1       #TODO -- handle structure variants and deletions > 1 base
            self.features.append((Feature(chr, start, end, ''), unique_id))

    def to_JSON(self):


        json_array = [];

        for variant, unique_id in self.variants:
            obj = {
                'unique_id': unique_id,
                'CHROM': variant.chrom,
                'POSITION': variant.pos,
                'REF': variant.ref,
                'ALT': ','.join(variant.alts),
                'ID': ''
            }

            if variant.id is not None:
                obj['ID'] = render_ids(variant.id)

            for h in self.info_fields:
                v = ''
                if h in variant.info:
                    if h == 'ANN':
                        genes, effects, impacts, transcript, aa_alt, nt_alt = decode_ann(variant, self.species)
                    elif h == 'COSMIC_ID':
                        v = render_id(v)
                    else:
                        v = render_values(variant.info[h])
                if h == 'ANN':
                    obj['GENE'] = genes
                    obj['EFFECTS'] = effects
                    obj['IMPACT'] = impacts
                    obj['TRANSCRIPT'] = transcript
                    obj['PROTEIN ALTERATION'] = aa_alt
                    obj['DNA ALTERATION'] = nt_alt
                else:
                    obj[h] = v

            for h in self.sample_fields:
                for sample, values in variant.samples.items():
                    v = ''
                    try:
                        v = values[h]
                    except KeyError:
                        # ignore if key is not present
                        pass

                    obj[f'{sample}:{h}'] = render_values(v)

            json_array.append(obj)

        if not any(obj['ID'] for obj in json_array):
            # Remove ID column if none of the records actually had an ID.
            for obj in json_array:
                del obj['ID']
        return json.dumps(json_array)


def render_value(v):
    """Render given value to string."""
    if isinstance(v, float):
        # ensure that we don't waste space by insignificant digits
        return f'{v:.2g}'
    return str(v)


def render_values(v):
    if isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
        return render_value(v)
    return ','.join(map(render_value, v))


def render_id(v):
    if v.startswith('COSM'):
        return (f'<a href = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?'
                f'id={v[4:]}" target="_blank">{v}</a>')
    return v


def render_ids(v):
    return ','.join(map(render_id, v.split(';')))


def decode_ann(variant, species):
    """Decode the standardized ANN field to something human readable."""
    annotations = ([variant.info['ANN'].split('|'
                   )] if isinstance(variant.info['ANN'],
                   str) else [e.split('|') for e in variant.info['ANN']])
    genes = []
    effects = []
    impacts = []
    transcripts = []
    aa_alts = []
    nt_alts = []
    for allele in variant.alts:
        for ann in annotations:
            ann_allele, kind, impact, gene = ann[:4]
            feature_id = ann[6]
            nt_mod, aa_mod = ann[9:11]

            if allele != ann_allele:
                continue

            full = '|'.join(ann)
            # Keep the most severe effect.
            # Link out to Genecards and show the full record in a tooltip.
            genes.append(f'<a href="https://www.ensembl.org/{species}/Gene/'
                           f'Summary?db=core;t={gene}" target="_blank">{gene}</a>')
            effects.append(kind.replace('&', '/'))
            impacts.append(impact)
            transcripts.append(f'<a href="https://www.ensembl.org/{species}/Transcript/Summary?db=core;t={feature_id}" target="_blank">{feature_id}</a>')
            aa_alts.append(f'<a href="https://www.google.com/search?q={gene}&as_epq={aa_mod}" target="_blank">{aa_mod}</a>')
            nt_alts.append(f'<a href="https://www.google.com/search?q={gene}&as_epq={nt_mod}" target="_blank">{nt_mod}</a>')
    return ','.join(genes), ','.join(effects), ','.join(impacts), ','.join(transcripts), ','.join(aa_alts), ','.join(nt_alts)
