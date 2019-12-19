
#import-module .\sendMail.ps1
#$securePwd = Read-Host "Enter password" -AsSecureString
firefox sapo.pt
$main = join-path $PSScriptRoot main.py
python $main