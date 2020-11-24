from PyQt5 import QtWidgets
import BOMAnalysisGUI as Gui
import pandas as pd
import sys
import os


def explore():
    qfd = Gui.QtWidgets.QFileDialog()
    path = "bom-examples"
    filters = "bom(*.bom)"
    title = 'Выбрать BOM 1'
    file = QtWidgets.QFileDialog.getOpenFileName(qfd, title, path, filters)
    ui.lineEdit.setText(file[0])
    return file[0]


def explore_second():
    qfd = Gui.QtWidgets.QFileDialog()
    path = "bom-examples"
    filters = "bom(*.bom)"
    title = 'Выбрать BOM 2'
    file = QtWidgets.QFileDialog.getOpenFileName(qfd, title, path, filters)
    ui.lineEdit_2.setText(file[0])
    return file[0]


def compare():
    bom_1 = ui.lineEdit.text()
    bom_2 = ui.lineEdit_2.text()
    print('Сравниваем ', bom_1, 'и ', bom_2)

    pd.options.mode.chained_assignment = None

    # BOM1
    ind = bom_1.rfind('/') + 1
    path = bom_1[:ind]
    old_doc = bom_1[ind:].replace(r'.bom', '').replace(r' ', '')
    print('PATH:', path, 'BOM1:', old_doc)

    df1 = pd.read_csv(path + old_doc + '.bom', encoding='ISO-8859-1', sep=";", index_col='RefDes')
    del df1['Count']
    df1 = df1.fillna('-')

    # BOM2
    ind = bom_2.rfind('/') + 1
    path = bom_2[:ind]
    new_doc = bom_2[ind:].replace(r'.bom', '').replace(r' ', '')
    print('PATH:', path, 'BOM2:', new_doc)

    df2 = pd.read_csv(path + new_doc + '.bom', encoding='ISO-8859-1', sep=";", index_col='RefDes')
    del df2['Count']
    df2 = df2.fillna('-')

    ###
    res = pd.merge(df1, df2, how='outer', on='RefDes', suffixes=('_old', '_new'), indicator=True).sort_values(
        'RefDes')
    ###
    add = res.loc[res['_merge'] == 'right_only']
    add = add[['ComponentName_new', 'PatternName_new', 'Value_new']]
    ###
    remove = res.loc[res['_merge'] == 'left_only']
    remove = remove[['ComponentName_old', 'PatternName_old', 'Value_old']]
    ###
    change = res.loc[res['_merge'] == 'both']
    del change['_merge']

    change['ComponentName'] = f'-'
    change['PatternName'] = f'-'
    change['Value'] = f'-'

    for i in range(len(change)):
        old_c = change['ComponentName_old'][i]
        new_c = change['ComponentName_new'][i]
        old_p = change['PatternName_old'][i]
        new_p = change['PatternName_new'][i]
        old_v = change['Value_old'][i]
        new_v = change['Value_new'][i]
        if old_c != new_c:
            change['ComponentName'][i] = f'{old_c} --> {new_c}'
        if old_p != new_p:
            change['PatternName'][i] = f'{old_p} --> {new_p}'
        if old_v != new_v:
            change['Value'][i] = f'{old_v} --> {new_v}'

    change = change[['ComponentName', 'PatternName', 'Value']]

    drop_index = []
    for i in range(len(change)):
        if change['ComponentName'][i] == '-' and change['PatternName'][i] == '-' and change['Value'][i] == '-':
            drop_index.append(i)
    drop_index.reverse()
    for i in drop_index:
        change = change.drop(change.index[i])

    ###
    old_name = old_doc.split("\\")[-1]
    new_name = new_doc.split("\\")[-1]

    path += 'from_' + old_name + '_to_' + new_name + '/'
    try:
        os.mkdir(path)
    except OSError:
        pass

    add.rename(
        columns={'ComponentName_new': 'ComponentName', 'PatternName_new': 'PatternName', 'Value_new': 'Value'},
        inplace=True)
    remove.rename(
        columns={'ComponentName_old': 'ComponentName', 'PatternName_old': 'PatternName', 'Value_old': 'Value'},
        inplace=True)

    sep_df0 = pd.DataFrame(data=[['', '', '']], columns=add.columns,
                           index=['Платы', '', 'Измененных компонентов', 'Новых компонентов',
                                  'Удаленных компонентов', '',
                                  ''])
    sep_df0.index.name = 'RefDes'

    sep_df0['ComponentName'][0] = f'Старая {old_name}.bom'
    sep_df0['PatternName'][0] = f'>>>>>'
    sep_df0['Value'][0] = f'Новая {new_name}.bom'

    sep_df0['ComponentName'][2] = f'{len(change)}'
    sep_df0['ComponentName'][3] = f'{len(add)}'
    sep_df0['ComponentName'][4] = f'{len(remove)}'

    sep_df1 = pd.DataFrame(data=[['', '', '']], columns=add.columns, index=['Изменено'])
    sep_df1.index.name = 'RefDes'

    sep_df1['ComponentName'][0] = f'ComponentName'
    sep_df1['PatternName'][0] = f'PatternName'
    sep_df1['Value'][0] = f'Value'

    sep_df2 = pd.DataFrame(data=[['', '', '']], columns=add.columns, index=['', '', 'Добавлено'])
    sep_df2.index.name = 'RefDes'
    sep_df2['ComponentName'][2] = f'ComponentName'
    sep_df2['PatternName'][2] = f'PatternName'
    sep_df2['Value'][2] = f'Value'

    sep_df3 = pd.DataFrame(data=[['', '', '']], columns=add.columns, index=['', '', 'Удалено'])
    sep_df3.index.name = 'RefDes'
    sep_df3['ComponentName'][2] = f'ComponentName'
    sep_df3['PatternName'][2] = f'PatternName'
    sep_df3['Value'][2] = f'Value'

    frames = [sep_df0, sep_df1, change, sep_df2, add, sep_df3, remove]
    frames = pd.concat(frames)

    frames_filename = f'{path}{old_name}_to_{new_name}.csv'
    print(frames_filename)

    frames.to_csv(frames_filename, encoding='utf-8-sig', index=True, sep=';', header=None)

    ui.lineEdit_2.hide()
    ui.pushButton.hide()
    ui.pushButton_2.hide()

    ui.lineEdit.setText(frames_filename)

    ui.label_2.hide()
    ui.pushButton_5.setGeometry(Gui.QtCore.QRect(70, 2400, 290, 31))

    ui.label.setText(
        f"<html><head/><body><p><span style=\" font-size:17pt;\">Отчет сформирован</span></p></body></html>")
    ui.label.setGeometry(70, 65, 581, 41)

    os.startfile(f'{frames_filename}')

    return frames_filename


app = QtWidgets.QApplication(sys.argv)
dialog = QtWidgets.QDialog()
ui = Gui.Ui_Dialog(dialog)
ui.setupUi(dialog)
dialog.show()
ui.pushButton.clicked.connect(explore)
ui.pushButton_2.clicked.connect(explore_second)
ui.pushButton_5.clicked.connect(compare)
sys.exit(app.exec_())
