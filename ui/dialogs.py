from ui import qtx


'''Standard buttons'''
YES     = qtx.QMessageBox.Yes
YES_ALL = qtx.QMessageBox.YesAll
NO      = qtx.QMessageBox.No
NO_ALL  = qtx.QMessageBox.NoAll
CANCEL  = qtx.QMessageBox.Cancel
SAVE    = qtx.QMessageBox.Save
DISCARD = qtx.QMessageBox.Discard


class Dialogs:
    '''Helper class for modal dialogs'''

    def __init__(self, parent=None):
        self.parent = parent

        # duplicate button values in instance - for convenience
        self.YES     = YES
        self.YES_ALL = YES_ALL
        self.NO      = NO
        self.NO_ALL  = NO_ALL
        self.CANCEL  = CANCEL
        self.SAVE    = SAVE
        self.DISCARD = DISCARD

    def error(self, message, title='Error', nostack=False):
        '''
        Displays error message in a dialog window. By default, shows exception stack as well.
        '''

        if not nostack and sys.exc_info()[0] != None:
            import traceback
            stack = traceback.format_exc(10)
            if stack:
                message += '\n' + stack

        qtx.QMessageBox.critical(self.parent, title, message)

    def warn(self, message, title='Warning'):
        '''
        Displays warning message in a dialog window.
        '''
        qtx.QMessageBox.warning(self.parent, title, message)

    def info(self, message, title='Info'):
        '''
        Displays informational message in a dialog window.
        '''
        qtx.QMessageBox.information(self.parent, title, message)

    def confirm(self, message, title='Confirm', default_button=None):
        '''
        Confirms an action.
        '''
        return qtx.QMessageBox.question(
            self.parent,
            title,
            message,
            YES | CANCEL,
            defaultButton=default_button or CANCEL
        ) == YES

    def overwrite_question(self, message, title='Overwrite'):
        '''
        Confirms resource overwrite.
        '''

        return qtx.QMessageBox.question(
            self.parent, title, message,
            YES | YES_ALL | NO | NO_ALL | CANCEL
        )

    def save_question(self, message, title='Save'):
        '''
        Pops up save question.
        '''

        return qtx.QMessageBox.information(
            self.parent,
            title,
            message,
            SAVE | DISCARD | CANCEL
        )

    def open_file(self, default_file, mask, title='Open file', validator=None):
        '''
        File open for read dialog.
        '''

        if mask:
            masks = mask + ';;All files (*.*)'
            initial_mask = masks
        else:
            masks = 'All files (*.*)'
            initial_mask = masks

        print(initial_mask)

        while True:
            file_name, _ = qtx.QFileDialog.getOpenFileName(
                self.parent, title, default_file, masks, initial_mask)
            if not file_name:
                return None
            try:
                if validator:
                    validator(file_name)
                return file_name
            except ValueError as e:
                self.error(str(e))
                continue

    def open_files(self, default_file, mask, title='Open files'):
        '''
        File open for read dialog.
        '''

        if mask:
            masks = mask + ';;All files (*.*)'
            initial_mask = masks
        else:
            masks = 'All files (*.*)'
            initial_mask = masks

        while True:
            file_names, _ = qtx.QFileDialog.getOpenFileNames(
                self.parent, title, default_file, masks, initial_mask)
            if not file_names:
                return None
            return file_names

    def open_dir(self, default_dir, title='Open directory', validator=None):
        '''
        File open for read dialog.
        '''

        while True:
            file_name = qtx.QFileDialog.getExistingDirectory(self.parent, title, default_dir)
            if not file_name:
                return None
            try:
                if validator:
                    validator(file_name)
                return file_name
            except ValidationError as e:
                self.error(str(e))
                continue

    def save_file(self, default_file, mask, title='Save file'):
        '''
        File open for write dialog.
        '''

        if mask:
            masks = mask + ';;All files (*.*)'
            initial_mask = masks
        else:
            masks = 'All files (*.*)'
            initial_mask = masks

        file_name, _ = qtx.QFileDialog.getSaveFileName(self.parent, title, default_file, masks, initial_mask)
        if not file_name:
            return None
        return file_name
