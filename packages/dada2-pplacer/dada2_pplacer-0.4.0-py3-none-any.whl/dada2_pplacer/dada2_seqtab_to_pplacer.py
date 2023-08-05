#!/usr/bin/env python
import pandas as pd
import csv
import argparse
import sys


def main():
    args_parser = argparse.ArgumentParser(description="""A small utility to convert dada2 style
    seqtables to a MOTHUR style sharetable and/or pplacer-style map and weights files.
    """)

    args_parser.add_argument('--seqtable', '-s',
                             help="Sequence table from dada2, in CSV format",
                             required=True, type=argparse.FileType('r'))
    args_parser.add_argument('--fasta_out_sequences', '-f',
                             help="Write sequence variants to this file, in FASTA format",
                             type=argparse.FileType('w'))
    args_parser.add_argument('--map', '-m',
                             help="Write pplacer-style mapping of sv to specimen",
                             type=argparse.FileType('w'))
    args_parser.add_argument('--weights', '-w',
                             help="Write pplacer-style weights of sv by specimen",
                             type=argparse.FileType('w'))
    args_parser.add_argument('--sharetable', '-t',
                             help="Write mothur-style sharetable to this location",
                             type=argparse.FileType('w'))

    args = args_parser.parse_args()

    # Check to see if we've been tasked with anything. If not, we have nothing to do and should exit
    if not (args.fasta_out_sequences or args.map or args.weights or args.sharetable):
        sys.exit("Nothing to do")

    # Just convert our handles over to something nicer
    if args.fasta_out_sequences:
        out_sv_seqs_h = args.fasta_out_sequences
    else:
        out_sv_seqs_h = None
    if args.map:
        out_map_h = args.map
        map_writer = csv.writer(out_map_h)
    else:
        map_writer = None
    if args.weights:
        out_weights_h = args.weights
        weights_writer = csv.writer(out_weights_h)
    else:
        weights_writer = None
    if args.sharetable:
        sharetable_fn = args.sharetable
    else:
        sharetable_fn = None

    # Load the sequence table
    seqtab = pd.read_csv(args.seqtable, index_col=0)
    # Rank order the sequences in order of mean relative abundance
    rank_ordered_seqs = list((seqtab.T / seqtab.T.sum()).T.mean().sort_values(ascending=False).index)

    # Generate sv labels for each sequence variant,
    # and create a dictionary that maps sequence-variant to sv_id...
    seq_to_sv_num = {s: 'sv-%d' % (i + 1) for i, s in enumerate(rank_ordered_seqs)}
    # and a dictionary to map sv_id to sequence-variant
    sv_num_to_seq = {'sv-%d' % (i + 1): s for i, s in enumerate(rank_ordered_seqs)}
    # reorder and rename our columns to fit these new mappings
    seqtab_reorder = seqtab[list(sv_num_to_seq.values())].rename(seq_to_sv_num, axis=1).sort_index()

    # Annoyingly, we need to pick a representitive actual sequence
    # from each sv to be it's champion for guppy.
    # To do so, we will go through each column, find the max count for that sv,
    # and use that specimen as the champion
    max_spec_for_sv = {sv_id: spec for sv_id, spec in seqtab_reorder.apply(lambda c: c.idxmax()).items()}

    if out_sv_seqs_h:
        # Write out the sequences in fasta format, using the sv-id's generated above as an ID
        for sv_id, seq in sv_num_to_seq.items():
            out_sv_seqs_h.write(">%s:%s\n%s\n" % (sv_id, max_spec_for_sv[sv_id], seq))

    # Now write the mapping and weights files
    # Both are headerless CSV format files
    # map: sequence_id (sv_id:specimen), specimen
    # weight: sequence_id (sv_id here), specimen_sequence_id (sv_id:specimen here), count
    # This is a bit of a clunky structure (relating to some historic cruft)

    if map_writer or weights_writer:
        for spec, row in seqtab.iterrows():
            row_nonzero = row[row > 0]
            for sv_id, count in row_nonzero.items():
                if map_writer:
                    map_writer.writerow([str(sv_id) + ":" + str(spec), spec])
                if weights_writer:
                    weights_writer.writerow([
                        sv_id + ":" + max_spec_for_sv[sv_id],
                        str(sv_id) + ":" + str(spec),
                        count])

    if sharetable_fn:
        sharetable_labels = pd.DataFrame()
        sharetable_labels['label'] = list(seqtab_reorder.index)
        sharetable_labels['group'] = "dada2"
        sharetable_labels['numsvs'] = len(seqtab_reorder.columns)
        sharetable_labels.head()
        pd.merge(
            sharetable_labels,
            seqtab_reorder,
            left_on='label',
            right_index=True
        ).to_csv(sharetable_fn, index=False)        

    # Cleanup.
    if out_sv_seqs_h:
        out_sv_seqs_h.close()
    if map_writer:
        out_map_h.close()
    if weights_writer:
        out_weights_h.close()

# Boilerplate method to run this as a script
if __name__ == '__main__':
    main()
