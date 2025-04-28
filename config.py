#config.py

# Dictionary
tahun_2022 = {'tahun' : '2022', 'tipe' : 'excel', 'url' : 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQPxyl1P5AOFTBbTNR2f1TH3jP69HJigz2nnixuT2Ft3E67jeQFerdFoD5heO9YSY-Zi_H7TjHrTu3x/pub?output=xlsx', 'icon' : ':tiger:', 'icon_sidebar' : ':tiger2:'}
tahun_2023 = {'tahun' : '2023', 'tipe' : 'excel', 'url' : 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ2gUwmQqoZnuheu3yON7gG9yep2apr1Hwcs9xvb4Ce1yxkIBNAHZmDoarWHOUymQ/pub?output=xlsx', 'icon' : ':rabbit:', 'icon_sidebar' : ':rabbit2:'}
#tahun_2024 = {'tahun' : '2024', 'tipe' : 'excel', 'url' : 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT85fb9TAXVvoVOWoBQ2kRJ_ETGs6DWyZ1u-ttnr8ejrvBvxC9yQvsVWRaKSRQkeSDC1SbPQJESmYqu/pub?output=xlsx', 'icon' : ':dragon_face:', 'icon_sidebar' : ':dragon:'}
tahun_2024 = {'tahun' : '2024', 'tipe' : 'excel', 'url' : '.../2024/2024all.xlsx', 'icon' : ':dragon_face:', 'icon_sidebar' : ':dragon:'}
tahun_2025 = {'tahun' : '2025', 'tipe' : 'csv', 'url' : 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSrI-S-HxETvnbQKJmbldzFj8G6cOTddrvGgtDtftsiJRd7vz2RApDPFXdx_TkU0xZz04Zp1Yvh146f/pub?output=csv', 'icon' : ' ', 'icon_sidebar' : ':snake:'}

# List standar nama kolom
mylist = ['Nama Barang', 'Serial Number', 'Qty', 'RMA Level', 'Tgl Masuk [PB06]', 'Tgl Keluar [PB07]', 'Final Status', 'Project']

# Kolom yang harus dihapus untuk data tahun 2023
columns_to_drop = ['Kategori','Expert','Tgl Tes','Tiket PB07']
