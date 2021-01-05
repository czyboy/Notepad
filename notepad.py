import os
import wx

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        panel = wx.Panel(self)
        
        # 控件配置：2个TextCtrl + 3个Button
        self.file_path = wx.TextCtrl(panel)
        self.open_button = wx.Button(panel, label='打开')
        self.open_button.Bind(wx.EVT_BUTTON, self.open_select_file)
        self.save_button = wx.Button(panel, label='保存')
        self.save_button.Bind(wx.EVT_BUTTON, self.save_file)
        self.save_as_button = wx.Button(panel, label='另存为')
        self.save_as_button.Bind(wx.EVT_BUTTON, self.save_file_as)
        self.close_button = wx.Button(panel, label='关闭')
        self.close_button.Bind(wx.EVT_BUTTON, self.close_file)

        self.content_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.content_text.Bind(wx.EVT_TEXT, self.change_frame_title)
        #布局器配置：垂直(v_sizer)为主，包含水平(h_sizer)
        v_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer = wx.BoxSizer()
        
        h_sizer.Add(self.file_path, proportion=5, flag=wx.EXPAND | wx.ALL, border=2)
        h_sizer.Add(self.open_button, flag=wx.EXPAND | wx.ALL, border=2)
        h_sizer.Add(self.save_button, flag=wx.EXPAND | wx.ALL, border=2)
        h_sizer.Add(self.save_as_button, flag=wx.EXPAND | wx.ALL, border=2)
        h_sizer.Add(self.close_button, flag=wx.EXPAND | wx.ALL, border=2)
        
        v_sizer.Add(h_sizer, flag=wx.EXPAND | wx.ALL, border=5)
        v_sizer.Add(self.content_text, proportion=5, flag=wx.EXPAND | wx.ALL, border=5)
        panel.SetSizer(v_sizer)
        
        self.SetWindowStyle(self.GetWindowStyle() ^ wx.MAXIMIZE_BOX)

        self.Show()
     
    def open_file(self, path):
        try:
            with open(path, 'rb') as fp:
                self.file_path.SetValue(path)
                self.content_text.SetValue(fp.read())
        except Exception as e:
            dlg = wx.MessageDialog(None, e.__doc__, '错误提示', wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Close(True)
            dlg.Destroy()

    def change_frame_title(self, event):
        self.title = self.GetTitle().split('*')
        if len(self.title) > 1:
            return None
        self.SetTitle('*' + self.title[-1] + ' - ' + '文本编辑')

    def open_select_file(self, event):
        file_wildcard = '文本文档(*.txt)|*.txt|所有文件(*.*)|*.*'
        dlg = wx.FileDialog(
            None, 
            '选择文件', 
            os.getcwd(), 
            '', 
            file_wildcard,
            wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.SetTitle(dlg.GetPath().split('\\')[-1])
            self.open_file(dlg.GetPath())
        dlg.Destroy()

    def save_file(self, event):
        try:
            with open(self.file_path.GetValue(), 'w') as fp:
                fp.write(self.content_text.GetValue())
                
        except Exception as e:
            dlg = wx.MessageDialog(None, e.__doc__, '错误提示', wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Close(True)
            dlg.Destroy()

    def save_file_as(event):
        pass
    def close_file(event):
        pass

def main():
    app = wx.App()
    main_frame = MainFrame(None, title='无标题 - 文本编辑', pos=(600, 300), size=(800, 400))
    app.SetTopWindow(main_frame)
    app.MainLoop()
if __name__ == '__main__':
    main()