param(
    [Parameter(Mandatory = $true)][string]$InputMarkdown,
    [Parameter(Mandatory = $true)][string]$OutputPdf
)

$ErrorActionPreference = 'Stop'
$work = Join-Path $env:TEMP ("forwarder-pdf-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $work | Out-Null
try {
    $base = [IO.Path]::GetFileNameWithoutExtension($OutputPdf)
    $tex = Join-Path $work "$base.tex"
    $initialPdf = Join-Path $work "$base.pdf"
    $source = Get-Content -LiteralPath $InputMarkdown -Raw
    $ascii = $source.Replace([char]0x201c, '"').Replace([char]0x201d, '"').Replace([char]0x2019, "'").Replace([char]0x2013, '-').Replace([char]0x2014, '-').Replace([char]0x2026, '...').Replace([char]0x20ac, 'EUR')
    $ascii = [regex]::Replace($ascii, '[^\u0000-\u007F]', '?')
    $escaped = $ascii.Replace('\end{verbatim}', '\end{verbatim}{}')
    $document = @"
\documentclass[10pt]{article}
\usepackage[a4paper,margin=18mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{fancyvrb}
\DefineVerbatimEnvironment{markdowntext}{Verbatim}{fontsize=\small,breaklines=true}
\begin{document}
\begin{markdowntext}
$escaped
\end{markdowntext}
\end{document}
"@
    Set-Content -LiteralPath $tex -Value $document -Encoding UTF8
    & pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$work $tex | Out-Null
    if (-not (Test-Path $initialPdf)) { throw "Initial PDF was not created." }

    $prefix = Join-Path $work 'page'
    & pdftoppm -png -r 180 $initialPdf $prefix | Out-Null
    $images = @(Get-ChildItem -LiteralPath $work -Filter 'page-*.png' | Sort-Object Name)
    if ($images.Count -eq 0) { throw "No rasterized pages were created." }

    $imageTex = Join-Path $work "$base-images.tex"
    $imageLines = foreach ($image in $images) {
        $escapedPath = $image.FullName.Replace('\', '/')
        "\includegraphics[width=\textwidth,height=\textheight,keepaspectratio]{`"$escapedPath`"}"
    }
    $imageDocument = @"
\documentclass{article}
\usepackage[a4paper,margin=0mm]{geometry}
\usepackage{graphicx}
\pagestyle{empty}
\begin{document}
$($imageLines -join "`n\newpage`n")
\end{document}
"@
    Set-Content -LiteralPath $imageTex -Value $imageDocument -Encoding UTF8
    & pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$work $imageTex | Out-Null
    $finalPdf = Join-Path $work "$base-images.pdf"
    if (-not (Test-Path $finalPdf)) { throw "Image-only PDF was not created." }
    Copy-Item -LiteralPath $finalPdf -Destination $OutputPdf -Force
}
finally {
    Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}
