# Set the path to the directory containing your files
$sourceDirectory = "E:\Reviewed\ts"

# Get all files in the source directory
$files = Get-ChildItem -Path $sourceDirectory -File

# Loop through each file
foreach ($file in $files) {
    # Create a directory with the same name as the file (without extension)
    $folderPath = Join-Path -Path $sourceDirectory -ChildPath $file.BaseName

    # Check if the folder already exists, if not, create it
    if (-not (Test-Path -Path $folderPath -PathType Container)) {
        New-Item -Path $folderPath -ItemType Directory
    }

    # Move the file into its respective folder
    Move-Item -Path $file.FullName -Destination $folderPath
}

Write-Host "Organization completed."
