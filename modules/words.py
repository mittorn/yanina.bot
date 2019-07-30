# coding:utf-8
from module_imports import *
import random
@cmd('ильфак')
def ilfak(p,t,m):
	vk_send(p,'мудак')

@cmd('мудак')
def mudak(p,t,m):
	vk_send(p,'ильфак')

@cmd('соси', 'сосать', 'сасать', 'сосатб', 'сасатб')
def suck(p,t,m):
	vk_send(p,'нет ты')

@cmd('хуйсоси')
def guba(p,t,m):
	vk_send(p,random.choice(['губойтряси','смартфон тряси']))


