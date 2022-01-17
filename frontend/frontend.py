import PySimpleGUI as sg

sg.theme('BluePurple')
   
# Create Two Columns
menu_column1 = sg.Column([[sg.Text('Source Folder (absolute path):')],
                         [sg.Text('', key='-SOURCE_PATH_WARNING-')],
                         [sg.Text('Destination Folder (absolute path):')],
                         [sg.Text('', key='-DEST_PATH_WARNING-')],
                         [sg.Text('Root Folder Name:')]])
menu_column2 = sg.Column([[sg.Input(key='-SOURCE_PATH-')],
                         [sg.Checkbox('Include files from all sub-folders', key='-RECURSIVE-')],
                         [sg.Input(key='-DEST_PATH')],
                         [sg.Checkbox('Replace existing folders', key='-REPLACE-'), sg.Checkbox('Create empty folders', key='-CREATE_EMPTY-')],
                         [sg.Input(key='-ROOT_NAME-')]])

folder_view = sg.Frame('Folder View', [[sg.Text('Current Folder:'), sg.Text('Folder1', key='-CURRENT_FOLDER_NAME_TEXT-')],
                                       [sg.Text('Child Folders:'), sg.Button('Add Subfolder', key='-ADD_SUBFOLDER-'), sg.Button('Clear All', key='-CLEAR_ALL_CHILD_FOLDERS-')],
                                       [sg.Column([[]], scrollable=True)],
                                       [sg.Text('Filters:'), sg.Button('Add Filter', key='-ADD_FILTER-'), sg.Button('Clear All', key='-CLEAR_ALL_FILTERS-')],
                                       [sg.Column([[]], scrollable=True)]], key='-FOLDER_VIEW-')
filter_view = sg.Frame('Filter View', [[]], key='-FILTER_VIEW-')
side_menu = sg.Column([[folder_view],
                       [filter_view]])

folder_structure = sg.Frame('Folder Structure', [[sg.Column([[]], scrollable=True)]])

log_window = sg.Frame('Log Window', [[sg.Button('Export To:', key='-EXPORT_LOG-'), sg.Input(key='-LOG_PATH-')],
                                     [sg.Multiline("lafjdlk fljdskl fkldjlf d fj dlfj df\ndjfldja fldfj kld flkj dklf jld fj\ndjflk daklfj dlkjf lkdjlfk dlkj fld\nsfdjfkld lfjdskl jflkdsj lfjdlkfjdsl f")]])
main_window = sg.Column([[sg.Button('Organize Folder!', key='-SUBMIT-'), sg.Text('', key='-SUBMIT_WARNING-')],
                         [menu_column1, menu_column2],
                         [folder_structure],
                         [log_window]])

layout = [[sg.Text('Your typed characters appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [side_menu, main_window],
          [sg.Button('Display'), sg.Button('Exit')]]
  
window = sg.Window('Introduction', layout, finalize=True)

# window.bind('<Configure>', "Configure")
output = window['-OUTPUT-']
  
while True:
    event, values = window.read()
    print(event, values)
      
    if event in  (None, 'Exit'):
        break
      
    if event == 'Display':
        # Update the "output" text element
        # to be the value of "input" element
        window['-OUTPUT-'].update(values['-SOURCE_PATH-'])

    elif event == 'Configure':
        if window.TKroot.state() == 'zoomed':
            output.update(value='Window zoomed and maximized !')
        else:
            window['-OUTPUT-'].update(value='Window normal')
  
window.close()