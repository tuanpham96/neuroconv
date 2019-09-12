from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QAction, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QGroupBox, QComboBox,
    QCheckBox)
from datetime import datetime
import numpy as np

class GroupGeneral(QGroupBox):
    def __init__(self, parent):
        """Groupbox for General fields filling form."""
        super().__init__()
        self.setTitle('General')
        self.group_name = 'General'

        self.lbl_file_path = QLabel('file_path:')
        self.lin_file_path = QLineEdit('')
        self.lbl_file_name = QLabel('file_name:')
        self.lin_file_name = QLineEdit('')

        self.grid = QGridLayout()
        self.grid.setColumnStretch(0, 0)
        self.grid.setColumnStretch(1, 0)
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lbl_file_path, 0, 0, 1, 2)
        self.grid.addWidget(self.lin_file_path, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_file_name, 1, 0, 1, 2)
        self.grid.addWidget(self.lin_file_name, 1, 2, 1, 4)

        self.setLayout(self.grid)

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['file_path'] = self.lin_file_path.text()
        data['file_name'] = self.lin_file_name.text()
        return data



class GroupNwbfile(QGroupBox):
    def __init__(self, parent):
        """Groupbox for NWBFile fields filling form."""
        super().__init__()
        self.setTitle('NWBFile')
        self.group_name = 'NWBFile'

        self.lbl_session_description = QLabel('session_description:')
        self.lin_session_description = QLineEdit("session_description")
        self.lin_session_description.setToolTip("a description of the session where "
            "this data was generated")

        self.lbl_identifier = QLabel('identifier:')
        self.lin_identifier = QLineEdit("ABC123")
        self.lin_identifier.setToolTip("a unique text identifier for the file")

        self.lbl_session_start_time = QLabel('session_start_time:')
        self.lin_session_start_time1 = QLineEdit(datetime.now().strftime("%d/%m/%Y"))
        self.lin_session_start_time1.setToolTip("the start date and time of the recording session")
        self.lin_session_start_time2 = QLineEdit(datetime.now().strftime("%H:%M"))
        self.lin_session_start_time2.setToolTip("the start date and time of the recording session")

        self.lbl_experimenter = QLabel('experimenter:')
        self.lin_experimenter = QLineEdit('')
        self.lin_experimenter.setPlaceholderText("Alan Lloyd Hodgkin, Andrew Fielding Huxley")
        self.lin_experimenter.setToolTip("comma-separated list of names of persons "
            "who performed experiment")

        self.lbl_experiment_description = QLabel('experiment_description:')
        self.lin_experiment_description = QLineEdit('')
        self.lin_experiment_description.setPlaceholderText("propagation of action "
            "potentials in the squid giant axon")
        self.lin_experiment_description.setToolTip("general description of the experiment")

        self.lbl_session_id = QLabel('session_id:')
        self.lin_session_id = QLineEdit('')
        self.lin_session_id.setPlaceholderText("LAB 0123")
        self.lin_session_id.setToolTip("lab-specific ID for the session")

        self.lbl_institution = QLabel('institution:')
        self.lin_institution = QLineEdit('')
        self.lin_institution.setPlaceholderText("institution")
        self.lin_institution.setToolTip("institution(s) where experiment is performed")

        self.lbl_lab = QLabel("lab:")
        self.lin_lab = QLineEdit('')
        self.lin_lab.setPlaceholderText("lab name")
        self.lin_lab.setToolTip("lab where experiment was performed")

        self.lbl_keywords = QLabel('keywords:')
        self.lin_keywords = QLineEdit('')
        self.lin_keywords.setPlaceholderText("action potential, ion channels, mathematical model")
        self.lin_keywords.setToolTip("comma-separated list of terms to search over")

        self.lbl_notes = QLabel("notes:")
        self.lin_notes = QLineEdit('')
        self.lin_notes.setPlaceholderText("Smells like a Nobel prize")
        self.lin_notes.setToolTip("Notes about the experiment")

        self.lbl_pharmacology = QLabel("pharmacology:")
        self.lin_pharmacology = QLineEdit('')
        self.lin_pharmacology.setPlaceholderText("pharmacology")
        self.lin_pharmacology.setToolTip("Description of drugs used, including how "
            "and when they were administered.\nAnesthesia(s), painkiller(s), etc., "
            "plus dosage, concentration, etc.")

        self.lbl_protocol = QLabel("protocol:")
        self.lin_protocol = QLineEdit('')
        self.lin_protocol.setPlaceholderText("protocol")
        self.lin_protocol.setToolTip("Experimental protocol, if applicable. E.g."
            " include IACUC protocol")

        self.lbl_related_pubications = QLabel("related pubications:")
        self.lin_related_pubications = QLineEdit('')
        self.lin_related_pubications.setPlaceholderText("related_pubications")
        self.lin_related_pubications.setToolTip("Publication information. PMID,"
            " DOI, URL, etc. If multiple, concatenate together \nand describe"
            " which is which")

        self.lbl_slices = QLabel("slices:")
        self.lin_slices = QLineEdit('')
        self.lin_slices.setPlaceholderText("slices")
        self.lin_slices.setToolTip("Description of slices, including information "
            "about preparation thickness, \norientation, temperature and bath solution")

        self.lbl_data_collection = QLabel("data_collection:")
        self.lin_data_collection = QLineEdit('')
        self.lin_data_collection.setPlaceholderText("data collection")
        self.lin_data_collection.setToolTip("Notes about data collection and analysis")

        self.lbl_surgery = QLabel("surgery:")
        self.lin_surgery = QLineEdit('')
        self.lin_surgery.setPlaceholderText("surgery")
        self.lin_surgery.setToolTip("Narrative description about surgery/surgeries, "
            "including date(s) and who performed surgery.")

        self.lbl_virus = QLabel("virus:")
        self.lin_virus = QLineEdit('')
        self.lin_virus.setPlaceholderText("virus")
        self.lin_virus.setToolTip("Information about virus(es) used in experiments, "
            "including virus ID, source, date made, injection location, volume, etc.")

        self.lbl_stimulus_notes = QLabel("stimulus_notes:")
        self.lin_stimulus_notes = QLineEdit('')
        self.lin_stimulus_notes.setPlaceholderText("stimulus notes")
        self.lin_stimulus_notes.setToolTip("Notes about stimuli, such as how and where presented.")

        grid = QGridLayout()
        grid.setColumnStretch(2, 1)
        grid.setColumnStretch(4, 1)
        grid.addWidget(self.lbl_session_description, 0, 0, 1, 2)
        grid.addWidget(self.lin_session_description, 0, 2, 1, 4)
        grid.addWidget(self.lbl_identifier, 1, 0, 1, 2)
        grid.addWidget(self.lin_identifier, 1, 2, 1, 4)
        grid.addWidget(self.lbl_session_start_time, 2, 0, 1, 2)
        grid.addWidget(self.lin_session_start_time1, 2, 2, 1, 2)
        grid.addWidget(self.lin_session_start_time2, 2, 4, 1, 2)
        grid.addWidget(self.lbl_experimenter, 3, 0, 1, 2)
        grid.addWidget(self.lin_experimenter, 3, 2, 1, 4)
        grid.addWidget(self.lbl_experiment_description, 4, 0, 1, 2)
        grid.addWidget(self.lin_experiment_description, 4, 2, 1, 4)
        grid.addWidget(self.lbl_session_id, 5, 0, 1, 2)
        grid.addWidget(self.lin_session_id, 5, 2, 1, 4)
        grid.addWidget(self.lbl_institution, 6, 0, 1, 2)
        grid.addWidget(self.lin_institution, 6, 2, 1, 4)
        grid.addWidget(self.lbl_lab, 7, 0, 1, 2)
        grid.addWidget(self.lin_lab, 7, 2, 1, 4)
        grid.addWidget(self.lbl_keywords, 8, 0, 1, 2)
        grid.addWidget(self.lin_keywords, 8, 2, 1, 4)
        grid.addWidget(self.lbl_notes, 9, 0, 1, 2)
        grid.addWidget(self.lin_notes, 9, 2, 1, 4)
        grid.addWidget(self.lbl_pharmacology, 10, 0, 1, 2)
        grid.addWidget(self.lin_pharmacology, 10, 2, 1, 4)
        grid.addWidget(self.lbl_protocol, 11, 0, 1, 2)
        grid.addWidget(self.lin_protocol, 11, 2, 1, 4)
        grid.addWidget(self.lbl_related_pubications, 12, 0, 1, 2)
        grid.addWidget(self.lin_related_pubications, 12, 2, 1, 4)
        grid.addWidget(self.lbl_slices, 13, 0, 1, 2)
        grid.addWidget(self.lin_slices, 13, 2, 1, 4)
        grid.addWidget(self.lbl_data_collection, 14, 0, 1, 2)
        grid.addWidget(self.lin_data_collection, 14, 2, 1, 4)
        grid.addWidget(self.lbl_surgery, 15, 0, 1, 2)
        grid.addWidget(self.lin_surgery, 15, 2, 1, 4)
        grid.addWidget(self.lbl_virus, 16, 0, 1, 2)
        grid.addWidget(self.lin_virus, 16, 2, 1, 4)
        grid.addWidget(self.lbl_stimulus_notes, 17, 0, 1, 2)
        grid.addWidget(self.lin_stimulus_notes, 17, 2, 1, 4)

        self.setLayout(grid)

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['session_description'] = self.lin_session_description.text()
        data['identifier'] = self.lin_identifier.text()
        str_datetime = self.lin_session_start_time1.text()+", "+self.lin_session_start_time2.text()
        data['session_start_time'] = datetime.strptime(str_datetime,'%d/%m/%Y, %H:%M')
        experimenter = self.lin_experimenter.text()
        data['experimenter'] = [ex.strip() for ex in experimenter.split(',')]
        data['experiment_description'] = self.lin_experiment_description.text()
        data['session_id'] = self.lin_session_id.text()
        data['institution'] = self.lin_institution.text()
        data['lab'] = self.lin_lab.text()
        keywords = self.lin_keywords.text()
        data['keywords'] = [kw.strip() for kw in keywords.split(',')]
        data['notes'] = self.lin_notes.text()
        data['pharmacology'] = self.lin_pharmacology.text()
        data['protocol'] = self.lin_protocol.text()
        data['related_pubications'] = self.lin_related_pubications.text()
        data['slices'] = self.lin_slices.text()
        data['data_collection'] = self.lin_data_collection.text()
        data['surgery'] = self.lin_surgery.text()
        data['virus'] = self.lin_virus.text()
        data['stimulus_notes'] = self.lin_stimulus_notes.text()
        return data



class GroupSubject(QGroupBox):
    def __init__(self, parent):
        """Groupbox for 'pynwb.file.Subject' fields filling form."""
        super().__init__()
        self.setTitle('Subject')
        self.group_name = 'Subject'

        self.lbl_age = QLabel('age:')
        self.lin_age = QLineEdit('')
        self.lin_age.setPlaceholderText("age")
        self.lin_age.setToolTip("the age of the subject")

        self.lbl_description = QLabel('description:')
        self.lin_description = QLineEdit('')
        self.lin_description.setPlaceholderText("description")
        self.lin_description.setToolTip("a description of the subject")

        self.lbl_genotype = QLabel('genotype:')
        self.lin_genotype = QLineEdit('')
        self.lin_genotype.setPlaceholderText("genotype")
        self.lin_genotype.setToolTip("the genotype of the subject")

        self.lbl_sex = QLabel('sex:')
        self.lin_sex = QLineEdit('')
        self.lin_sex.setPlaceholderText("sex")
        self.lin_sex.setToolTip("the sex of the subject")

        self.lbl_species = QLabel('species:')
        self.lin_species = QLineEdit('')
        self.lin_species.setPlaceholderText("species")
        self.lin_species.setToolTip("the species of the subject")

        self.lbl_subject_id = QLabel('subject_id:')
        self.lin_subject_id = QLineEdit('')
        self.lin_subject_id.setPlaceholderText("subject_id")
        self.lin_subject_id.setToolTip("a unique identifier for the subject")

        self.lbl_weight = QLabel('weight:')
        self.lin_weight = QLineEdit('')
        self.lin_weight.setPlaceholderText("weight")
        self.lin_weight.setToolTip("the weight of the subject")

        self.lbl_date_of_birth = QLabel('date_of_birth:')
        self.lin_date_of_birth = QLineEdit('')
        self.lin_date_of_birth.setPlaceholderText(datetime.now().strftime("%d/%m/%Y"))
        self.lin_date_of_birth.setToolTip("datetime of date of birth. May be "
            "supplied instead of age.")

        self.grid = QGridLayout()
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lbl_age, 0, 0, 1, 2)
        self.grid.addWidget(self.lin_age, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_description, 1, 0, 1, 2)
        self.grid.addWidget(self.lin_description, 1, 2, 1, 4)
        self.grid.addWidget(self.lbl_genotype, 2, 0, 1, 2)
        self.grid.addWidget(self.lin_genotype, 2, 2, 1, 4)
        self.grid.addWidget(self.lbl_sex, 3, 0, 1, 2)
        self.grid.addWidget(self.lin_sex, 3, 2, 1, 4)
        self.grid.addWidget(self.lbl_species, 4, 0, 1, 2)
        self.grid.addWidget(self.lin_species, 4, 2, 1, 4)
        self.grid.addWidget(self.lbl_subject_id, 5, 0, 1, 2)
        self.grid.addWidget(self.lin_subject_id, 5, 2, 1, 4)
        self.grid.addWidget(self.lbl_weight, 6, 0, 1, 2)
        self.grid.addWidget(self.lin_weight, 6, 2, 1, 4)
        self.grid.addWidget(self.lbl_date_of_birth, 7, 0, 1, 2)
        self.grid.addWidget(self.lin_date_of_birth, 7, 2, 1, 4)

        self.setLayout(self.grid)

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['age'] = self.lin_age.text()
        data['description'] = self.lin_description.text()
        data['genotype'] = self.lin_genotype.text()
        data['sex'] = self.lin_sex.text()
        data['species'] = self.lin_species.text()
        data['subject_id'] = self.lin_subject_id.text()
        data['weight'] = self.lin_weight.text()
        str_datetime = self.lin_date_of_birth.text()
        if len(str_datetime)>0:
            data['date_of_birth'] = datetime.strptime(str_datetime,'%d/%m/%Y')
        else:
            data['date_of_birth'] = ''
        return data



class GroupDevice(QGroupBox):
    def __init__(self, parent):
        """Groupbox for pynwb.device.Device fields filling form."""
        super().__init__()
        self.setTitle('Device')
        self.parent = parent
        self.group_name = 'Device'

        self.lbl_name = QLabel('name:')
        self.lin_name = QLineEdit('Device')
        self.lin_name.setToolTip("the name pof this device")
        nDevices = 0
        for grp in self.parent.groups_list:
            if isinstance(grp, GroupDevice):
                nDevices += 1
        if nDevices > 0:
            self.lin_name.setText('Device'+str(nDevices))

        self.grid = QGridLayout()
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lbl_name, 0, 0, 1, 2)
        self.grid.addWidget(self.lin_name, 0, 2, 1, 4)

        self.setLayout(self.grid)

    def refresh_objects_references(self):
        """Refreshes references with existing objects in parent group."""
        pass

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['name'] = self.lin_name.text()
        return data



class GroupOpticalChannel(QGroupBox):
    def __init__(self, parent):
        """Groupbox for pynwb.ophys.OpticalChannel fields filling form."""
        super().__init__()
        self.setTitle('OpticalChannel')
        self.parent = parent
        self.group_name = 'OpticalChannel'

        self.lbl_name = QLabel('name:')
        self.lin_name = QLineEdit('OpticalChannel')
        self.lin_name.setToolTip("the name of this optical channel")
        nOptCh = 0
        for grp in self.parent.groups_list:
            if isinstance(grp, GroupOpticalChannel):
                nOptCh += 1
        if nOptCh > 0:
            self.lin_name.setText('OpticalChannel'+str(nOptCh))

        self.lbl_description = QLabel('description:')
        self.lin_description = QLineEdit('description')
        self.lin_description.setToolTip("Any notes or comments about the channel")

        self.lbl_emission_lambda = QLabel('emission_lambda:')
        self.lin_emission_lambda = QLineEdit('0.0')
        self.lin_emission_lambda.setToolTip("Emission lambda for channel")

        self.grid = QGridLayout()
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lbl_name, 0, 0, 1, 2)
        self.grid.addWidget(self.lin_name, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_description, 1, 0, 1, 2)
        self.grid.addWidget(self.lin_description, 1, 2, 1, 4)
        self.grid.addWidget(self.lbl_emission_lambda, 2, 0, 1, 2)
        self.grid.addWidget(self.lin_emission_lambda, 2, 2, 1, 4)

        self.setLayout(self.grid)

    def refresh_objects_references(self):
        """Refreshes references with existing objects in parent group."""
        pass

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['name'] = self.lin_name.text()
        data['description'] = self.lin_description.text()
        try:
            data['emission_lambda'] = float(self.lin_emission_lambda.text())
        except:
            data['emission_lambda'] = 0.0
            print("'emission_lambda' must be a float")
        return data



class GroupImagingPlane(QGroupBox):
    def __init__(self, parent):
        """Groupbox for pynwb.ophys.ImagingPlane fields filling form."""
        super().__init__()
        self.setTitle('ImagingPlane')
        self.parent = parent
        self.group_name = 'ImagingPlane'

        self.lbl_name = QLabel('name:')
        self.lin_name = QLineEdit('ImagingPlane')
        self.lin_name.setToolTip("The name of this ImagingPlane")
        nImPl = 0
        for grp in self.parent.groups_list:
            if isinstance(grp, GroupImagingPlane):
                nImPl += 1
        if nImPl > 0:
            self.lin_name.setText('ImagingPlane'+str(nImPl))

        self.lbl_optical_channel = QLabel('optical_channel:')
        self.combo_optical_channel = QComboBox()
        self.combo_optical_channel.setToolTip("One of possibly many groups storing "
            "channelspecific data")

        self.lbl_description = QLabel('description:')
        self.lin_description = QLineEdit('description')
        self.lin_description.setToolTip("Description of this ImagingPlane")

        self.lbl_device = QLabel('device:')
        self.combo_device = QComboBox()
        self.combo_device.setToolTip("The device that was used to record")

        self.lbl_excitation_lambda = QLabel('excitation_lambda:')
        self.lin_excitation_lambda = QLineEdit('0.0')
        self.lin_excitation_lambda.setToolTip("Excitation wavelength in nm")

        self.lbl_imaging_rate = QLabel('imaging_rate:')
        self.lin_imaging_rate = QLineEdit('0.0')
        self.lin_imaging_rate.setToolTip("Rate images are acquired, in Hz")

        self.lbl_indicator = QLabel('indicator:')
        self.lin_indicator = QLineEdit('indicator')
        self.lin_indicator.setToolTip("Calcium indicator")

        self.lbl_location = QLabel('location:')
        self.lin_location = QLineEdit('location')
        self.lin_location.setToolTip("Location of image plane")

        self.lbl_manifold = QLabel('manifold:')
        self.chk_manifold = QCheckBox("Get from source file")
        self.chk_manifold.setChecked(False)
        self.chk_manifold.setToolTip("Physical position of each pixel. size=(height, "
            "width, xyz).\n Check box if this data will be retrieved from source file.\n"
            "Uncheck box to ignore it.")

        self.lbl_conversion = QLabel('conversion:')
        self.lin_conversion = QLineEdit('')
        self.lin_conversion.setPlaceholderText("1")
        self.lin_conversion.setToolTip("Multiplier to get from stored values to "
            "specified unit (e.g., 1e-3 for millimeters)")

        self.lbl_unit = QLabel('unit:')
        self.lin_unit = QLineEdit('')
        self.lin_unit.setPlaceholderText("meters")
        self.lin_unit.setToolTip("Base unit that coordinates are stored in (e.g., Meters)")

        self.lbl_reference_frame = QLabel('reference_frame:')
        self.lin_reference_frame = QLineEdit('')
        self.lin_reference_frame.setPlaceholderText("reference_frame")
        self.lin_reference_frame.setToolTip("Describes position and reference frame "
            "of manifold based on position of first element in manifold.")

        self.grid = QGridLayout()
        self.grid.setColumnStretch(5, 1)
        self.grid.addWidget(self.lbl_name, 0, 0, 1, 2)
        self.grid.addWidget(self.lin_name, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_optical_channel, 1, 0, 1, 2)
        self.grid.addWidget(self.combo_optical_channel, 1, 2, 1, 4)
        self.grid.addWidget(self.lbl_description, 2, 0, 1, 2)
        self.grid.addWidget(self.lin_description, 2, 2, 1, 4)
        self.grid.addWidget(self.lbl_device, 3, 0, 1, 2)
        self.grid.addWidget(self.combo_device, 3, 2, 1, 4)
        self.grid.addWidget(self.lbl_excitation_lambda, 4, 0, 1, 2)
        self.grid.addWidget(self.lin_excitation_lambda, 4, 2, 1, 4)
        self.grid.addWidget(self.lbl_imaging_rate, 5, 0, 1, 2)
        self.grid.addWidget(self.lin_imaging_rate, 5, 2, 1, 4)
        self.grid.addWidget(self.lbl_indicator, 6, 0, 1, 2)
        self.grid.addWidget(self.lin_indicator, 6, 2, 1, 4)
        self.grid.addWidget(self.lbl_location, 7, 0, 1, 2)
        self.grid.addWidget(self.lin_location, 7, 2, 1, 4)
        self.grid.addWidget(self.lbl_manifold, 8, 0, 1, 2)
        self.grid.addWidget(self.chk_manifold, 8, 2, 1, 2)
        self.grid.addWidget(self.lbl_conversion, 9, 0, 1, 2)
        self.grid.addWidget(self.lin_conversion, 9, 2, 1, 4)
        self.grid.addWidget(self.lbl_unit, 10, 0, 1, 2)
        self.grid.addWidget(self.lin_unit, 10, 2, 1, 4)
        self.grid.addWidget(self.lbl_reference_frame, 11, 0, 1, 2)
        self.grid.addWidget(self.lin_reference_frame, 11, 2, 1, 4)

        self.setLayout(self.grid)

    def refresh_objects_references(self):
        """Refreshes references with existing objects in parent group."""
        self.combo_optical_channel.clear()
        self.combo_device.clear()
        for grp in self.parent.groups_list:
            if isinstance(grp, GroupOpticalChannel):
                self.combo_optical_channel.addItem(grp.lin_name.text())
            if isinstance(grp, GroupDevice):
                self.combo_device.addItem(grp.lin_name.text())

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['name'] = self.lin_name.text()
        data['description'] = self.lin_description.text()
        try:
            data['excitation_lambda'] = float(self.lin_excitation_lambda.text())
        except:
            data['excitation_lambda'] = 0.0
        try:
            data['imaging_rate'] = float(self.lin_imaging_rate.text())
        except:
            data['imaging_rate'] = 0.0
        data['indicator'] = self.lin_indicator.text()
        data['location'] = self.lin_location.text()
        try:
            data['conversion'] = float(self.lin_conversion.text())
        except:
            data['conversion'] = 0.0
        data['unit'] = self.lin_unit.text()
        return data



class GroupOphys(QGroupBox):
    def __init__(self, parent):
        """Groupbox for Ophys module fields filling form."""
        super().__init__()
        self.setTitle('Ophys')
        self.group_name = 'Ophys'
        self.groups_list = []

        self.combo1 = CustomComboBox()
        self.combo1.addItem('-- Add group --')
        self.combo1.addItem('Device')
        self.combo1.addItem('OpticalChannel')
        self.combo1.addItem('ImagingPlane')
        self.combo1.setCurrentIndex(0)
        self.combo1.activated.connect(lambda: self.add_group('combo'))
        self.combo2 = CustomComboBox()
        self.combo2.addItem('-- Del group --')
        self.combo2.setCurrentIndex(0)
        self.combo2.activated.connect(lambda: self.del_group('combo'))

        self.lbl_f1 = QLabel('field1:')
        self.lin_f1 = QLineEdit('')
        self.lin_f1.setPlaceholderText("field_name")
        self.lin_f1.setToolTip("tooltip")

        self.vbox1 = QVBoxLayout()
        self.vbox1.addStretch()

        self.grid = QGridLayout()
        self.grid.setColumnStretch(5, 1)
        self.grid.addWidget(self.combo1, 1, 0, 1, 2)
        self.grid.addWidget(self.combo2, 1, 2, 1, 2)
        self.grid.addWidget(self.lbl_f1, 2, 0, 1, 2)
        self.grid.addWidget(self.lin_f1, 2, 2, 1, 4)
        self.grid.addLayout(self.vbox1, 3, 0, 1, 6)
        self.setLayout(self.grid)

        # Initiate with some sub-groups
        self.add_group(group_type='Device')
        self.add_group(group_type='OpticalChannel')
        self.add_group(group_type='ImagingPlane')

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['f1'] = self.lin_f1.text()
        return data

    def add_group(self, group_type):
        """Adds group form."""
        if group_type=='combo':
            group_type = str(self.combo1.currentText())
        if group_type == 'Device':
            item = GroupDevice(self)
        elif group_type == 'OpticalChannel':
            item = GroupOpticalChannel(self)
        elif group_type == 'ImagingPlane':
            item = GroupImagingPlane(self)
        if group_type != '-- Add group --':
            item.lin_name.textChanged.connect(self.refresh_del_combo)
            self.groups_list.append(item)
            nWidgetsVbox = self.vbox1.count()
            self.vbox1.insertWidget(nWidgetsVbox-1, item) #insert before the stretch
            self.combo1.setCurrentIndex(0)
            self.combo2.addItem(item.lin_name.text())
            self.refresh_children()

    def del_group(self, group_name):
        """Deletes group form by name."""
        if group_name=='combo':
            group_name = str(self.combo2.currentText())
        if group_name != '-- Del group --':
            nWidgetsVbox = self.vbox1.count()
            for i in range(nWidgetsVbox):
                if self.vbox1.itemAt(i) is not None:
                    if (hasattr(self.vbox1.itemAt(i).widget(), 'lin_name')) and \
                        (self.vbox1.itemAt(i).widget().lin_name.text()==group_name):
                        self.groups_list.remove(self.vbox1.itemAt(i).widget())   #deletes list item
                        self.vbox1.itemAt(i).widget().setParent(None)            #deletes widget
                        self.combo2.removeItem(self.combo2.findText(group_name))
                        self.combo2.setCurrentIndex(0)
                        self.refresh_children()

    def refresh_children(self):
        """Refreshes references with existing objects in child groups."""
        for child in self.groups_list:
            child.refresh_objects_references()

    def refresh_del_combo(self):
        """Refreshes del combobox with existing objects in child groups."""
        self.combo2.clear()
        self.combo2.addItem('-- Del group --')
        for child in self.groups_list:
            self.combo2.addItem(child.lin_name.text())




class GroupEphys(QGroupBox):
    def __init__(self, parent):
        """Groupbox for Ephys fields filling form."""
        super().__init__()
        self.setTitle('Ephys')
        self.group_name = 'Ephys'

        self.lbl_f1 = QLabel('field1:')
        self.lin_f1 = QLineEdit('')
        self.lin_f1.setPlaceholderText("field_name")
        self.lin_f1.setToolTip("tooltip")

        self.lbl_f2 = QLabel('field2:')
        self.lin_f2 = QLineEdit('')
        self.lin_f2.setPlaceholderText("field_name")
        self.lin_f2.setToolTip("tooltip")

        self.grid = QGridLayout()
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lbl_f1, 0, 0, 1, 2)
        self.grid.addWidget(self.lin_f1, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_f2, 1, 0, 1, 2)
        self.grid.addWidget(self.lin_f2, 1, 2, 1, 4)

        self.setLayout(self.grid)

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['f1'] = self.lin_f1.text()
        data['f2'] = self.lin_f2.text()
        return data



class CustomComboBox(QComboBox):
    def __init__(self):
        """Class created to ignore mouse wheel events on combobox."""
        super().__init__()

    def wheelEvent(self, event):
        event.ignore()
