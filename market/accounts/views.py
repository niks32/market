from django.contrib.auth.decorators import login_required
from django.template.response       import TemplateResponse
from django.shortcuts               import get_object_or_404
from django.contrib                 import messages
from django.core.urlresolvers       import reverse
from django.http                    import HttpResponseRedirect


from .models import Company, CompanyBook
from .forms  import CompanyForm, CompanyBookForm

@login_required( None, None, "/profile/login" )
def details(request):
    ctx = {'company_book': request.user.company_book.all()}
    return TemplateResponse(request, "accounts/details.html", ctx)


def validate_address_and_render(request, company_form, company_book_form,
                                success_message):
    if company_form.is_valid() and company_book_form.is_valid():
        company = company_form.save()
        company_book_form.instance.company = company
        company_book = company_book_form.save()
        messages.success(request, success_message % company_book)
        return HttpResponseRedirect(reverse("profile:details"))

    return TemplateResponse(
        request,
        "accounts/company-edit.html",
        {'company_form': company_form, 'company_book_form': company_book_form })



@login_required( None, None, "/profile/login" )
def company_create(request):
    if request.POST:
        company_form      = CompanyForm(request.POST)
        company_book_form = CompanyBookForm(request.POST, instance=CompanyBook(user=request.user))
    else:
        company_form        = CompanyForm()
        company_book_form   = CompanyBookForm()

    message = "Компания успешно добавлена"
    return validate_address_and_render(request, company_form, company_book_form, message)

@login_required( None, None, "/profile/login" )
def company_edit(request, pk, slug):
        company_book        = get_object_or_404(CompanyBook, pk=pk, user=request.user)
        company             = company_book.company
        company_form        = CompanyForm(instance=company)
        company_book_form   = CompanyBookForm(instance=company_book)

        msg = 'fuck it'

        return validate_address_and_render(request, company_form, company_book_form, msg)