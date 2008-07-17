from django import newforms as forms
from django.utils.translation import ugettext_lazy as _

from bookmarks.models import Bookmark, BookmarkInstance

class BookmarkForm(forms.ModelForm):
    
    url = forms.URLField(label = "URL", verify_exists=True, widget=forms.TextInput(attrs={"size": 40}))
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"size": 40}))
    redirect = forms.BooleanField(label="Redirect", required=False)
    
    def clean_url(self):
        if Bookmark.objects.filter(url=self.cleaned_data["url"]).count() > 0:
            raise forms.ValidationError(_("That url has already been submitted and Pinax does not yet support multiple bookmarking of a URL"))
        return self.cleaned_data["url"]
    
    def should_redirect(self):
        if self.cleaned_data["redirect"]:
            return True
        else:
            return False
    
    class Meta:
        model = Bookmark
        exclude = ('adder', 'added', 'has_favicon', 'favicon_checked')


class BookmarkInstanceForm(forms.ModelForm):
    
    url = forms.URLField(label = "URL", verify_exists=True, widget=forms.TextInput(attrs={"size": 40}))
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"size": 40}))
    redirect = forms.BooleanField(label="Redirect", required=False)
    
    def should_redirect(self):
        if self.cleaned_data["redirect"]:
            return True
        else:
            return False
    
    def save(self, commit=True):
        self.instance.url = self.cleaned_data['url']
        return super(BookmarkInstanceForm, self).save(commit)
    
    class Meta:
        model = BookmarkInstance
        exclude = ('user', 'bookmark', 'saved')
