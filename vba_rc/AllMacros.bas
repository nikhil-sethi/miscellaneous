Attribute VB_Name = "NewMacros"
Sub Fill_all()
Attribute Fill_all.VB_ProcData.VB_Invoke_Func = "Normal.NewMacros.Macro1"
'
' Macro1 Macro
'
'
Dim objExcel As Object '
Set objExcel = CreateObject("Excel.Application")
' Get class_list sheet
Set wb = Workbooks.Open("D:\vba_test\source_sheet.xlsx")
Set c_list = wb.Sheets("class_list")

Dim max_students As Integer
Dim student_rating As String

num_students = c_list.UsedRange.Rows.Count - 1

For i = 1 To num_students
    ' create document copy, set docname = student name
    ' make copy active
    ' get child rating from sheet
    ' set initial and final box values
    ' for each textbox
        ' set textbox(j).text to jth row and random column 'rating' sheet
    
    student_name = c_list.Range("C" & i + 1).Value
    student_rating = c_list.Range("E" & i + 1).Value
    
    save_source = "D:\vba_test\"
    doc_name = student_name & ".docx"
    
    'Copy doc
    WordBasic.CopyFileA FileName:=save_source & ActiveDocument.Name, _
    Directory:=save_source & doc_name
    'Make active
    Documents.Open (save_source & doc_name)
    'Set initial and final boxes
    Set s = ActiveDocument.Shapes
    's(8).TextFrame.TextRange.Text = 'academic year from
    's(9).TextFrame.TextRange.Text = 'academic year from
    s(10).TextFrame.TextRange.Text = student_name
    's(11).TextFrame.TextRange.Text = "class"
    s(12).TextFrame.TextRange.Text = c_list.Range("D" & i + 1).Value 'DOB
    's(13).TextFrame.TextRange.Text = 'Section
    s(14).TextFrame.TextRange.Text = c_list.Range("B" & i + 1).Value 'Admission number
    s(46).TextFrame.TextRange.InsertBefore (c_list.Range("G" & i + 1).Value) 'remarks
    s(47).TextFrame.TextRange.Text = c_list.Range("F" & i + 1).Value 'attendance
    's(48).TextFrame.TextRange.Text = "Teacher name"
    's(49).TextFrame.TextRange.Text = "Coordinator name"
    's(50).TextFrame.TextRange.Text = "head mistress name"
    's(52).TextFrame.TextRange.Text = "Principal name"
    
    Dim max_coms As Integer
Dim j As Integer
Dim oShape As Shape
    If ActiveDocument.Shapes.Count > 0 Then
        For j = 16 To 45 'ActiveDocument.Shapes.Count
            max_coms = WorksheetFunction.CountA(wb.Sheets(student_rating).Rows(j - 15))
            Set oShape = ActiveDocument.Shapes(j)
            If oShape.AutoShapeType = msoShapeRectangle Then 'we need to check both if oShape is of type msoShapeRectangle and its textframe contains place for writing
                If oShape.TextFrame.HasText = True Then
                    oShape.TextFrame.TextRange.Text = wb.Sheets(student_rating).Cells(j - 15, Int(1 + Rnd * (max_coms - 1 + 1))).Value
                    oShape.TextFrame.TextRange.Font.Name = "Arial"
                    oShape.TextFrame.TextRange.ParagraphFormat.LineSpacing = LinesToPoints(1.5)
                    oShape.TextFrame.TextRange.Font.Size = 12
                End If
            End If
        Next
    End If
ActiveDocument.Save
'Uncomment below to save as pdf
'ActiveDocument.ExportAsFixedFormat , OutputFileName:=student_name & ".pdf", _
     ExportFormat:=wdExportFormatPDF
ActiveDocument.Close
Next
End Sub

Sub Set_prop()


Dim oShape As Shape
If ActiveDocument.Shapes.Count > 0 Then
    For j = 13 To 13 'ActiveDocument.Shapes.Count
        Set oShape = ActiveDocument.Shapes(j)
        If oShape.AutoShapeType = msoShapeRectangle Then 'we need to check both if oShape is of type msoShapeRectangle and its textframe contains place for writing
            If oShape.TextFrame.HasText = True Then
                'oShape.TextFrame.TextRange.Font.Name = "Arial"
                'oShape.TextFrame.TextRange.Font.Size = 12
                'oShape.TextFrame.TextRange.ParagraphFormat.LineSpacing = LinesToPoints(1.5)
                
            End If
        End If
    Next
End If
ActiveDocument.Save
'ActiveDocument.Close



End Sub


Sub test()

Dim objExcel As Object '
Set objExcel = CreateObject("Excel.Application")
' Get class_list sheet
Set c_list = Workbooks.Open("D:\vba_test\source_sheet.xlsx").Sheets("class_list")

For i = 14 To 16
    If Not i = 13 Or 17 Or 22 Then
        save_source = "path_to _doc"
        img_source = "path_to_image" & i - 1 & ".jpg"
    
        student_name = c_list.Range("C" & i)
        doc_name = student_name & ".docx"
        'Make active
        Documents.Open (save_source & doc_name)
        ActiveDocument.GoTo(What:=wdGoToPage, Count:=1).Select
        Set aShape = Selection.InlineShapes.AddPicture(FileName:=img_source, _
              LinkToFile:=False, SaveWithDocument:=True).ConvertToShape
        With aShape
            .WrapFormat.Type = wdWrapTight
            .RelativeHorizontalPosition = wdRelativeHorizontalPositionPage
            .RelativeVerticalPosition = wdRelativeVerticalPositionPage
            .Top = CentimetersToPoints(8.72)
            .Left = CentimetersToPoints(6.94)
            .Select
        End With
            
        ActiveDocument.Save
        ActiveDocument.Close
    End If
Next
objExcel.Quit
End Sub
