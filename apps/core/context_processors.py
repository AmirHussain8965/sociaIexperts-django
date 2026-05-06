from .forms import NewsletterForm


def newsletter_form(request):
    """Context processor to make newsletter form available on all pages"""
    return {
        'newsletter_form': NewsletterForm()
    }
