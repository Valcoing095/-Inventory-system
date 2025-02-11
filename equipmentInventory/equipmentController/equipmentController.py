from django.shortcuts import render
from django.http import JsonResponse

from django.http import HttpResponse
from .models import Area, Equipo, Empresa,Sede,EmpresaSede, Usuario


def registerEquipmentInventory(Request):
    # Get the equipment id from the request