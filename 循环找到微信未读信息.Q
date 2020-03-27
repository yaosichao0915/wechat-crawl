[General]
SyntaxVersion=2
BeginHotkey=121
BeginHotkeyMod=0
PauseHotkey=0
PauseHotkeyMod=0
StopHotkey=123
StopHotkeyMod=0
RunOnce=1
EnableWindow=
MacroID=e97247f9-b7ae-4a65-a1e1-67dbb3b8d0d5
Description=寻找公众号未读信息
Enable=0
AutoRun=0
[Repeat]
Type=0
Number=1
[SetupUI]
Type=2
QUI=
[Relative]
SetupOCXFile=
[Comment]

[Script]

odt = 72
maxh = 650
miss = 0
missD = 0
//循环读取订阅号中未读信息，微信客户端需要全屏，微信内置浏览器需要全屏//
//Call Main()
Call StartDingyue()
Function Main()
	odt = 72
	MoveTo 109, odt
	
	For 10
	Delay 500
	MouseWheel + 50
	Next

	Delay 1000
While True
	MoveTo 109, odt
	GetColor = GetPixelColor(109, odt)
	If GetColor = "303BFF"  Then
		TracePrint "找到未读信息，颜色为：" & GetColor
		Call startGZH()
		miss = 0
	Else 
		TracePrint "没有找到未读信息，颜色为：" & GetColor
		miss = miss + 1
	End If
	odt = odt + 3
	
	If odt >= maxh Then 
		MouseWheel - 5 
		odt = 72
	End If
	If miss >= 300 Then 
		Call StartDingyue()

	End If
	Delay 100
Wend
End Function

Function StartDingyue()
	odt=72
	MoveTo 147, 39
	Delay 1312
	LeftClick 1
	Delay 1791
	SayString "BioData"
	Delay 1791
	MoveTo 146, 117
	Delay 1784
	LeftClick 1
	MoveTo 297, odt
	
	For 10
	Delay 500
	MouseWheel + 50
	Next
	Delay 1000
	
	While True
		MoveTo 297, odt
		GetColor = GetPixelColor(297, odt)
		If GetColor = "303BFF"  Then
			TracePrint "找到未读信息，颜色为：" & GetColor
			Call startDYH()
			missD=0
		Else 
			TracePrint "没有找到未读信息，颜色为：" & GetColor
			missD = missD + 1
		End If
		odt = odt + 3
		
		If odt >= maxh Then 
			MouseWheel - 5 
			odt = 73
		End If
		Delay 100
		If missD >= 300 Then 
			Call Main() 
		End If
	Wend
End Function
//进公众号，获取公众号文章列表//
Function startGZH()
    TracePrint "进入公众号！"

	startSp = 220
	LeftClick 1
	MoveTo 1344, 40
	Delay 800
	LeftClick 1
	Delay 800
	MoveTo 1250, startSp
	Delay 800
	
	While startSp < 400
		Shape2 = 924318289   
		shape = GetCursorShape(0)
		TracePrint "收拾：" & shape
		If shape = shape2  
			LeftClick 1
			Goto gos
		Else    
    		startSp = startSp + 1
    		MoveTo 1255, startSp
		End If
		Delay 80
	Wend
	Rem gos
	
	Delay 6000
	
	MoveTo 1104, 196
	Delay 2000
	RightClick 1
	Delay 2
	MoveTo 1127, 275
	Delay 1220
	LeftClick 1
	Delay 2000
	'ctrl shift x另存'
	KeyDown 17, 1
	KeyDown 16, 1
	KeyPress 83, 1
	KeyUp 16, 1
	KeyUp 17, 1
	
	Delay 1500
	
	KeyPress "Enter", 1
	
	Delay 1000
	
	KeyDown 18, 1
	KeyPress 70, 1
	KeyUp 18, 1
	
	Delay 500
	
	KeyPress "X", 1
	
	Delay 1000
	
    KeyPress "Esc", 1
	
	TracePrint "退出公众号！"

End Function

Function startDYH()
    TracePrint "进入订阅号！"

	startSp = 227
	LeftClick 1
	MoveTo 1346, 39
	Delay 1500
	LeftClick 1
	MoveTo 1278, 70
	Delay 1500
	LeftClick 1
	MoveTo 1344, 40
	Delay 1500
	LeftClick 1
	MoveTo 1251, 231
	Delay 1500
	LeftClick 1
	MoveTo 1255, startSp
	Delay 1000
	
	While True
		Shape2 = 924318289   
		shape = GetCursorShape(0)
		TracePrint "收拾：" & shape
		If shape = shape2  
			LeftClick 1
			Goto gos
		Else    
    		startSp = startSp + 1
    		MoveTo 1255, startSp
		End If
		Delay 100
	Wend
	Rem gos
	Delay 6000
	
	MoveTo 1104, 196
	Delay 2000
	RightClick 1
	Delay 2
	MoveTo 1127, 275
	Delay 1220
	LeftClick 1
	Delay 2000
	'ctrl shift x另存'
	KeyDown 17, 1
	KeyDown 16, 1
	KeyPress 83, 1
	KeyUp 16, 1
	KeyUp 17, 1
	
	Delay 1500
	
	KeyPress "Enter", 1
	
	Delay 1000
	
	KeyDown 18, 1
	KeyPress 70, 1
	KeyUp 18, 1
	
	Delay 500
	
	KeyPress "X", 1
	
	Delay 1000
	
    KeyPress "Esc", 1
	
	TracePrint "退出公众号！"

End Function