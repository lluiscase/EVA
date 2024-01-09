from vosk import Model, KaldiRecognizer                           
import pyaudio                                                    
import pyttsx3                                                    
import json                                                       
import pywhatkit                                                  
import os
from tkinter import *
from tkinter import messagebox
import datetime
import requests as rq
from random import randint
import sys
import winsound
import time

engine = pyttsx3.init()     

winsound.PlaySound('evaSong.wav', winsound.SND_ASYNC)

cidade = 'São Paulo'

class SystemInfo:
    def Init(self):
        pass
#########################################Respostas Prontas########################################################################################
def get_hello():
        Hello = ['Olá, Tudo bem?', "Oi", "hello"]
        randomizador = randint(0,2)
        answer = '{}'.format(Hello[randomizador])
        return answer
    
def get_howareyou():
        Howareyou = ['estou bem, obrigada por perguntar.', 'Bem', 'estou bem', 'me sinto bem']
        randomizador = randint(0,3)
        answer = '{}'.format(Howareyou[randomizador])
        return answer

def get_history():
        History = ("Oi, sobre a minha historia,iniciou-se por um incrivel grupo de estudantes do terceiro ano do ensino medio que decidiram me criar pois tinham que realizar um trabalho de conclusão do curso tecnico e assim com carinho e um pouco de stress, nasci para ajuda-los em seus afazeres")
        answer = '{}'.format(History)
        return answer

def get_jokes():
        Jokes = ["Sabe o que é um bis na água? Uma bisnaguinha" , 
        "Eu tomo café. A Cláudia, leite. Eu tomo gelado. O Clark, Kent." , 
       "Eu morava numa ilha e me mudei para outra. Isso não foi um trocadilho, mas uma trocadilha",
       "Por que o jacaré tirou o filho da escola? Porque ele réptil de ano!",
       "Qual é o animal que não vale mais nada? O javali!", 
       "Sabe o que o melão estava fazendo de mãos dadas com o mamão perto de Copacabana? Levando o mamão papaya.",
       "Tinha dois caminhões voando. Um deles caiu. Por que o outro continuou voando? Porque era caminhão-pipa.",
       "Sabe o que acontece com a Inglaterra quando chove? vira InglaLama",
       "Não sou palhaço para contar piada"
       ]
        randomizador = randint(0,7)
        answer = '{}'.format(Jokes[randomizador])
        return answer

def get_reciclagem():
        Reciclagem = ["Lembre-se das lixeiras seletivas e suas cores, pois são grandes aliadas do meio ambiente. Suas cores são: Azul - papel e papelão. Vermelha - plástico. Verde - vidro. Amarela - metal. Com isso, o trabalho dos catadores é facilitado e os resíduos chegam ao destino apropriado mais rápido."]
        answer = '{}'.format(Reciclagem)
        return answer
########################################Comandos logicos##########################################################################################  
def get_time():
        hour = datetime.datetime.now().strftime('%H')
        minutes = datetime.datetime.now().strftime('%M')
        answer = 'são {} horas e {} minutos'.format(hour, minutes)
        return answer

def get_date():
        DayOfMonth = datetime.datetime.now().strftime('%d')
        NumberoftheMonth = datetime.datetime.now().strftime('%m')
        answer = 'Hoje é dia {} do mês {} '.format(DayOfMonth, NumberoftheMonth)
        return answer

def clima_tempo():  
        endereco_api = "http://api.openweathermap.org/data/2.5/weather?appid=d682b15305b7f8cfda7c2c837f87dc35&q="
        url = endereco_api + cidade

        infos = rq.get(url).json()

        longitude = infos['coord']['lon']
        latitude = infos['coord']['lat']

        temp = infos['main']['temp'] - 273.15 
        pressao_atm = infos['main']['pressure'] / 1013.25 
        humidade = infos['main'] ['humidity'] 
        temp_max= infos['main']['temp_max'] - 273.15 
        temp_min= infos['main']['temp_min'] - 273.15 

        v_speed = infos['wind']['speed'] #km/h
        v_direc = infos['wind']['deg'] #recebe em graus

        nebulosidade = infos['clouds']['all']

        return [longitude, latitude,
            temp, pressao_atm, humidade,
            temp_max, temp_min, v_speed,
            v_direc, nebulosidade, id]

def temperatura():
        temp_atual = clima_tempo()[2]
        temp_max = clima_tempo()[5]
        temp_min = clima_tempo()[6]
        resposta = 'A temperatura de agora é {:.2f}º. Hoje temos uma máxima de {:.2f}º e uma minima de {:.2f}º'.format(temp_atual, temp_max, temp_min)
        return resposta

def talk(text):
  engine.say(text)
  engine.runAndWait()

def update(ind):
      frame = frames[ind]
      ind += 1
      if ind>1: 
          ind = 0
      label.configure(image=frame)
      window.after(1000, update, ind)

#Puxa as funcionalidades das bibliotecas vosk, pyaudio para o funcionamento do reconhecimento
model = Model('model')                        
rec = KaldiRecognizer(model,16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,frames_per_buffer=2048)
stream.start_stream()

while True:
#Funções que implementam o reconhecedor de voz do vosk após instanciar as funcionalidades 
    data = stream.read(2048)
    if len(data) == 0:
        break
    
    if rec.AcceptWaveform(data):
      result = rec.Result()
      result = json.loads(result)

      if result is not None:
          speech = result['text'] 
 
          print('Você disse:', speech.split())

          if speech == 'eva que horas são' or speech == 'eva me diga as horas' or speech == 'eva que oração' or speech == 'me diga as horas' or speech == 'eva me siga as horas':
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando" , "Comando de Horário")
            print(get_time())
            talk(get_time())
            window.after(3500,window.destroy)
            window.mainloop()

          elif 'toque' in speech:
            song = speech.replace('toque','')
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando do Youtube")
            print('Tocando' + song)
            talk('Tocando' + song)
            pywhatkit.playonyt(song)
            window.after(3500,window.destroy)
            window.mainloop()
        
          elif 'pesquisa' in speech:
            search = speech.replace('pesquisa', '')
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando de pesquisa")
            print('Pesquisando' + search)
            talk('Pesquisando' + search)
            pywhatkit.search(search)
            window.after(3500,window.destroy)
            window.mainloop()
            
          elif speech == 'olá eva' or speech == 'ou a eva' or speech == 'oi eva': 
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando de olá")
            print(get_hello())               
            talk(get_hello())
            window.after(3500,window.destroy)
            window.mainloop()
        
          elif speech == 'tudo bem eva' or speech == 'como você está eva' or speech =='tudo bem' or speech=='como você':
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando de 'tudo bem?'")
            print(get_howareyou())
            talk(get_howareyou())
            window.after(3500,window.destroy)
            window.mainloop()

          elif speech == 'eva como reciclar' or speech == 'eva explique sobre reciclagem' or speech == 'como reciclar' or speech == 'explique sobre reciclagem' or speech == 'clique sobre reciclagem' or speech == 'eva e clique sobre a reciclagem' or speech == 'clique sobre a reciclagem':
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando sobre reciclagem")
            print(get_reciclagem())
            talk(get_reciclagem())
            window.after(3500,window.destroy)
            window.mainloop()

          elif speech == 'eva qual a data de hoje' or speech == 'a data de hoje' or speech == '� com a data de hoje' or speech == 'eva com a data de hoje' or speech == 'da qual a data de hoje' or speech == 'qual a data de hoje' or speech== 'com a data de hoje' or speech == 'eva qual o dia de hoje'  or speech == 'o eva com a data de hoje' or speech =='eva a data de hoje' or speech == 'que dia é hoje' or speech == 'qual o dia de hoje' or speech == 'ela com a data de hoje':
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando de data")
            print(get_date())
            talk(get_date())
            window.after(3500,window.destroy)
            window.mainloop()

          elif 'eva mostre as informações da cidade' in speech or speech == 'eva mostra as informações da cidade'or speech == 'mostra as informações da cidade':
            lista_infos = clima_tempo()
            humidade = lista_infos[4]
            v_speed = lista_infos[7]
            v_direc = lista_infos[8]
            nebulosidade = lista_infos[9]
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando de informações da cidade")
            print('Mostrando informações de {}'.format(cidade))
            talk('Mostrando informações de {}'.format(cidade))
            talk('Humidade : {}'.format(humidade))
            talk('Nebulosidade : {}'.format(nebulosidade))
            talk('Velocidade do vento : {}m/s\nDireção do vento: {}'.format(v_speed, v_direc))
            window.after(3500,window.destroy)
            window.mainloop()

          elif speech == 'eva qual a temperatura' or speech == 'eva com a temperatura' or speech == 'eva cota pirata' or speech == 'pacote temperatura' or speech == 'é com a temperatura':
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando de temperatura")
            print(temperatura())
            talk(temperatura())
            window.after(3500,window.destroy)
            window.mainloop()
   
          elif speech == 'eva com uma piada' or speech == 'eva conte uma piada' :
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando de piada")
            print(get_jokes())
            talk(get_jokes())
            window.after(3500,window.destroy)
            window.mainloop()

          elif speech == 'conte sobre você' or speech == 'conte sua história' or speech == 'conte sua história eva' or speech == 'com sobre você' or speech == 'cote sobre você' or speech == 'contei sobre você' or speech == 'conto sobre você':
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando da historia da eva")
            print(get_history())
            talk(get_history())
            window.after(3500,window.destroy)
            window.mainloop()

          elif speech == 'abrir explorador de arquivos' or speech == 'abra explorador de arquivos' or speech == 'abra a história de arquivos' or speech == 'abrir arquivos' or speech == 'abrir e explorador de arquivos':
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando para abrir explorador de arquivos")
            print("abrindo explorador de arquivos")
            talk("abrindo explorador de arquivos")
            os.startfile('explorer.exe')
            window.after(3500,window.destroy)
            window.mainloop()

          elif speech == 'abrir Spotify' or speech == 'abra Spotify' or speech == 'abrir esportes' or speech == 'abra esportes':
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando para abrir spotify")
            print("abrindo spotify")
            talk("abrindo spotify")
            os.startfile('spotify.exe')
            window.after(3500,window.destroy)
            window.mainloop()            
          
          elif speech == 'abrir google' or speech == 'abra google':
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando para abrir o google")
            print("abrindo google")
            talk("abrindo google")
            os.startfile('chrome.exe')
            window.after(3500,window.destroy)
            window.mainloop()

          elif speech == 'abrir bloco de notas' or speech == 'abra bloco de notas':
            window = Tk()
            frames = [PhotoImage(file='interface.gif',format = 'gif -index %i' %(i)) for i in range(2)]
            window.geometry("840x480")
            label = Label(window)
            label.pack(ipadx=150,ipady=150)
            window.after(0, update, 0)
            messagebox.showinfo("Executando", "Comando para abrir o bloco de notas")
            print("abrindo bloco de notas")
            talk("abrindo bloco de notas")
            os.startfile('notepad.exe')
            window.after(3500,window.destroy)
            window.mainloop()
          
          elif speech == 'eva desligar' or speech == 'desligar' or speech == 'eva de gaia' or speech == 'eva deve ligar' or speech == 'erva desligar ' or speech == 'eva desliga' or speech == 'desligar eva' or speech == 'desliga eva':
            winsound.PlaySound('exit to eva.wav', winsound.SND_ASYNC)
            time.sleep(1)
            sys.exit()