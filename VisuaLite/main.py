from modules import gui

#dirname = 'C:/_Projects/_REPO/_otherREPO/DataAnalysis/Visualite/FCM_B_C/FCM_C/LogExport202107061025/'
#print(dirname)
#
#csv_files_list = []
#for filename in fcm.os.listdir(dirname):
#    if filename.lower().endswith('.csv'):
#        csv_files_list.append(filename)
#print (csv_files_list)
#
#DataFiles = [dirname + x for x in csv_files_list if x.startswith('S')]
#AlarmFiles = [dirname + x for x in csv_files_list if x.startswith('A')]
#EventFiles = [dirname + x for x in csv_files_list if x.startswith('E')]
#
#import_success, mch_info, COs, LogsStandard, LogsAlarms, LogsEvents = fcm.import_data(DataFiles, AlarmFiles, EventFiles)
## mch_info: if all files are from the same machine it gets the value of first 3 rows of files, else it gets the name of wrong file
#
#if import_success:
#    df = fcm.ChangeOverToDF(COs[0], LogsStandard)
#
#    fig = fcm.Plot_ChangeOver(df, mch_info, LogsAlarms, LogsEvents)
#    fig.write_html("ChangeOver_test4ROWS.html", config={'displaylogo': False})
#    #fig.update_layout(autosize=False, width=1000, height=800)
#    #fig.show(config={'displaylogo': False})
#
#    fig2 = fcm.Plot_ChangeOver_simple(df)
#    fig2.write_html("ChangeOver_test1ROW.html", config={'displaylogo': False})
#    #fig2.update_layout(autosize=False, width=1000, height=800)
#    #fig2.show(config={'displaylogo': False})
#else:
#    print('Wrong File: ' + mch_info)

a = gui.App()
a.mainloop()