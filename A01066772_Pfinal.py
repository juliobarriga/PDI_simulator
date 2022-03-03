import tkinter as tk
from tkinter import filedialog

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.patches as mpatches

import numpy as np
import math
import time

#Proyecto de Control Computarizado
#Julio David Barriga Tehandón
#A01066772


window = tk.Tk()
window.wm_title("Simulador de dinámicas de procesos")

frame = tk.Frame(master=window, width=1350, height=770)
frame.pack()

titulo = tk.Label(text="Simulador de dinámicas de procesos", font="Arial 12 bold")
titulo.place(x=320, y=0)

image = tk.PhotoImage(file="Control.png")
imagen_lbl = tk.Label(image=image)
imagen_lbl.place(x=0, y= 550)

mk=[]
c_k=[]
pk=[]
rk=[]
ek=[]
tiempo=[]
contador=0
start=0
k=0 #el paso en el que va
n=0 #la posicion del txt
p=0

fig=plt.figure(figsize=(8,3.5))
ax=fig.add_axes([0.1,0.2,0.8,0.75],polar=False)
ax.set(ylim=(0, 100))
ax.set_xlabel('Tiempo')
canvas=FigureCanvasTkAgg(fig,master=window)
canvas.get_tk_widget().place(x=525, y=30)


fig2=plt.figure(figsize=(8,3.5))
bx=fig2.add_axes([0.1,0.2,0.8,0.75],polar=False)
bx.set(ylim=(0, 100))
bx.set_xlabel('Tiempo')
canvas2=FigureCanvasTkAgg(fig2,master=window)
canvas2.get_tk_widget().place(x=525, y=415)


#canvas.show()

def inicio():
    global start
    global contador
    global n
    global ref
    global p
    global grafica
    ax.clear()
    bx.clear()
    start=1
    modo=var.get()
    print('incio')
    if start == 1:
        if modo == 1:
            parametros_manual()
            if not archivo.get():
                if not m_k.get():
                    mk.append(mk[-1])
                else:
                    mk.append(step)
            else:
                if len(mk)>=negativos:#cuando se inicia con txt
                    print(filename)
                    with open(filename) as f:
                       lis = [float(line.split()[0]) for line in f]
                    if n<len(lis):
                        mk.append(lis[n])
                        n=n+1
                    else:
                        if not m_k.get():
                            mk.append(lis[n-1])
                        else:
                            mk.append(step)
                else:
                    print('error')
            pk.append(p)
            y = a1*c_k[contador-1+negativos] + b1*mk[contador-1-N+negativos] + b2*mk[contador-2-N+negativos]+pk[contador+negativos]
            #print(y)
            c_k.append(y)
            rk.append(y)
            z = rk[contador]-c_k[contador]
            ek.append(z)

        elif modo == 2:
            parametros_automatico()
            if not r_k.get():
                rk.append(rk[-1])
            else:
                rk.append(ref)
            pk.append(p)
            print(c_k[contador-1+negativos])
            print(c_k[contador-2+negativos])
            print(c_k[contador-1+negativos])
            y = a1*c_k[contador-1+negativos] + b1*mk[contador-1-N+negativos] + b2*mk[contador-2-N+negativos]+pk[contador+negativos]
            print(y)
            c_k.append(y)
            z = rk[-1]-c_k[-1]
            print(z)
            ek.append(z)
            print(mk[contador-1+negativos])
            print(ek[contador+negativos])
            print(ek[contador-1+negativos])
            print(ek[contador-2+negativos])
            x = mk[contador-1+negativos]+B0*ek[contador+negativos]+B1*ek[contador-1+negativos]+B2*ek[contador-2+negativos]
            mk.append(x)


            #print('Modo Automatico')
        else:
            print('Seleccione Modo')
        #print('ck')
        #print(len(c_k))
        #print(c_k[-1])
        #print('mk')
        #print(len(mk))
        #print(mk[-1])
        #print('pk')
        #print(len(pk))
        #print(pk[-1])
        tiempo.append(contador)
        #print('tiempo')
        #print(len(tiempo))
        #print(tiempo[-1])
        #print('rk')
        #print(len(rk))
        #print(rk[-1])
        #print('ek')
        #print(len(ek))
        #print(ek[-1])
        paramMk["text"] = f"{round(mk[-1], 4)}"
        paramEk["text"] = f"{round(ek[-1], 4)}"
        ax.plot(tiempo,c_k,linestyle="-", marker='None', color='b')
        ax.plot(tiempo,rk,linestyle="-", marker='None', color='g')
        c_k_patch = mpatches.Patch(color='b', label='c(k)')
        rk_patch = mpatches.Patch(color='g', label='r(k)')
        ax.legend(handles=[c_k_patch, rk_patch])
        ax.set(ylim=(0, 100))
        canvas.draw()
        bx.plot(tiempo,mk,linestyle="-", marker='None', color='m')
        bx.plot(tiempo,pk,linestyle="-", marker='None', color='r')
        mk_patch = mpatches.Patch(color='m', label='m(k)')
        pk_patch = mpatches.Patch(color='r', label='p(k)')
        bx.legend(handles=[mk_patch, pk_patch])
        bx.set(ylim=(0, 100))
        canvas2.draw()
        contador=contador + 1
        p=0
        window.after(1000,inicio)

def stop():
    start=0;

def perturbacion():
    global p
    p=float(p_k.get())
    print('perturbacion')

def referencia():
    global ref
    ref=float(r_k.get())
    print('referencia')

def escalon():
    global step
    step = float(m_k.get())
    print('escalon rojo')

def parametros_manual():
    global a1
    global b1
    global b2
    global N
    global negativos
    #print('parametros manual')
    theta_ = float(theta_cte.get())
    T = float(T_cte.get())
    tau = float(tau_cte.get())
    kparam = float(k_cte.get())

    N = math.trunc(theta_/T)
    theta = theta_-(N*T)
    m = 1 - (theta/T)

    a1 = math.exp(-(T/tau))
    b1 = kparam*(1-math.exp(-(m*T/tau)))
    b2 = kparam*(math.exp(-(m*T/tau))-math.exp(-(T/tau)))

    paramN["text"] = f"{round(N, 4)}"
    paramtheta["text"] = f"{round(theta, 4)}"
    paramm["text"] = f"{round(m, 4)}"

    parama1["text"] = f"{round(a1, 4)}"
    paramb1["text"] = f"{round(b1, 4)}"
    paramb2["text"] = f"{round(b2, 4)}"

    negativos = 2 + N
    while len(mk)==0:
        neg = 0
        while neg<negativos:
            mk.append(0)
            c_k.append(0)
            tiempo.append(0)
            pk.append(0)
            rk.append(0)
            ek.append(0)
            neg = neg + 1
    #print(mk)
    #print(c_k)
    #print(contador)

def parametros_automatico():
    global a1
    global b1
    global b2
    global B0
    global B1
    global B2
    global N
    global negativos
    #print('parametros automatico')
    theta_ = float(theta_cte.get())
    T = float(T_cte.get())
    tau = float(tau_cte.get())
    kparam = float(k_cte.get())
    kc = float(kc_cte.get())
    taui = float(taui_cte.get())
    taud = float(taud_cte.get())

    N = math.trunc(theta_/T)
    theta = theta_-(N*T)
    m = 1 - (theta/T)

    a1 = math.exp(-(T/tau))
    b1 = kparam*(1-math.exp(-(m*T/tau)))
    b2 = kparam   *(math.exp(-(m*T/tau))-math.exp(-(T/tau)))

    B0 = kc*(1+(T/taui)+(taud/T))
    B1 = kc*(-1-(2*taud/T))
    B2 = kc*(taud/T)

    paramN["text"] = f"{round(N, 4)}"
    paramtheta["text"] = f"{round(theta, 4)}"
    paramm["text"] = f"{round(m, 4)}"

    parama1["text"] = f"{round(a1, 4)}"
    paramb1["text"] = f"{round(b1, 4)}"
    paramb2["text"] = f"{round(b2, 4)}"

    paramB0["text"] = f"{round(B0, 4)}"
    paramB1["text"] = f"{round(B1, 4)}"
    paramB2["text"] = f"{round(B2, 4)}"

    negativos = 2 + N
    while len(mk)==0:
        neg = 0
        while neg<negativos:
            mk.append(0)
            c_k.append(0)
            tiempo.append(0)
            pk.append(0)
            rk.append(0)
            neg = neg + 1





#############################################################################

subtitulo_1 = tk.Label(text="Entradas por el usuario", font="Arial 10 bold")
subtitulo_1.place(x=0, y=20)

k_lbl = tk.Label(text="k", font="Arial 10")
k_lbl.place(x=0, y=40)
k_cte = tk.Entry(width=4)
k_cte.place(x=25, y=40)

tau_lbl = tk.Label(text=u"\u03C4", font="Arial 10")
tau_lbl.place(x=100, y=40)
tau_cte = tk.Entry(width=4)
tau_cte.place(x=125, y=40)

theta_lbl = tk.Label(text=u"\u0398\uFF07", font="Arial 10")
theta_lbl.place(x=0, y=80)
theta_cte = tk.Entry(width=4)
theta_cte.place(x=25, y=80)

T_lbl = tk.Label(text="T", font="Arial 10")
T_lbl.place(x=100, y=80)
T_cte = tk.Entry(width=4)
T_cte.place(x=125, y=80)

kc_lbl = tk.Label(text=u"Kc", font="Arial 10")
kc_lbl.place(x=200, y=40)
kc_cte = tk.Entry(width=4)
kc_cte.place(x=225, y=40)

taui_lbl = tk.Label(text=u"\u03C4i", font="Arial 10")
taui_lbl.place(x=300, y=40)
taui_cte = tk.Entry(width=4)
taui_cte.place(x=325, y=40)

taud_lbl = tk.Label(text=u"\u03C4d", font="Arial 10")
taud_lbl.place(x=300, y=80)
taud_cte = tk.Entry(width=4)
taud_cte.place(x=325, y=80)

#############################################################################

subtitulo_2 = tk.Label(text="Entrada de archivo", font="Arial 10 bold")
subtitulo_2.place(x=0, y=120)

archivo = tk.Entry(width=12)
archivo.place(x=0, y=150)

def browsefunc():
    global filename
    filename =filedialog.askopenfilename(filetypes=(("txt files","*.txt"),("All files","*.*")))
    archivo.insert(tk.END, filename) # add this


b_txt = tk.Button(window,text="Browse",command=browsefunc)
b_txt.place(x=100, y=146)

subtitulo_5 = tk.Label(text="Entrada tipo escalón", font="Arial 10 bold")
subtitulo_5.place(x=200, y=120)

mk_lbl = tk.Label(text=u"\uFF4D\uFF08\uFF4B\uFF09", font="Arial 10")
mk_lbl.place(x=200, y=150)

m_k = tk.Entry(width=6, bg="white")
m_k.place(x=260, y=150)

mk_b = tk.Button(text="Enviar", command=escalon)
mk_b.place(x=315, y=146)

#############################################################################

subtitulo_3 = tk.Label(text="Parámetros", font="Arial 10 bold")
subtitulo_3.place(x=0, y=180)

param_a1 = tk.Label(text="a1", font="Arial 10")
param_a1.place(x=0, y=200)
parama1 = tk.Label(master=window, width=8, bg="white")
parama1.place(x=25, y=200)

param_b1 = tk.Label(text="b1", font="Arial 10")
param_b1.place(x=0, y=240)
paramb1 = tk.Label(master=window, width=8, bg="white")
paramb1.place(x=25, y=240)

param_b2 = tk.Label(text="b2", font="Arial 10")
param_b2.place(x=0, y=280)
paramb2 = tk.Label(master=window, width=8, bg="white")
paramb2.place(x=25, y=280)

param_N = tk.Label(text=u"\uFF2E", font="Arial 10")
param_N.place(x=100, y=200)
paramN = tk.Label(master=window, width=8, bg="white")
paramN.place(x=125, y=200)

param_theta = tk.Label(text=u"\u0398", font="Arial 10")
param_theta.place(x=100, y=240)
paramtheta = tk.Label(master=window, width=8, bg="white")
paramtheta.place(x=125, y=240)

param_m = tk.Label(text=u"\uFF4D", font="Arial 10")
param_m.place(x=100, y=280)
paramm = tk.Label(master=window, width=8, bg="white")
paramm.place(x=125, y=280)

param_B0 = tk.Label(text="B0", font="Arial 10")
param_B0.place(x=200, y=200)
paramB0 = tk.Label(master=window, width=8, bg="white")
paramB0.place(x=225, y=200)

param_B1 = tk.Label(text="B1", font="Arial 10")
param_B1.place(x=200, y=240)
paramB1 = tk.Label(master=window, width=8, bg="white")
paramB1.place(x=225, y=240)

param_B2 = tk.Label(text="B2", font="Arial 10")
param_B2.place(x=200, y=280)
paramB2 = tk.Label(master=window, width=8, bg="white")
paramB2.place(x=225, y=280)

param_Mk = tk.Label(text=u"\uFF4D\uFF08\uFF4B\uFF09", font="Arial 10")
param_Mk.place(x=300, y=200)
paramMk = tk.Label(master=window, width=8, bg="white")
paramMk.place(x=360, y=200)

param_Ek = tk.Label(text=u"\u0065\uFF08\uFF4B\uFF09", font="Arial 10")
param_Ek.place(x=300, y=240)
paramEk = tk.Label(master=window, width=8, bg="white")
paramEk.place(x=360, y=240)

#############################################################################

subtitulo_4 = tk.Label(text="Perturbación", font="Arial 10 bold")
subtitulo_4.place(x=0, y=320)

pk_lbl = tk.Label(text=u"\uFF30\uFF08\uFF4B\uFF09", font="Arial 10")
pk_lbl.place(x=0, y=340)

p_k=tk.Entry(width=4)
p_k.place(x=60, y=340)

p_send=tk.Button(window,text="Enviar", command=perturbacion)
p_send.place(x=110, y=336)

#############################################################################

subtitulo_6 = tk.Label(text="Referencia", font="Arial 10 bold")
subtitulo_6.place(x=0, y=380)

rk_lbl = tk.Label(text=u"\u0072\uFF08\uFF4B\uFF09", font="Arial 10")
rk_lbl.place(x=0, y=420)

r_k=tk.Entry(width=4)
r_k.place(x=60, y=420)

r_send=tk.Button(window,text="Enviar", command=referencia)
r_send.place(x=110, y=416)
#############################################################################

#fig1 = Figure(figsize=(5, 2), dpi=100)
#t1 = np.arange(0, 3, .01)
#fig1.add_subplot(111).plot(tiempo, c_k)

#plot1 = FigureCanvasTkAgg(fig1, master=window)  # A tk.DrawingArea.
#plot1.draw()

#fig2 = Figure(figsize=(5, 2), dpi=100)
#t2 = np.arange(0, 3, .01)
#fig2.add_subplot(111).plot(tiempo, mk)

#plot2 = FigureCanvasTkAgg(fig2, master=window)  # A tk.DrawingArea.
#plot2.draw()

#plot1.get_tk_widget().place(x=450, y=260)
#plot2.get_tk_widget().place(x=450, y=470)

#############################################################################

var = tk.IntVar()

b_manual = tk.Radiobutton(text="Manual", variable=var, value=1)
b_manual.place(x=0, y=470)

b_auto = tk.Radiobutton(text="Automatico", variable=var, value=2)
b_auto.place(x=100, y=470)

#####################################################################

b_inicio = tk.Button(master=window, text="Inicio", command=inicio)
b_inicio.place(x=0, y=510)

window.mainloop()
