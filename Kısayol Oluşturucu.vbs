Set fso = CreateObject("Scripting.FileSystemObject")
Set ws = CreateObject("WScript.Shell")
currDir = fso.GetParentFolderName(WScript.ScriptFullName)
desktop = ws.SpecialFolders("Desktop")

Set shortcut = ws.CreateShortcut(desktop & "\Görev ve Alýþkanlýk Takibi.lnk")
shortcut.TargetPath = currDir & "\baslat.bat"
shortcut.WorkingDirectory = currDir
shortcut.IconLocation = currDir & "\images\ToDo.ico,0"
shortcut.Description = "AI Destekli Görev ve Alýþkanlýk Takip Programý"
shortcut.Save

MsgBox "Masaüstünüze 'Görev ve Alýþkanlýk Takibi' kýsayolu baþarýyla eklendi!", 64, "Kýsayol Kurulumu"
