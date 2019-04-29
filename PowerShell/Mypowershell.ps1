Get-Command
Get-Process
Get-Help Get-Process # PowerShell 주석
$env:PSModulePath

Install-Module -Name Az -AllowClobber

Import-Module Az.Accounts

Get-ExecutionPolicy # PowerShell 스크립트 실행 정책 보여줌
    # Restricted : 제한됨 (*.ps1 파일) : 강력하기 때문에 강한 보안 걸려있음
    # Unrestricted : 실행 (보안상 위험) : 인증서 매칭

Set-ExecutionPolicy Unrestricted # PowerShell 스크립트 실행 정책 수정
# Set-ExecutionPolicy -ExecutionPolicy가 생략된 모습

Add-AzAccount # 또는
Connect-AzAccount

Get-AzSubscription


Set-AzureRmContext -SubscriptionId #'SubscriptionId'
Select-AzSubscription -Subscription 80647935-3144-4ef2-8d55-587f415ef448 # 이 subscription에서 작업하도록 하겠다 <Subscription id>

#-----------------------------------AzureRM 모듈 설치------------------------------------------#

Install-Module -Name AzureRM -AllowClobber
Import-Module AzureRM
Connect-AzureRmAccount
