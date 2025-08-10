from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import collageserializer,studentserializer,companyserializer,employeeserializer
from .models import collage,student,company,employee
from django.views import View
from django.views.generic import TemplateView,RedirectView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.views.generic.list import BaseListView
from datetime import datetime
from django.urls import reverse_lazy
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.paginator import EmptyPage, PageNotAnInteger
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly,AllowAny,IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly,DjangoModelPermissions
from .custom_permission import cusper
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .paginatior import mycursor


def homepage(request):
    return render(request,'home.html')

class onlyone(View):
    def post(self,request):
        return HttpResponse('supported only post request')

class doubleR(View):
    def get(self,request):
        return HttpResponse('this is GET')
    def post(self,request):
        return HttpResponse('this is post')
    
class revr(View):
    def get(self,request):
        return HttpResponseRedirect((reverse_lazy('amrin')))

class homefromcbv(TemplateView):
    name = 'mit'
    template_name = 'homefromcbv.html'
    extra_context = {'naam' : name}

class overide(TemplateView):
    name = 'mit'
    time_now = datetime.now()
    template_name = 'homefromcbv.html'
    def get_context_data(self, **kwargs):
        extra_data = super().get_context_data(**kwargs)
        extra_data['naam'] = self.name
        extra_data['time'] = self.time_now
        return extra_data

class jump(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        dig = self.request.POST.get('digit')
        if dig:
            return f'https://jsonplaceholder.typicode.com/posts/{dig}'
        else:
            return f'https://jsonplaceholder.typicode.com/posts/'
        
class prac(TemplateView):
    template_name = 'xapi.html'
    def get_collage(self):
        indx = self.request.GET.get('digit')
        st = collage.objects.get(collage_id = indx)
        st_nm = st.name
        return st_nm
    def get_context_data(self, **kwargs):
        collage_name =  super().get_context_data(**kwargs)
        collage_name_is = self.get_collage()
        collage_name['done'] = collage_name_is
        return collage_name
    
class prac_add(View):
    def post(self,request):
        name = self.request.POST.get('col_name')
        cd = collage(name=name)
        cd.save()
        return HttpResponse('created susceessfully')

class show1list(ListView):
    model = student
    template_name = "xapi.html"
    context_object_name = 'mycoll' 

class show2list(BaseListView):
    model = collage
    paginate_by = 2

    def get_queryset(self):
        return collage.objects.all().order_by('collage_id')
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = request.GET.get('digit',1)
        paginator = self.get_paginator(queryset,self.paginate_by)
        
        try:
            collage_pages = paginator.page(page)
        except PageNotAnInteger:
            collage_pages = paginator.page(1)
        except EmptyPage:
            collage_pages = paginator.page(paginator.num_pages)

        
        collage_data = list(collage_pages.object_list.values('collage_id','name'))

        # Response with pagination metadata
        return JsonResponse({
            'collages': collage_data,
            'page': collage_pages.number,
            'has_next': collage_pages.has_next(),
            'has_previous': collage_pages.has_previous(),
            'total_pages': paginator.num_pages,
            'total_students': paginator.count
        })
    
class detail(DetailView):
    model = student
    pk_url_kwarg = 'pk'
    #slug bhi option mein
    template_name = "xapi.html"
    context_object_name = 'stud'


class crev(CreateView):
    model = student
    fields = ['name','phone_no','address']
    template_name = "home.html"
    success_url = reverse_lazy('parul_added')

    def form_valid(self, form):
        obj_n = form.instance.name
        obj_n = obj_n.lower()
        form.instance.name = obj_n
        return super().form_valid(form)

class updat(UpdateView):
    model = student
    fields = ['name','phone_no','address']
    template_name = "home.html"
    success_url = reverse_lazy('parul_added')
    #def get_object(self, queryset=None):
        # condition for who update this
        
class delv(DeleteView):
    model = student
    template_name = "home.html"
    success_url = reverse_lazy('parul_added')



# Create your views here.
##############################################################################
@api_view(['GET','POST'])
def collage_list(request):
    if(request.method == 'GET'):
        collages = collage.objects.all()
        serializer = collageserializer(collages, many=True)
        return Response(serializer.data)
    elif(request.method=='POST'):
        serializer = collageserializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    else:
        return Response(serializer.errors)

@api_view(['GET','PUT','DELETE'])
def collage_updates(request,pk):
    try:
        collages = collage.objects.get(pk=pk)
    except collage.DoesNotExist:
        return Response({'error':'collage not found'})


    if(request.method=='GET'):
        serializer = collageserializer(collages)
        return Response(serializer.data)
    elif(request.method=='PUT'):
        serializer = collageserializer(collages, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    elif(request.method=='DELETE'):
        collages.delete()
        return Response({'message': 'collage deleted successfully.'},)


@api_view(['GET'])
def student_info(request):
    if(request.method == 'GET'):
        students = student.objects.all()
        serializer = studentserializer(students, many=True)
        return Response(serializer.data)   
    

#class based apis

#using genericapi with mixins
"""
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView

# List + Create
class CompanyListCreateView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = company.objects.all()
    serializer_class = companyserializer
    permission_classes = [DjangoModelPermissions]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Retrieve + Update + Delete
class CompanyDetailView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = company.objects.all()
    serializer_class = companyserializer
    permission_classes = [DjangoModelPermissions]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Custom endpoint: /companies/<pk>/employs/
class CompanyEmployeesView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get(self, request, pk):
        try:
            currunt_company = company.objects.get(pk=pk)
            employees_of_this = employee.objects.filter(company=currunt_company)
            emp_serializer = employeeserializer(employees_of_this, many=True)
            return Response(emp_serializer.data)
        except company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
# List + Create
class EmployeeListCreateView(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             generics.GenericAPIView):
    queryset = employee.objects.all()
    serializer_class = employeeserializer
    permission_classes = [DjangoModelPermissions]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Retrieve + Update + Delete
class EmployeeDetailView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = employee.objects.all()
    serializer_class = employeeserializer
    permission_classes = [DjangoModelPermissions]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
url may be for single company's employeesdetails is like this
  path('companies/<int:pk>/employs/', CompanyEmployeesView.as_view(), name='company-employees'),

"""

#using cencreteapi view
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView

# List + Create Companies
class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = company.objects.all()
    serializer_class = companyserializer
    permission_classes = [DjangoModelPermissions]

# Retrieve + Update + Delete Company
class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = company.objects.all()
    serializer_class = companyserializer
    permission_classes = [DjangoModelPermissions]

# Custom view to get employees of a specific company
class CompanyEmployeesView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get(self, request, pk):
        try:
            currunt_company = company.objects.get(pk=pk)
            employees_of_this = employee.objects.filter(company=currunt_company)
            emp_serializer = employeeserializer(employees_of_this, many=True)
            return Response(emp_serializer.data)
        except company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

            # List + Create Employees
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = employee.objects.all()
    serializer_class = employeeserializer
    permission_classes = [DjangoModelPermissions]

# Retrieve + Update + Delete Employee
class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = employee.objects.all()
    serializer_class = employeeserializer
    permission_classes = [DjangoModelPermissions]

    
for this access url should be
  path('companies/<int:pk>/employs/', CompanyEmployeesView.as_view(), name='company-employees'),

"""

# using_viewset
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions

class companyview(viewsets.ViewSet):
    permission_classes = [DjangoModelPermissions]

    def list(self, request):
        companies = company.objects.all()
        serializer = companyserializer(companies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            currunt_company = company.objects.get(pk=pk)
            serializer = companyserializer(currunt_company)
            return Response(serializer.data)
        except company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = companyserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            obj = company.objects.get(pk=pk)
        except company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = companyserializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            obj = company.objects.get(pk=pk)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def employs(self, request, pk=None):
        try:
            currunt_company = company.objects.get(pk=pk)
            employees_of_this = employee.objects.filter(company=currunt_company)
            emp_serializer = employeeserializer(employees_of_this, many=True)
            return Response(emp_serializer.data)
        except company.DoesNotExist:
            return Response({'error': 'Company does not exist'}, status=status.HTTP_404_NOT_FOUND)

class employeeview(viewsets.ViewSet):
    permission_classes = [DjangoModelPermissions]

    def list(self, request):
        employees = employee.objects.all()
        serializer = employeeserializer(employees, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            emp = employee.objects.get(pk=pk)
            serializer = employeeserializer(emp)
            return Response(serializer.data)
        except employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = employeeserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            emp = employee.objects.get(pk=pk)
        except employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = employeeserializer(emp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            emp = employee.objects.get(pk=pk)
            emp.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

"""
#easyeast way using_modelviewsets
class companyview(viewsets.ModelViewSet):
    queryset = company.objects.all()
    serializer_class = companyserializer
    

    @action(detail=True,methods = ['get'])
    def employs(self,request,pk):
        try:   
            currunt_company = company.objects.get(pk=pk)
            employees_of_this = employee.objects.filter(company=currunt_company)
            emp_serializer = employeeserializer(employees_of_this,many=True)
            return Response(emp_serializer.data)
        except:
            return Response('company does not exist')

class employeeview(viewsets.ModelViewSet):
    queryset = employee.objects.all()
    serializer_class = employeeserializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
   # filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    #filterset_fields = ['address']
    #search_fields = ['name','address']
   # filter_backends = [OrderingFilter]
    #pagination_class = mycursor
    
    