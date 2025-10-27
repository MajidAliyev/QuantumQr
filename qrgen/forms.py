from django import forms
from .models import QRCode


class QRCodeForm(forms.ModelForm):
    """Form for creating QR codes"""
    data = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'rows': 4,
            'placeholder': 'Enter URL, text, or data...'
        }),
        required=False
    )

    destination_url = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'https://example.com'
        }),
        required=False,
        label='Destination URL (for dynamic QR codes)'
    )

    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'My QR Code'
        })
    )

    qr_type = forms.ChoiceField(
        choices=QRCode.qr_type.field.choices,
        widget=forms.RadioSelect(attrs={'class': 'inline-flex'}),
        initial='static'
    )

    fill_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'h-10 w-20 border border-gray-300 rounded cursor-pointer'
        }),
        initial='#000000'
    )

    back_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'h-10 w-20 border border-gray-300 rounded cursor-pointer'
        }),
        initial='#FFFFFF'
    )

    error_correction = forms.ChoiceField(
        choices=QRCode.error_correction.field.choices,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )

    size = forms.IntegerField(
        min_value=100,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )

    logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
        })
    )

    class Meta:
        model = QRCode
        fields = ['name', 'qr_type', 'data', 'destination_url', 'fill_color',
                  'back_color', 'error_correction', 'size', 'logo']


class QRCodeUpdateForm(forms.ModelForm):
    """Form for updating QR codes (mainly for dynamic codes)"""
    destination_url = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )

    class Meta:
        model = QRCode
        fields = ['destination_url']


class BulkUploadForm(forms.Form):
    """Form for bulk CSV upload"""
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
        }),
        label='Upload CSV file'
    )

    fill_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'h-10 w-20 border border-gray-300 rounded cursor-pointer'
        }),
        initial='#000000',
        required=False
    )

    back_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'h-10 w-20 border border-gray-300 rounded cursor-pointer'
        }),
        initial='#FFFFFF',
        required=False
    )
