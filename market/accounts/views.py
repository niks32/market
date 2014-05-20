from django.contrib.auth.decorators import login_required
from django.template.response       import TemplateResponse
from django.shortcuts               import get_object_or_404, redirect
from django.contrib                 import messages
from django.core.urlresolvers       import reverse
from django.http                    import HttpResponseRedirect, Http404


from .models import Company, CompanyBook
from .forms  import CompanyForm, CompanyBookForm, UserForm

@login_required( None, None, "/profile/login" )
def details(request):
    ctx = {'company_book': request.user.company_book.all(), 'user_form': UserForm }
    return TemplateResponse(request, "accounts/details.html", ctx)


def validate_address_and_render(request, company_form, company_book_form,
                                success_message):
    if company_form.is_valid() and company_book_form.is_valid():
        try:
            company = company_form.save()
            company_book_form.instance.company = company
            company_book_form.save()
            messages.success(request, success_message + " %s" % company)
            return HttpResponseRedirect(reverse("account:details"))
        except:
            messages.warning(request, "Ошибка добавления.")
            return redirect("account:details")

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


@login_required( None, None, "/profile/login" )
def company_make_default(request, pk):
    user = request.user
    company_book = get_object_or_404(CompanyBook, pk=pk, user=user)
    user.default_company = company_book
    user.save()
    return redirect('account:details')


@login_required( None, None, "/profile/login" )
def company_delete(request, slug, pk):
    company_book = get_object_or_404(CompanyBook, pk=pk, user=request.user)

    if not company_book.get_slug():
        raise Http404

    if request.POST:
        company_book.company.delete()
        message = "Компания '%s' удалена."
        messages.success(request, message % company_book.company)
        return HttpResponseRedirect(reverse("account:details"))

    return TemplateResponse(request, "accounts/company-delete.html", {"company": company_book.company})