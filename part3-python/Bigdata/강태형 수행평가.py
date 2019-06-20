moneyForChange = int(input('바꿀 돈 -->'))
ohBaek = 0
baek = 0
ohsip = 0
sip = 0
leftover = 0

if moneyForChange > 500:
    ohBaek = moneyForChange // 500
    moneyForChange -= 500 * ohBaek

if moneyForChange > 100:
    baek = moneyForChange // 100
    moneyForChange -= 100 * baek

if moneyForChange > 50:
    ohsip = moneyForChange // 50
    moneyForChange -= 50 * ohsip

if moneyForChange > 10:
    sip = moneyForChange // 10
    moneyForChange -= 10 * sip

leftover = moneyForChange

print("500원: ",ohBaek,"100원: ",baek,"50원: ",ohsip,"10원: ",sip,"나머지: ",leftover)
