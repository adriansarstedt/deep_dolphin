from pynetdicom import AE, evt, StoragePresentationContexts, debug_logger
from pydicom import dcmread
import os
from pynetdicom.sop_class import MRImageStorage

debug_logger()

# Implement a handler for evt.EVT_C_STORE
def handle_store(event):
    """Handle a C-STORE request event."""
    # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
    ds = event.dataset

    # Add the File Meta Information
    ds.file_meta = event.file_meta

    # Save the dataset using the SOP Instance UID as the filename

    if ds.SOPClassUID == MRImageStorage:
        base_data_dir = "./"
        data_dir = os.path.join(base_data_dir, ds.StudyInstanceUID, ds.ProtocolName)

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        ds.save_as(
            os.path.join(data_dir, ds.SOPInstanceUID + ".dcm"),
            write_like_original=False,
        )

    print("Dataset Start")
    print(ds)
    print("Dataset End")

    # Return a 'Success' status
    return 0x0000


handlers = [(evt.EVT_C_STORE, handle_store)]

# Initialise the Application Entity
ae = AE()

# Read in our DICOM CT dataset
# Read in our DICOM CT dataset
ds_compressed = dcmread("./compressed_dicom_example.dcm")
for context in StoragePresentationContexts:
    ae.add_supported_context(context.abstract_syntax)
    # should probably add the normal transfer syntax as well
    # want to make sure this works with both compressed and uncompressed
    # also should refine what contexts we actually need
    # should only be the MR_Image
    # this can be tested using the debug_logger()

# Start listening for incoming association requests
ae.start_server(("", 11118), evt_handlers=handlers)
