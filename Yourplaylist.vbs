Set WshShell = CreateObject("WScript.Shell")
strDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.Run chr(34) & strDirectory & "\yourplaylist_config.bat" & Chr(34), 0
Set WshShell = Nothing