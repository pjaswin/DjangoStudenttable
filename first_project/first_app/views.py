from ast import Not
from multiprocessing import context
from operator import contains
from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import Degree, Student
from django.http import HttpResponseRedirect
from .forms import DegreeForm ,StudentForm,Searchform
import json
from django.db.models import Q


def index(request) :
  degree_values = Degree.objects.all()

  students_details=Student.objects.all()  
  my_dict = {
        'degree_rows' : degree_values,
        'students_rows':students_details,
    }
  return render(request,'index.html',context=my_dict)
def get_degree(request):
  if request.method == 'POST':                  # if this is a POST request we need to process the form data
    form = DegreeForm(request.POST, request.FILES)   # create a form instance and populate it with data from the request:
    if form.is_valid():                         # check whether it's valid:
      title = form.cleaned_data['title']        # process the data in form.cleaned_data as required
      branch = form.cleaned_data['branch']
      print(title, branch)

      d = Degree(title=title, branch=branch)    # write to the database
      d.save()

      # Retrieve the json file and process here
      f = request.FILES['file']          # open the json files - get file handle
      data = json.load(f)
      for deg in data['degree']:         # iterate through the degree list
        t = deg['title']                 # get the title of each item in the list
        b = deg['branch']                # get the branch of each item in the list
        dl = Degree(title=t, branch=b)   # Create a Degree model instance
        dl.save()                        # save

      return HttpResponseRedirect('/degree/')   # redirect to a new URL:
  else:                                   # if a GET (or any other method) we'll create a blank form
    form = DegreeForm()
    return render(request, 'degree.html', {'form': form })
def get_student(request):
  if request.method == 'POST':                  # if this is a POST request we need to process the form data
    form = StudentForm(request.POST, request.FILES)   # create a form instance and populate it with data from the request:
    if form.is_valid():                         # check whether it's valid:
      degree = form.cleaned_data['degree']        # process the data in form.cleaned_data as required
      roll_number = form.cleaned_data['roll_number']
      name = form.cleaned_data['name']
      year = form.cleaned_data['year']
      dob = form.cleaned_data['dob']
      file = form.cleaned_data['file']
      print(degree, roll_number,name,year,dob,file)

      d = Student(degree=degree,roll_number=roll_number,name=name,year=year,dob=dob)    # write to the database
      d.save()

     
      f = request.FILES['file']          # open the json files - get file handle
      data = json.load(f)
      for deg in data['student']:         # iterate through the degree list
        de = deg['degree']                 # get the title of each item in the list
        r = deg['roll_number']
        na=deg['name']
        ye=deg['year']
        do=deg['dob']
        degg=Degree.objects.get(branch=de[0]["branch"])
                     # get the branch of each item in the list
        dl = Student(degree=degg,roll_number=r,name=na,year=ye,dob=do)     # Create a Degree model instance
        dl.save()                        # save

      return HttpResponseRedirect('/student/')   # redirect to a new URL:
  else:                                   # if a GET (or any other method) we'll create a blank form
    form = StudentForm()
  return render(request, 'student.html', {'student_form': form })


def get_search(request):
  #DuplicateStudent.objects.all().delete()
  form_class=Searchform
  form=form_class(request.POST or None)
  template_name = 'search.html'
  if request.method == 'POST':                  # if this is a POST request we need to process the form data
    form = Searchform(request.POST)
  if form.is_valid():
    query=form.cleaned_data["keywords"]
    date1=form.cleaned_data["date1"]
    date2=form.cleaned_data["date2"]
    sortv=form.cleaned_data["sort"]
    print(date1,date2)
    
    if date1:
        results = Student.objects.filter(Q(name__icontains=query) & Q(dob__range=(date1, date2)))
    else :
         # query example
         results = Student.objects.filter(Q(name__icontains=query))
    # if date1:
    #   result1=Student.objects.filter(dob__range=[date1,date2])
    # for i in results:
    #   dll = DuplicateStudent(degree=i.degree,roll_number=i.roll_number,name=i.name,year=i.year,dob=i.dob)
    #   dll.save()
    # search_details=DuplicateStudent.objects.all() 
    if sortv ==True:
      results=results.order_by('name')


    return render( request, template_name, {'date_form':results,'normal_form': form})
  else:
    return render(request, 'search.html', {'normal_form': form})

# def MyView(request):
#  mylist=request.POST.getlist('sort')
#  if 'sorting' in mylist:
#    pass

    
    

