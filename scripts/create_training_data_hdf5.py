##############################################################################

# This script writes out the per-vertex features and lesion classification for each patient and control to a .hdf5 file. 

#import relevant packages
import numpy as np
import nibabel as nb
import argparse
import io_meld as io
import h5py
import os

#parse commandline arguments pointing to subject_dir etc
parser = argparse.ArgumentParser(description='create feature matrix for all subjects')
parser.add_argument('subject_dir', type=str,
                    help='path to subject dir')
parser.add_argument('subject_ids',
                    type=str,
                    help='textfile containing list of subject ids')

args = parser.parse_args()


#save subjects dir and subject ids. import the text file containing subject ids
subject_dir=args.subject_dir
subject_ids_filename=args.subject_ids
subject_ids=np.loadtxt(os.path.join(subject_dir, subject_ids_filename), dtype='str', ndmin=1)


#list features
features = np.array(['.inter_z.on_lh.intra_z.thickness.sm10.mgh', '.inter_z.asym.on_lh.intra_z.thickness.sm10.mgh',
                     '.inter_z.on_lh.intra_z.w-g.pct.sm10.mgh','.inter_z.asym.on_lh.intra_z.w-g.pct.sm10.mgh',
                     '.inter_z.on_lh.intra_z.pial.K_filtered.sm20.mgh','.inter_z.asym.on_lh.intra_z.pial.K_filtered.sm20.mgh',
                     '.inter_z.on_lh.curv.mgh','.inter_z.on_lh.sulc.mgh',
                     '.inter_z.asym.on_lh.curv.mgh','.inter_z.asym.on_lh.sulc.mgh',
                     '.inter_z.on_lh.intra_z.gm_FLAIR_0.75.sm10.mgh','.inter_z.on_lh.intra_z.gm_FLAIR_0.5.sm10.mgh',
                     '.inter_z.on_lh.intra_z.gm_FLAIR_0.25.sm10.mgh','.inter_z.on_lh.intra_z.gm_FLAIR_0.sm10.mgh',
                     '.inter_z.on_lh.intra_z.wm_FLAIR_0.5.sm10.mgh','.inter_z.on_lh.intra_z.wm_FLAIR_1.sm10.mgh',
                     '.inter_z.asym.on_lh.intra_z.gm_FLAIR_0.75.sm10.mgh','.inter_z.asym.on_lh.intra_z.gm_FLAIR_0.5.sm10.mgh',
                     '.inter_z.asym.on_lh.intra_z.gm_FLAIR_0.25.sm10.mgh','.inter_z.asym.on_lh.intra_z.gm_FLAIR_0.sm10.mgh',
                     '.inter_z.asym.on_lh.intra_z.wm_FLAIR_0.5.sm10.mgh','.inter_z.asym.on_lh.intra_z.wm_FLAIR_1.sm10.mgh',
    '.on_lh.thickness.mgh', '.on_lh.w-g.pct.mgh', '.on_lh.curv.mgh','.on_lh.sulc.mgh',
    '.on_lh.gm_FLAIR_0.75.mgh', '.on_lh.gm_FLAIR_0.5.mgh', '.on_lh.gm_FLAIR_0.25.mgh',
    '.on_lh.gm_FLAIR_0.mgh', '.on_lh.wm_FLAIR_0.5.mgh', '.on_lh.wm_FLAIR_1.mgh',
    '.on_lh.pial.K_filtered.sm20.mgh'])
n_vert=163842
cortex_label=nb.freesurfer.io.read_label(os.path.join(subject_dir,'fsaverage_sym/label/lh.cortex.label'))
medial_wall = np.delete(np.arange(n_vert),cortex_label)




for subject in subject_ids:
    print "saving subject " + subject + "..."
    io.save_subject(subject,features,medial_wall,subject_dir)



