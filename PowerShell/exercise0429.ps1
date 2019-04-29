#실습
Add-AzureRmAccount
Get-AzureRmSubscription
Set-AzureRmContext -SubscriptionId 'SubscriptionId'
$rg = New-AzureRMResourceGroup -Name '20533E0204-LabRG' -Location 'AzureRegion'
$vnet = New-AzureRmVirtualNetwork -ResourceGroupName $rg.ResourceGroupName -Name '20533E0204-vnet' -AddressPrefix '10.11.0.0/16' -Location $rg.Location
Add-AzureRmVirtualNetworkSubnetConfig -Name 'Subnet1' -VirtualNetwork $vnet -AddressPrefix '10.11.0.0/24'
Set-AzureRmVirtualNetwork -VirtualNetwork $vnet

$vnet = New-AzureRmVirtualNetwork -ResourceGroupName $rg.ResourceGroupName -Name '20533E0202-vnet' -AddressPrefix '10.1.0.0/16' -Location $rg.Location

Add-AzureRmVirtualNetworkSubnetConfig -Name 'Subnet1' -VirtualNetwork $vnet -AddressPrefix '10.1.0.0/24'
Add-AzureRmVirtualNetworkSubnetConfig -Name 'Subnet2' -VirtualNetwork $vnet -AddressPrefix '10.1.1.0/24'