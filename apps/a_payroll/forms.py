from django import forms
from .models import Employee, EmployeeTaxData, EmployeeJobData 
from .models import Dependence, Position, Type, Movement,TypeEmployee,TypePayroll,Bank,WorkingDay,TypeSalary,TaxRegime, CategoryTab, AttributeCatalog,CategoryAttribute, Period

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        widgets = {
            "key": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "paternal_surname": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "maternal_surname": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "cellphone": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "municipality": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "colony": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "street": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "no_ext": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "no_int": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "reference": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "languages": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "sex": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),
            "marital_status": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),                                                                                                                                                                                                                   

        }

    def clean(self):
        cleaned_data = super().clean()
        for key, value in cleaned_data.items():
            if value == "":
                cleaned_data[key] = None
        return cleaned_data

class NullEmptyMixin:
    def clean(self):
        cleaned_data = super().clean()
        for field, value in cleaned_data.items():
            if value == "":
                cleaned_data[field] = None
        return cleaned_data

class EmployeeJobForm(NullEmptyMixin,forms.ModelForm):
    class Meta:
        model = EmployeeJobData
        exclude = ["employee","position","type_employee","type_payroll","total_salary","category"]
        fields = "__all__"
        widgets={
            "dependence": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),           
            "base_date": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "contract_date": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "contract_termination_date": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),                                                                 
            "account_no": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "bank": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),
            "check_in_time": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "check_out_time": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "working_day": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),
            "type_salary": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),
            "description":forms.Textarea(
                attrs={
                    "rows": "2",
                    "placeholder": "Deja un comentario u observación...",
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2",
                }
            ),                                                                                      
        }

    def clean(self):
        cleaned_data = super().clean()
        for key, value in cleaned_data.items():
            if value == "":
                cleaned_data[key] = None
        return cleaned_data

class EmployeeTaxForm(NullEmptyMixin,forms.ModelForm):
    class Meta:
        model = EmployeeTaxData
        exclude = ["employee"]
        fields="__all__"
        widgets = {
            "tax_regime": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),
            "rfc": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "curp": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "nss": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "cp": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "birth_date": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),                                                              
        }

    def clean(self):
        cleaned_data = super().clean()
        for key, value in cleaned_data.items():
            if value == "":
                cleaned_data[key] = None
        return cleaned_data        

class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = "__all__"
        widgets = {
            "start_date": forms.TextInput(
                attrs={
                    "type":"date",
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "end_date": forms.TextInput(
                attrs={
                    "type":"date",
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "description":forms.Textarea(
                attrs={
                    "rows": "2",
                    "placeholder": "Deja un comentario u observación...",
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2",
                }
            ),              
        }

class PayrollDependenceForm(forms.ModelForm):
    class Meta:
        model = Dependence
        fields = "__all__"
        widgets = {
            "key": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "description":forms.Textarea(
                attrs={
                    "rows": "2",
                    "placeholder": "Deja un comentario u observación...",
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2",
                }
            ),                
        }

class PayrollCategoryForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"
        widgets = {
            "key": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "description":forms.Textarea(
                attrs={
                    "rows": "2",
                    "placeholder": "Deja un comentario u observación...",
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2",
                }
            ),                
        }

class PayrollTypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = "__all__"
        widgets = {
            "key": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "description":forms.Textarea(
                attrs={
                    "rows": "2",
                    "placeholder": "Deja un comentario u observación...",
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2",
                }
            ),                
        }    

class PayrollMovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = "__all__"
        widgets = {
            "key": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "description":forms.Textarea(
                attrs={
                    "rows": "2",
                    "placeholder": "Deja un comentario u observación...",
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2",
                }
            ),                
        }  

class PayrollTypeEmployeeForm(forms.ModelForm):
    class Meta:
        model = TypeEmployee
        fields = "__all__"
        widgets = {
            "key": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "description":forms.Textarea(
                attrs={
                    "rows": "2",
                    "placeholder": "Deja un comentario u observación...",
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2",
                }
            ),                
        }  

class PayrollTypePayrollForm(forms.ModelForm):
    class Meta:
        model = TypePayroll
        fields = "__all__"
        widgets = {
            "key": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "description":forms.Textarea(
                attrs={
                    "rows": "2",
                    "placeholder": "Deja un comentario u observación...",
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2",
                }
            ),                
        }    

class CategoryTabForm(forms.ModelForm):
    class Meta:
        model = CategoryTab
        fields = "__all__"
        widgets = {
            "position": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),
            "type_employee": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),
            "type_payroll": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),                                            
        }                           

class AttributeCatalogForm(forms.ModelForm):
    class Meta:
        model = AttributeCatalog
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "type": forms.Select(
                attrs={
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                }
            ),
            "description":forms.Textarea(
                attrs={
                    "rows": "2",
                    "placeholder": "Deja un comentario u observación...",
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2",
                }
            ),                            
        }

class CategoryAttributeForm(forms.ModelForm):
    class Meta:
        model = CategoryAttribute
        fields = "__all__"

        
