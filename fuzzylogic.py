import csv
import pandas as pd
import numpy as np

data = pd.read_csv("influencers.csv")

def validasiRentan(a, b, x):
    return max(min(x, b), a)

#STEP 1 = Fuzzification dan STEP 2 = Inference
def raterendah(nilai):
	if nilai <= 2:
		return 1
	elif nilai > 2 and nilai < 3 :
		return validasiRentan(0.0, 1.0, (nilai - 3) / (3 - 2))
	else :
		return 0

def ratecukuptinggi(nilai):
	if (nilai <= 3 or nilai >= 6):	
		return 0
	elif (3 < nilai < 4):
		return validasiRentan(0.0, 1.0,(nilai - 3) / (4 - 3))
	elif (4 <= nilai <= 5):	
		return 1
	else :
		return validasiRentan(0.0, 1.0,-(nilai - 6) / (6 - 5))

def ratetinggi(nilai):
	if nilai <= 5 or nilai >= 9:
		return 0
	elif 5 < nilai < 6:
		return validasiRentan(0.0, 1.0,(nilai - 5) / (6 - 5))
	elif 6 <= nilai <= 8:
		return 1
	else:
		return validasiRentan(0.0, 1.0,-(nilai - 8) / (9 - 8))
			
def ratesangattinggi(nilai):
	if nilai <= 8:
		return 0
	elif 8 < nilai < 9:
		return validasiRentan(0.0, 1.0,(nilai - 8) / (9 - 8))
	else:
		return 1
			
#grafik followers

def followersedikit(nilai):
	if nilai <= 20000:
		return 1
	elif 20000 < nilai < 30000:
		return validasiRentan(0.0, 1.0, -(nilai - 30000) / (30000 - 20000))
	else:
		return 0

def followercukupbanyak(nilai):
	if nilai <= 30000 or nilai >= 60000:
		return 0
	elif 30000 < nilai < 40000:
		return validasiRentan(0.0, 1.0,(nilai - 30000) / (40000 - 30000))
	elif 40000 <= nilai <= 50000:
		return 1
	else:
		return validasiRentan(0.0, 1.0, -(nilai - 60000) / (60000 - 50000))

def followerbanyak(nilai):
	if nilai <= 50000 or nilai >= 90000:
		return 0
	elif 50000 < nilai < 60000:
		return validasiRentan(0.0, 1.0,(nilai - 50000) / (60000 - 50000))
	elif 60000 <= nilai <= 80000:
		return 1
	else:
		return validasiRentan(0.0, 1.0, -(nilai - 80000) / (90000 - 80000))
		
def followersangatbanyak(nilai):
	if nilai <= 80000:
		return 0
	elif 80000 < nilai < 90000:
		return validasiRentan(0.0, 1.0,(nilai - 80000) / (90000 - 80000))
	else :
		return 1  
		
def layakRendah(nilai):
	if nilai < 45:
		return 0
	elif nilai >= 45 and nilai < 80:        #45 <= x <= 80
		return validasiRentan(.0, 1.0, (nilai-45)/(80-45))
	elif nilai >= 80:
		return 0

def layakTinggi(nilai):
	if nilai < 45:
		return 0
	elif nilai >= 45 and nilai < 80:        #45 <= x <= 80
		return validasiRentan(.0, 1.0, (nilai-45)/(80-45))
	elif nilai >= 80:
		return 1
		
#STEP 3 = Conjunction and Disjunction
def Kelayakan(raterendah, ratecukuptinggi, ratetinggi, ratesangattinggi, followersedikit, followercukupbanyak, followerbanyak, followersangatbanyak):
	layak = []
	layak.append(min(raterendah,followersedikit))
	layak.append(min(raterendah,followercukupbanyak))
	layak.append(min(raterendah,followerbanyak))
	layak.append(min(raterendah,followersangatbanyak))
	layak.append(min(ratecukuptinggi,followersedikit))
	layak.append(min(ratecukuptinggi,followercukupbanyak))
	layak.append(min(ratecukuptinggi,followerbanyak))
	layak.append(min(ratecukuptinggi,followersangatbanyak))
	layak.append(min(ratetinggi,followersedikit))
	layak.append(min(ratetinggi,followercukupbanyak))
	layak.append(min(ratetinggi,followerbanyak))
	layak.append(min(ratetinggi,followersangatbanyak))
	layak.append(min(ratesangattinggi,followersedikit))
	layak.append(min(ratesangattinggi,followercukupbanyak))
	layak.append(min(ratesangattinggi,followerbanyak))
	layak.append(min(ratesangattinggi,followersangatbanyak))
	return max(layak)
	
#STEP 4 = Defuzzification
def defuzzification(nano, mikro, medium):
	x = 50
	standarRendah = []
	standarTinggi = []
	counter = 0
	m = 0
	while x < medium:
		standarRendah.append(validasiRentan(0.0, nano, layakRendah(x)))
		m = m + x*validasiRentan(0.0, nano, layakRendah(x))
		counter = counter + 1
		x = x + 10000    #jarak antar titik pada grafik
	for i in range(0, counter):
		standarTinggi.append(validasiRentan(0.0, medium, layakTinggi(x)))
		m = m + x*validasiRentan(0.0, medium, layakTinggi(x))
		counter = counter + 1
		x = x + 1    #jarak antar titik pada grafik
	m = m / (np.sum(standarRendah)+np.sum(standarTinggi))
	return m

def classification(x):
	if x < 50 :
		return 'Tidak'
	else:
		return 'Ya'

		
def validation(list1, list2):
	counter = 0
	for i in range(0, len(list1)):
		if list1[i] == list2[i]:
			counter = counter + 1
	return counter*100/ len(list1)
	
raRendah = []
raCukupTinggi = []
raTinggi = []
raSangatTinggi = []
follSedikit = []
follCukupBanyak = []
follBanyak = []
follSangatBanyak = []
layRendah = []
layTinggi = []
deFuzzy = []
klasifikasi = []
hasilFuzzy = {}
i = 1
for i in range(len(data)):
	raRendah.append(raterendah(data['Rate Engangement'][i]))
	raCukupTinggi.append(ratecukuptinggi(data['Rate Engangement'][i]))
	raTinggi.append(ratetinggi(data['Rate Engangement'][i]))
	raSangatTinggi.append(ratesangattinggi(data['Rate Engangement'][i]))
	follSedikit.append(followersedikit(data['Jumlah Followers'][i]))
	follCukupBanyak.append(followercukupbanyak(data['Jumlah Followers'][i]))
	follBanyak.append(followerbanyak(data['Jumlah Followers'][i]))
	follSangatBanyak.append(followersangatbanyak(data['Jumlah Followers'][i]))
	
	layTinggi.append(Kelayakan(raRendah[i], raCukupTinggi[i], raTinggi[i], raSangatTinggi[i], follSedikit[i], follCukupBanyak[i], follBanyak[i], follSangatBanyak[i]))
	layRendah.append(min(raRendah[i],follSedikit[i]))
	
	deFuzzy.append(defuzzification(layRendah[i], layTinggi[i], 60))
	klasifikasi.append(classification(deFuzzy[i]))

print("===== Hasil Seleksi ===== \n")
print("=> Rate Engangement Rendah : ")
print(raRendah, "\n")
print("=> Rate Engangement Cukup Tinggi : ")
print(raCukupTinggi, "\n")
print("=> Rate Engangement Tingi :")
print(raTinggi, "\n")
print("=> Rate Engangement Sangat Tinggi : ")
print(raSangatTinggi, "\n")
print("=> Jumlah Follower Sedikit : ")
print(follSedikit, "\n")
print("=> Jumlah Follower Cukup Banyak : ")
print(follCukupBanyak, "\n")
print("=> Jumlah Follower Banyak : ")
print(follBanyak, "\n")
print("=> Nilai Follower Sangat Banyak :")
print(follSangatBanyak, "\n")
print("=> Hasil Defuzzifikasi :")
print(deFuzzy, "\n")

print("=> Nilai Kelayakan Tinggi :")
print(layTinggi, "\n")
print("=> Urutan Kelayakan dari Terkecil ke Terbesar :  ")
x = layTinggi.sort(reverse = True)
print(layTinggi, "\n")
print("Nilai Kelayakan 20 Terbaik")
a = (layTinggi[:20])
print(a, "\n")

n = 0
for i in range (len(layTinggi)) :
		if (layTinggi[i] == layTinggi[i]) :
			o = ("Ya")
		else :
			p = ("Tidak")
			
hasilFuzzy = {'ID':data['ID'], 'Rate Engangement' :data['Rate Engangement'], 'Jumlah Followers': data['Jumlah Followers'], 'Diterima/Tidak' : klasifikasi }
new_data = pd.DataFrame(hasilFuzzy)
new_data.to_csv('chosen.csv', index=False)