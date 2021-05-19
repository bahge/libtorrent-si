# Implementação baseada na biblioteca libtorrent

import libtorrent as lt
import time
import datetime
import sys
import os

ses = lt.session() 
ses.listen_on(6881, 6891) 

print('Implementação para a disciplina de Sistemas Distribuidos')
print('Aluno: Leandro Costa Garcia')
print('RGA: 201811316013')
print('')
file_name = input("Digite o nome do arquivo (sem .torrent) > ")
dest_folder = input("Digite o caminho da pasta de destino > ")

info = lt.torrent_info(file_name+'.torrent')

if os.path.isdir(dest_folder):
    print("Diretório de destino > " + dest_folder)
else:
    dest_folder = './'
    print("O arquivo será enviado para a mesma pasta do arquivo .torrent")

handle = ses.add_torrent({'ti': info, 'save_path': dest_folder})

s = handle.status()

begin = time.time()
print('Hora:')
print(datetime.datetime.now())

print('Baixando: ', s.name)
while (not s.is_seeding):
    s = handle.status()

    print('\r%.2f%% completo (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
        s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
        s.num_peers, s.state), end=' ')

    alerts = ses.pop_alerts()
    for a in alerts:
        if a.category() & lt.alert.category_t.error_notification:
            print(a)

    sys.stdout.flush()

    time.sleep(1)

print(handle.status().name, "FINALIZADO")
end = time.time()

print("Tempo decorrido: ",int((end-begin)//60),"min :", int((end-begin)%60), "sec")
print(datetime.datetime.now())
print('')
print('Aplicação para fins educacionais')
