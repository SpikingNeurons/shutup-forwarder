param([Parameter(Mandatory=$true)][string]$InputMarkdown,[Parameter(Mandatory=$true)][string]$OutputPdf)
$ErrorActionPreference='Stop'
$work=Join-Path $env:TEMP ('forwarder-pdf-'+[guid]::NewGuid().ToString('N')); New-Item -ItemType Directory -Path $work | Out-Null
try {
  $base=[IO.Path]::GetFileNameWithoutExtension($OutputPdf); $tex=Join-Path $work "$base.tex"; $initial=Join-Path $work "$base.pdf"
  $ascii=Get-Content -LiteralPath $InputMarkdown -Raw
  $ascii=$ascii.Replace([char]0x201c,'"').Replace([char]0x201d,'"').Replace([char]0x2019,"'").Replace([char]0x2013,'-').Replace([char]0x2014,'-').Replace([char]0x2026,'.')
  $ascii=[regex]::Replace($ascii,[string][char]0x20ac,'EUR'); $ascii=[regex]::Replace($ascii,'[^\u0000-\u007F]','?'); $ascii=$ascii.Replace('\end{verbatim}','\end{verbatim}{}')
  $doc="\documentclass[10pt]{article}`n\usepackage[a4paper,margin=18mm]{geometry}`n\usepackage{fvextra}`n\DefineVerbatimEnvironment{markdowntext}{Verbatim}{fontsize=\small,breaklines=true,breakanywhere=true}`n\begin{document}`n\begin{markdowntext}`n$ascii`n\end{markdowntext}`n\end{document}`n"
  Set-Content -LiteralPath $tex -Value $doc -Encoding UTF8; & pdflatex -interaction=nonstopmode -halt-on-error -output-directory $work $tex | Out-Null
  if(!(Test-Path $initial)){throw 'Initial PDF was not created.'}; $prefix=Join-Path $work 'page'; & pdftoppm -png -r 120 $initial $prefix | Out-Null
  $images=@(Get-ChildItem -LiteralPath $work -Filter 'page-*.png' | Sort-Object Name); if($images.Count -eq 0){throw 'No rasterized pages were created.'}
  $imageTex=Join-Path $work "$base-images.tex"; $lines=foreach($image in $images){$p=$image.FullName.Replace('\','/'); "\includegraphics[width=\textwidth,height=\textheight,keepaspectratio]{`"$p`"}"}
  $imageDoc="\documentclass{article}`n\usepackage[a4paper,margin=0mm]{geometry}`n\usepackage{graphicx}`n\pagestyle{empty}`n\begin{document}`n$($lines -join "`n\newpage`n")`n\end{document}`n"
  Set-Content -LiteralPath $imageTex -Value $imageDoc -Encoding UTF8; & pdflatex -interaction=nonstopmode -halt-on-error -output-directory $work $imageTex | Out-Null
  $final=Join-Path $work "$base-images.pdf"; if(!(Test-Path $final)){throw 'Image-only PDF was not created.'}; Copy-Item $final $OutputPdf -Force
} finally {Remove-Item $work -Recurse -Force -ErrorAction SilentlyContinue}
