Set fso = CreateObject("Scripting.FileSystemObject")
Set ws = CreateObject("WScript.Shell")
currDir = fso.GetParentFolderName(WScript.ScriptFullName)
desktop = ws.SpecialFolders("Desktop")

shortcutName = "G" & ChrW(246) & "rev ve Al" & ChrW(305) & ChrW(351) & "kanl" & ChrW(305) & "k Takibi.lnk"
Set shortcut = ws.CreateShortcut(desktop & "\" & shortcutName)
shortcut.TargetPath = currDir & "\baslat.bat"
shortcut.WorkingDirectory = currDir
shortcut.IconLocation = currDir & "\images\ToDo.ico,0"
shortcut.Description = "AI Destekli G" & ChrW(246) & "rev ve Al" & ChrW(305) & ChrW(351) & "kanl" & ChrW(305) & "k Takip Program" & ChrW(305)
shortcut.Save

msg = "Masa" & ChrW(252) & "st" & ChrW(252) & "n" & ChrW(252) & "ze 'G" & ChrW(246) & "rev ve Al" & ChrW(305) & ChrW(351) & "kanl" & ChrW(305) & "k Takibi' k" & ChrW(305) & "sayolu ba" & ChrW(351) & "ar" & ChrW(305) & "yla eklendi!"
title = "K" & ChrW(305) & "sayol Kurulumu"

MsgBox msg, 64, title
