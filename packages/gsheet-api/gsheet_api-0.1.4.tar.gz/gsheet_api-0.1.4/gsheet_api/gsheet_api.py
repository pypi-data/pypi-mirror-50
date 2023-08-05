from datetime import datetime
import logging

import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from pytz import timezone

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GSheetAPI(object):
    """
    Easily and efficiently manage a Google Sheet.

    Notes:
        - Credentials required are the Google Service account json file
        - Sheet must be shared with edit access to the `client_email` found the the service account
        - Credentials can be entered as a dictionary or a file path to a json file. If you are sing a file path, set the
            `credentials_from_path` argument to True

    Usage Example:
        gsheet = GSheetAPI(..)  # initialize the class
        gsheet.sheet_to_df(..)  # import data from the sheet to a Pandas DataFrame

        gsheet.change_gsheet(..)  # switch to a new Google Sheet to work off of
        gsheet.get_cell(..)  # get the contents of a single cell

        gsheet.change_tab(..)  # switch to a new tab in the current working Google Sheet
        gsheet.set_cell(..)  # set the value of a single cell
        gsheet.df_to_sheet(..)  # export a Pandas DataFrame to the current working sheet
        gsheet.timestamp_to_cell(..)  # export a timestamp to a single cell in the sheet
    """
    def __init__(self, credentials, sheet_id, tab_name):
        """
        Initializes the GSheetAPI and sets the current working sheet and current working tab
        :param dict|str credentials: Dictionary containing your Google Service Account json blob or a file
            path entered as a string
        :param str sheet_id: Sheet id found in the Google Sheet URL
        :param str tab_name: Name of the tab to use within the Google Sheet
        """
        scope = ['https://spreadsheets.google.com/feeds']
        if isinstance(credentials, str):
            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
        elif isinstance(credentials, dict):
            creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
        else:
            raise TypeError("Credentials must be either a dictionary or a file path to a .json file")
        self.gs = gspread.authorize(creds)
        self.wks = self.gs.open_by_key(sheet_id)
        self.sht = self.wks.worksheet(tab_name)
        logger.info('Working sheet set to tab `{}` of `{}`'.format(tab_name, self.wks.title))

    def change_gsheet(self, sheet_id, tab_name):
        """
        Changes the current working sheet
        :param str sheet_id: Sheet id found in the Google Sheet URL
        :param str tab_name: Name of the tab to use within the Google Sheet
        """
        self.wks = self.gs.open_by_key(sheet_id)
        self.sht = self.wks.worksheet(tab_name)
        logger.info('Working sheet set to tab `{}` of `{}`'.format(tab_name, self.wks.title))

    def change_tab(self, tab_name):
        """
        Changes the working tab name within the current sheet
        :param str tab_name: Name of the tab to use within the Google Sheet
        """
        self.sht = self.wks.worksheet(tab_name)
        logger.info('Working tab set to `{}`'.format(tab_name))

    def df_to_sheet(self, df_input, row_start, col_start,
                    clear_sheet=False, clear_range=None, allow_formulas=True,
                    include_index=False, resize=False, include_column_header=True):
        """
        Exports a Pandas DataFrame to a Google Sheet
        :param pandas.DataFrame df_input: DataFrame to export
        :param int row_start: Integer value of the row (starting at 1)
        :param int col_start: Integer value of the column (starting at 1)
        :param bool clear_sheet: (default False) If the entire sheet should be cleared before dumping data
        :param bool clear_range: (default None) A range that should be cleared (eg. 'A1:B12')
        :param bool allow_formulas: (default True) Whether or not formulas should be executed or shown as a raw string
        :param bool include_index: (default False) Whether or not the DataFrame index should be shown in the sheet
        :param bool resize: (default False) If the sheet should resize when the data is too large to fit in the sheet
        :param bool include_column_header: (default True) If the data header should be dumped into the sheet
        """
        col_num = df_input.shape[1] + col_start - 1
        row_num = df_input.shape[0] + row_start - 1
        if clear_sheet:
            self.sht.clear()
        elif clear_range:
            cell_range = self.sht.range(clear_range)
            for cell in cell_range:
                cell.value = ''
            self.sht.update_cells(cell_range)

        set_with_dataframe(worksheet=self.sht,
                           dataframe=df_input,
                           row=row_start,
                           col=col_start,
                           include_index=include_index,
                           include_column_header=include_column_header,
                           resize=resize,
                           allow_formulas=allow_formulas)

        logger.info('{} rows and {} columns exported to `{}` starting in row {} and '
                    'column {}'.format(row_num, col_num, self.sht.title, row_start, col_start))

    def sheet_to_df(self, col_list, header, evaluate_formulas):
        """
        Grabs data from a Google Sheet and returns it as a Pandas DataFrame
        :param list col_list: List of ints representing the column number to extract (eg. range(0, 4) for [0, 1, 2, 3])
        :param int header: Integer of the row to use as a column (0 indexed)
        :param bool evaluate_formulas: Whether or not the formulas should be computed before extracting the cell content
        :return pandas.DataFrame: The sheet contents as a DataFrame object
        """
        df = get_as_dataframe(self.sht, parse_date=True, usecols=col_list, header=header,
                              evaluate_formulas=evaluate_formulas).dropna(how='all')
        return df

    def timestamp_to_cell(self, cell, fmt="%Y-%m-%d %H:%M %Z", tz='US/Central'):
        """
        Exports a timestamp to a single cell in the Google Sheet
        :param str cell:
        :param str fmt: (default "%Y-%m-%d %H:%M %Z")
        :param str tz: (default "US/Central")
        """
        now_time = datetime.now(timezone(tz))
        self.sht.update_acell(cell, now_time.strftime(fmt))
        str_time = now_time.strftime(fmt)
        logger.info("`{}` exported to cell `{}` of `{}`".format(str_time, cell, self.sht.title))

    def set_cell(self, cell, cell_content):
        """
        Sets a cell to a given value
        :param str cell: Cell reference (eg. 'A2')
        :param str cell_content: Desired cell content
        """
        self.sht.update_acell(cell, cell_content)
        logger.info("Cell `{cell}` change to `{cell_content}`".format(**locals()))

    def get_cell(self, cell):
        """
        Gets the current value of a given cell in the sheet
        :param str cell: Cell reference (eg. 'A2')
        :return: The current contents of the cell
        """
        return self.sht.acell(cell).value
