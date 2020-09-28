import os
import subprocess as sub
import numpy as np
import argparse

def perform_segmentation(subjects_dir, subj_name):
    """
    Perform cortical parcellation based on T1w contrast image using Freesurfer recon-all [1]
    
    Parameters
    ----------
       subjects_dir : string
            the path to subjects directory input and output
       subj_name : string
            the name of the subject folder as MELD_[site code]_[scanner code]_[patient/control]_[number]
    
    Outputs
    ---------
    	Freesurfer cortical parcellation outputs for one subject. See freesurfer architecture for more information
    
    References
    ----------
    	[1] Natalia Zaretskaya et al, Advantages of cortical surface reconstruction using submillimeter 7 T MEMPRAGE, 2018, NeuroImage 165

    """
    
    input_dir = os.path.join(subjects_dir,'input',subj_name)
    T1_file = os.path.join(input_dir,'T1',subj_name + '.nii')
    FLAIR_file = os.path.join(input_dir,'FLAIR',subj_name + '_FLAIR'+'.nii')
    output_dir =os.path.join(subjects_dir, 'output')
	
	#check inputs exist
    if not os.path.isfile(T1_file):
        raise FileNotFoundError('Could not find T1 volume in {}. Check if name follow the right nomenclature'.format(T1_file))
    if os.path.isfile(FLAIR_file):
        print('No FLAIR file has been found')
        isflair = True
    else:
        isflair = False
	
    # Initialise freesurfer variable environment
    ini_freesurfer = format("$FREESURFER_HOME/SetUpFreeSurfer.sh")

    # Perform cortical segmentation
    if isflair == True:
    	print('Segmentation using T1 and FLAIR')
    	recon_all = format("$FREESURFER_HOME/bin/recon-all -sd {} -s {} -i {} -FLAIR {} -FLAIRpial -all"
                       .format(output_dir, subj_name, T1_file, FLAIR_file))
    else:
    	print('Segmentation using T1 only')
    	recon_all = format("$FREESURFER_HOME/bin/recon-all -sd {} -s {} -i {} -all"
                       .format(output_dir, subj_name, T1_file))
                       
    command1 = ini_freesurfer + ';' + recon_all
    
    try:
        print("INFO : Start cortical parcellation (up to 36h). Please wait")
        sub.check_call(command1, shell=True)
        print("INFO : End of cortical parcellation. Results stored in {}".format(output_dir))
    except sub.CalledProcessError:
        quit()


if __name__ == "__main__":
	
    #parse commandline arguments 
    parser = argparse.ArgumentParser(description='perform cortical 		parcellation using recon-all from freesurfer')
    parser.add_argument('subjects_dir', type=str, 
                    help='path to subjects directory')
    parser.add_argument('subject_ids', 
                    type=str,
                    help='textfile containing list of subject ids')
    args = parser.parse_args()
    subjects_dir = args.subjects_dir
    subjects_ids_filename = args.subject_ids
	subject_ids=np.loadtxt(subject_dir+subject_ids_filename, dtype='str',ndmin=1)

    #process data 
    #TODO add a loop for processing more than 1 subject
    subj_name = subjects_ids[0]
    perform_segmentation(subjects_dir, subj_name)
	
