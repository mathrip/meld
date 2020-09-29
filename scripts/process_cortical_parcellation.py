"""
    Perform cortical parcellation based on T1w contrast and FLAIR images using Freesurfer recon-all [1]
    
    Parameters
    ----------
       input_dir : string
            the path to subjects input T1 and FLAIR
       subjects_dir : string
            the path to subjects output directory
       subj_name : string
            the name of the subject folder as MELD_[site code]_[scanner code]_[patient/control]_[number]
    
    Outputs
    ---------
    	Freesurfer cortical parcellation outputs for one subject. See freesurfer architecture for more information
    
    References
    ----------
    	[1] Natalia Zaretskaya et al, Advantages of cortical surface reconstruction using submillimeter 7 T MEMPRAGE, 2018, NeuroImage 165

"""

#import relevant librairies
import os
import subprocess as sub
import numpy as np
import argparse


if __name__ == "__main__":
	
    #parse commandline arguments 
    parser = argparse.ArgumentParser(description='perform cortical parcellation using recon-all from freesurfer')
    parser.add_argument('input_dir', type=str, 
                    help='path to inputs directory')
    parser.add_argument('subjects_dir', type=str, 
                    help='path to output subjects directory')
    parser.add_argument('subject_ids', 
                    type=str,
                    help='textfile containing list of subject ids')
    args = parser.parse_args()
    input_dir = args.input_dir
    subjects_dir = args.subjects_dir
    subjects_ids_filename = args.subject_ids
    subjects_ids=np.loadtxt(os.path.join(subjects_dir, subjects_ids_filename), dtype='str',ndmin=1)

    #process data 
    for s in subjects_ids :
        T1_file = os.path.join(input_dir, s, 'T1', s+'.nii')
        FLAIR_file = os.path.join(input_dir, s, 'FLAIR', s+'_FLAIR'+'.nii')

	#check inputs exist
        if not os.path.isfile(T1_file):
            raise FileNotFoundError('Could not find T1 volume in {}. Check if name follow the right nomenclature'.format(T1_file))
        if os.path.isfile(FLAIR_file):
            print('No FLAIR file has been found')
            isflair = True
        else:
            isflair = False

        #initialise freesurfer variable environment
        ini_freesurfer = format("$FREESURFER_HOME/SetUpFreeSurfer.sh")

        #setup cortical segmentation
        if isflair == True:
            print('Segmentation using T1 and FLAIR')
            recon_all = format("$FREESURFER_HOME/bin/recon-all -sd {} -s {} -i {} -FLAIR {} -FLAIRpial -all"
	                   .format(subjects_dir, s, T1_file, FLAIR_file))
        else:
            print('Segmentation using T1 only')
            recon_all = format("$FREESURFER_HOME/bin/recon-all -sd {} -s {} -i {} -all"
		                   .format(subjects_dir, s, T1_file))

        #call freesurfer
        command1 = ini_freesurfer + ';' + recon_all
        try:
            print("INFO : Start cortical parcellation (up to 36h). Please wait")
            sub.check_call(command1, shell=True)
            print("INFO : End of cortical parcellation. Results stored in {}".format(subjects_dir))
        except sub.CalledProcessError:
            quit()

	
