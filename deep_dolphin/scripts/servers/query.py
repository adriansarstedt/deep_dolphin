from pydicom.dataset import Dataset

from pynetdicom import AE, debug_logger, StoragePresentationContexts, QueryRetrievePresentationContexts
from pynetdicom.sop_class import StudyRootQueryRetrieveInformationModelFind
from pynetdicom.sop_class import CTImageStorage, MRImageStorage
from pynetdicom.pdu_primitives import SCP_SCU_RoleSelectionNegotiation

debug_logger()

ae = AE()

# To show which protocols are working and not vv
# ae.requested_contexts = StoragePresentationContexts
ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)

# Create our Identifier (query) dataset
ds = Dataset()
ds.StudyDescription = '*'
ds.PatientName = '*'
ds.StudyDescription = '*'
ds.SeriesDescription = '*'
ds.QueryRetrieveLevel = 'SERIES'

# Associate with the peer AE at IP 127.0.0.1 and port 11112
assoc = ae.associate('127.0.0.1', 11112)
if assoc.is_established:
    # Send the C-FIND request
    print("Association established")
    responses = assoc.send_c_find(ds, StudyRootQueryRetrieveInformationModelFind)

    print("{} {} mathched your query".format(len(list(responses)), ds.QueryRetrieveLevel))

    for (status, identifier) in responses:
        # type(identifier) = pydicom.dataset.Dataset
        if status:
            print()
            print('C-FIND query status: 0x{0:04X}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()
else:
    print('Association rejected, aborted or never connected')
