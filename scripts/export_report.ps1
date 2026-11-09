# Mở báo cáo .docx bằng Microsoft Word (COM), cập nhật mục lục + field, lưu, xuất PDF cùng tên.
#   powershell -ExecutionPolicy Bypass -File scripts/export_report.ps1 [-Docx baocao\<file>.docx]
param([string]$Docx = "baocao\10-250201078-2502010484-250201058.docx")

$path = (Resolve-Path $Docx).Path
$pdf = [IO.Path]::ChangeExtension($path, ".pdf")
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($path, $false, $false)
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Fields.Update() | Out-Null
    $doc.Repaginate()
    foreach ($toc in $doc.TablesOfContents) { $toc.UpdatePageNumbers() }
    $doc.Save()
    $doc.ExportAsFixedFormat($pdf, 17)          # 17 = wdExportFormatPDF
    $pages = $doc.ComputeStatistics(2)          # 2 = wdStatisticPages
    $doc.Close($false)
    Write-Output "OK: $pdf ($pages trang)"
}
finally {
    $word.Quit()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
}
