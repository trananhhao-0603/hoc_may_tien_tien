# Xuất từng slide của một file .pptx ra PNG (và tuỳ chọn PDF) bằng Microsoft PowerPoint (COM).
#   powershell -ExecutionPolicy Bypass -File scripts/export_slides.ps1 -Pptx <file.pptx> -OutDir <thư mục> [-Width 1280] [-Pdf]
param([Parameter(Mandatory)][string]$Pptx, [Parameter(Mandatory)][string]$OutDir, [int]$Width = 1280, [switch]$Pdf)

$path = (Resolve-Path $Pptx).Path
New-Item -ItemType Directory -Force $OutDir | Out-Null
$out = (Resolve-Path $OutDir).Path
$app = New-Object -ComObject PowerPoint.Application
try {
    $pres = $app.Presentations.Open($path, $true, $false, $false)   # ReadOnly, Untitled=false, WithWindow=false
    $h = [int]($Width * $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth)
    $i = 0
    foreach ($s in $pres.Slides) {
        $i++
        $s.Export((Join-Path $out ("slide-{0:D2}.png" -f $i)), "PNG", $Width, $h)
    }
    if ($Pdf) { $pres.SaveAs([IO.Path]::ChangeExtension($path, ".pdf"), 32) }   # 32 = ppSaveAsPDF
    $pres.Close()
    Write-Output "OK: $i slide -> $out"
}
finally {
    $app.Quit()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
