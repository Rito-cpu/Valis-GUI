import sys
import subprocess


def start_valis_process(settings_data: dict = None):
    """
        # Example usage
        data_dict = {
            'text': widget.text()
        }

        argument = data_dict['text']
        command = f'echo {argument}'
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                text=True,
                capture_output=True
            )
            print(f'Command Output: {result.stdout}')
        except subprocess.CalledProcessError as e:
            print(f'An error occurred: {e})
    """
    if settings_data:
        # Setting Categories
        process_data = settings_data['processing_settings']
        rigid_data = settings_data['rigid_settings']
        non_rigid_settings = settings_data['non_rigid_settings']

        # Process Category
        proc_max_size = process_data['maximum_size']
        proc_type = process_data['process_type']
        proc_opt = process_data['options']
        # TODO: How do we handle different data from processing options since it has various attributes?

        # Rigid Category
        rigid_detector = rigid_data['detector']
        rigid_descriptor = rigid_data['descriptor']
        rigid_matching_metric = rigid_data['matching_metric']
        rigid_similarity_metric = rigid_data['similarity_metric']
        rigid_image_scaling = rigid_data['image_scaling']
        rigid_maximize_mi = rigid_data['maximize_mi']
        use_non_rigid = rigid_data['use_non_rigid']

        # Non-Rigid Category
        non_rigid_method = non_rigid_settings['method']

        # TODO: Create command that runs valis-wsi software with parameters retreived from dictionary
        valis_command = f'echo {rigid_detector}'

        try:
            result = subprocess.run(
                valis_command,
                shell=True,
                check=True,
                text=True,
                capture_output=True
            )
            print(f'Command Output: {result.stdout}')
        except subprocess.CalledProcessError as e:
            print(f'An error occurred: {e}')
    else:
        print('No data given!')
