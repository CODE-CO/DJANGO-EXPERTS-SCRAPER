from django.shortcuts import render
from django.http import JsonResponse
import os

def index(request):
    return render(request, 'files/index.html')

def get_file_content(request):
    filter_option = request.POST.get('filter', 'all')
    file_mapping = {
        'all': 'all.txt',
        'men': 'men.txt',
        'women': 'women.txt'
    }
    file_name = file_mapping.get(filter_option, 'all.txt')
    file_path = os.path.join('main', 'static', 'files', 'txt', file_name)
    
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return JsonResponse({'content': file_content})
    except FileNotFoundError:
        return JsonResponse({'error': 'File not found.'})