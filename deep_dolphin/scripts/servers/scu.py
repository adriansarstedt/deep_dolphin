from pydicom import dcmread
from pynetdicom import AE, debug_logger, StoragePresentationContexts
from pynetdicom.sop_class import MRImageStorage

debug_logger()

def send_rt_struct():
    ae = AE()

    # Add a requested presentation context
    # ae.add_requested_context(MRImageStorage)

    from pydicom.uid import JPEGLossless
    transfer_syntax = JPEGLossless

    # Read in our DICOM CT dataset
    ds_compressed = dcmread('./compressed_dicom_example.dcm')

    for context in StoragePresentationContexts:
        ae.add_requested_context(context.abstract_syntax, ds_compressed.file_meta.TransferSyntaxUID)
        # should probably add the normal transfer syntax as well
        # want to make sure this works with both compressed and uncompressed
        # also should refine what contexts we actually need
        # should only be the MR_Image
        # this can be tested using the debug_logger()

    # Associate with peer AE at IP 127.0.0.1 and port 11112
    assoc = ae.associate('127.0.0.1', 11112)
    if assoc.is_established:
        # Use the C-STORE service to send the dataset
        # returns the response status as a pydicom Dataset
        status = assoc.send_c_store(ds_compressed)

        # Check the status of the storage request
        if status:
            # If the storage request succeeded this will be 0x0000
            print('C-STORE request status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')

send_rt_struct()
