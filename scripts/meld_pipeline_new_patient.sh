########### master script for running the meld pipeline on new patient ########

## run "bash meld_pipeline.sh <path_to_subjects_dir> <path_to_meld_scripts_dir>

input_dir=$1
subjects_dir=$2
script_dir=$4
subject_ids="List_subjects.txt"
site_code=$3

#perform cortical parcellation
#echo "Processing cortical parcellation"
#python "$script_dir"/process_cortical_parcellation.py "$input_dir" "$subjects_dir" "$subject_ids"

#register to symmetric fsaverage xhemi
echo "Creating registration to template surface"
bash "$script_dir"/create_xhemi.sh "$subjects_dir" "$subject_ids"

#create basic features
echo "Sampling features in native space"
bash "$script_dir"/sample_FLAIR_smooth_features.sh "$subjects_dir" "$subject_ids" "$script_dir"
echo "Filtering intrinsic curvature"
python "$script_dir"/filter_intrinsic_curvature.py "$subjects_dir" "$subject_ids"

#normalise intrasubject
echo "Intrasubject normalisation"
python "$script_dir"/intrasubject_normalisation.py "$subjects_dir" "$subject_ids"
echo "Moving features to template surface"
bash "$script_dir"/move_to_xhemi_flip.sh "$subjects_dir" "$subject_ids"
echo "Moving lesion masks to template surface"
bash "$script_dir"/lesion_labels.sh "$subjects_dir" "$subject_ids"

#calculates if there are enough (>20) controls
#create the mu and std overlays for  normalisation of controls and patients
python "$script_dir"/create_control_subjects.py "$subjects_dir" "$subject_ids" "$script_dir"/template_control/


#normalise intersubject by mu and std
echo "normalising by controls"
python "$script_dir"/normalise_by_controls.py "$subjects_dir" "$subject_ids" "$script_dir"/template_control/


#create training_data matrix for all patients and controls.
echo "creating final training data matrix"

rm "$subjects_dir"/MELD_*.hdf5
python "$script_dir"/create_training_data_hdf5.py "$subjects_dir" "$subject_ids"
